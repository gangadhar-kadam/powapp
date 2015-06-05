# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt.

from __future__ import unicode_literals
import webnotes
import webbrowser
from webnotes import _, throw
from webnotes.utils import flt, cint,cstr
import json

def get_customer_list(doctype, txt, searchfield, start, page_len, filters):
	if webnotes.conn.get_default("cust_master_name") == "Customer Name":
		fields = ["name", "customer_group", "territory"]
	else:
		fields = ["name", "customer_name", "customer_group", "territory"]
		
	return webnotes.conn.sql("""select %s from `tabCustomer` where docstatus < 2 
		and (%s like %s or customer_name like %s) order by 
		case when name like %s then 0 else 1 end,
		case when customer_name like %s then 0 else 1 end,
		name, customer_name limit %s, %s""" % 
		(", ".join(fields), searchfield, "%s", "%s", "%s", "%s", "%s", "%s"), 
		("%%%s%%" % txt, "%%%s%%" % txt, "%%%s%%" % txt, "%%%s%%" % txt, start, page_len))
		
@webnotes.whitelist()
def get_item_details(args):
	"""
		args = {
			"item_code": "",
			"warehouse": None,
			"customer": "",
			"conversion_rate": 1.0,
			"selling_price_list": None,
			"price_list_currency": None,
			"plc_conversion_rate": 1.0
		}
	"""

	if isinstance(args, basestring):
		args = json.loads(args)
	args = webnotes._dict(args)
	
	if args.barcode:
		args.item_code = _get_item_code(barcode=args.barcode)
	elif not args.item_code and args.serial_no:
		args.item_code = _get_item_code(serial_no=args.serial_no)
	
	item_bean = webnotes.bean("Item", args.item_code)
	
	_validate_item_details(args, item_bean.doc)
	
	meta = webnotes.get_doctype(args.doctype)

	# hack! for Sales Order Item
	warehouse_fieldname = "warehouse"
	if meta.get_field("reserved_warehouse", parentfield=args.parentfield):
		warehouse_fieldname = "reserved_warehouse"
	
	out = _get_basic_details(args, item_bean, warehouse_fieldname)
	
	if meta.get_field("currency"):
		out.base_ref_rate = out.basic_rate = out.ref_rate = out.export_rate = 0.0
		
		if args.selling_price_list and args.price_list_currency:
			out.update(_get_price_list_rate(args, item_bean, meta))
		
	out.update(_get_item_discount(out.item_group, args.customer))
	
	if out.get(warehouse_fieldname):
		out.update(get_available_qty(args.item_code, out.get(warehouse_fieldname)))
	
	out.customer_item_code = _get_customer_item_code(args, item_bean)
	
	if cint(args.is_pos):
		pos_settings = get_pos_settings(args.company)
		if pos_settings:
			out.update(apply_pos_settings(pos_settings, out))
		
	if args.doctype in ("Sales Invoice", "Delivery Note"):
		if item_bean.doc.has_serial_no == "Yes" and not args.serial_no:
			out.serial_no = _get_serial_nos_by_fifo(args, item_bean)
		
	return out

def _get_serial_nos_by_fifo(args, item_bean):
	return "\n".join(webnotes.conn.sql_list("""select name from `tabSerial No` 
		where item_code=%(item_code)s and warehouse=%(warehouse)s and status='Available' 
		order by timestamp(purchase_date, purchase_time) asc limit %(qty)s""", {
			"item_code": args.item_code,
			"warehouse": args.warehouse,
			"qty": cint(args.qty)
		}))

def _get_item_code(barcode=None, serial_no=None):
	if barcode:
		input_type = "Barcode"
		item_code = webnotes.conn.sql_list("""select name from `tabItem` where barcode=%s""", barcode)
	elif serial_no:
		input_type = "Serial No"
		item_code = webnotes.conn.sql_list("""select item_code from `tabSerial No` 
			where name=%s""", serial_no)
			
	if not item_code:
		throw(_("No Item found with ") + input_type + ": %s" % (barcode or serial_no))
	
	return item_code[0]
	
def _validate_item_details(args, item):
	from utilities.transaction_base import validate_item_fetch
	validate_item_fetch(args, item)
	
	# validate if sales item or service item
	if args.order_type == "Maintenance":
		if item.is_service_item != "Yes":
			throw(_("Item") + (" %s: " % item.name) + 
				_("not a service item.") +
				_("Please select a service item or change the order type to Sales."))
		
	elif item.is_sales_item != "Yes":
		throw(_("Item") + (" %s: " % item.name) + _("not a sales item"))
			
def _get_basic_details(args, item_bean, warehouse_fieldname):
	item = item_bean.doc
	
	from webnotes.defaults import get_user_default_as_list
	user_default_warehouse_list = get_user_default_as_list('warehouse')
	user_default_warehouse = user_default_warehouse_list[0] \
		if len(user_default_warehouse_list)==1 else ""
	
	out = webnotes._dict({
			"item_code": item.name,
			"description": item.description_html or item.description,
			warehouse_fieldname: user_default_warehouse or item.default_warehouse \
				or args.get(warehouse_fieldname),
			"income_account": item.default_income_account or args.income_account \
				or webnotes.conn.get_value("Company", args.company, "default_income_account"),
			"expense_account": item.purchase_account or args.expense_account \
				or webnotes.conn.get_value("Company", args.company, "default_expense_account"),
			"cost_center": item.default_sales_cost_center or args.cost_center,
			"qty": 1.0,
			"export_amount": 0.0,
			"amount": 0.0,
			"batch_no": None,
			"item_tax_rate": json.dumps(dict(([d.tax_type, d.tax_rate] for d in 
				item_bean.doclist.get({"parentfield": "item_tax"})))),
		})
	
	for fieldname in ("item_name", "item_group", "barcode", "brand", "stock_uom"):
		out[fieldname] = item.fields.get(fieldname)
			
	return out
	
def _get_price_list_rate(args, item_bean, meta):
	ref_rate = webnotes.conn.sql("""select ref_rate from `tabItem Price` 
		where price_list=%s and item_code=%s and selling=1""", 
		(args.selling_price_list, args.item_code), as_dict=1)

	if not ref_rate:
		return {}
	
	# found price list rate - now we can validate
	from utilities.transaction_base import validate_currency
	validate_currency(args, item_bean.doc, meta)
	
	return {"ref_rate": flt(ref_rate[0].ref_rate) * flt(args.plc_conversion_rate) / flt(args.conversion_rate)}
	
def _get_item_discount(item_group, customer):
	parent_item_groups = [x[0] for x in webnotes.conn.sql("""SELECT parent.name 
		FROM `tabItem Group` AS node, `tabItem Group` AS parent 
		WHERE parent.lft <= node.lft and parent.rgt >= node.rgt and node.name = %s
		GROUP BY parent.name 
		ORDER BY parent.lft desc""", (item_group,))]
		
	discount = 0
	for d in parent_item_groups:
		res = webnotes.conn.sql("""select discount, name from `tabCustomer Discount` 
			where parent = %s and item_group = %s""", (customer, d))
		if res:
			discount = flt(res[0][0])
			break
			
	return {"adj_rate": discount}

@webnotes.whitelist()
def get_available_qty(item_code, warehouse):
	return webnotes.conn.get_value("Bin", {"item_code": item_code, "warehouse": warehouse}, 
		["projected_qty", "actual_qty"], as_dict=True) or {}
		
def _get_customer_item_code(args, item_bean):
	customer_item_code = item_bean.doclist.get({"parentfield": "item_customer_details",
		"customer_name": args.customer})
	
	return customer_item_code and customer_item_code[0].ref_code or None
	
def get_pos_settings(company):
	pos_settings = webnotes.conn.sql("""select * from `tabPOS Setting` where user = %s 
		and company = %s""", (webnotes.session['user'], company), as_dict=1)
	
	if not pos_settings:
		pos_settings = webnotes.conn.sql("""select * from `tabPOS Setting` 
			where ifnull(user,'') = '' and company = %s""", company, as_dict=1)
			
	return pos_settings and pos_settings[0] or None
	
def apply_pos_settings(pos_settings, opts):
	out = {}
	
	for fieldname in ("income_account", "cost_center", "warehouse", "expense_account"):
		if not opts.get(fieldname):
			out[fieldname] = pos_settings.get(fieldname)
			
	if out.get("warehouse"):
		out["actual_qty"] = get_available_qty(opts.item_code, out.get("warehouse")).get("actual_qty")
	
	return out

@webnotes.whitelist(allow_guest=True)
def login(api_key,username,password,_type='POST'):
   	login =[]
	loginObj = {}
   	if len(api_key)<3:
		key={}
		login.append(key)
		loginObj['status']='403'
		loginObj['error']='Invalid API Key'
		#loginObj['key']=login
		return loginObj
   	elif len(username)<3 :
		key={}
		login.append(key)
		loginObj['status']='400'
		loginObj['error']='Invalid Username'
		#loginObj['key']=login
		return loginObj 

	elif len(password)<3:
		key={}
		login.append(key)
		loginObj['status']='402'
		loginObj['error']='Invalid Password'
		#loginObj['key']=login
		return loginObj 
   	else:	
		qr="select password from __Auth where user="+username+" and password=password("+password+")"
		res=webnotes.conn.sql(qr)
		#return res
		#rg=webnotes.conn.sql("select region from `tabFranchise` where contact_email="+username+"")
		from webnotes.model.doc import Document
		import random
		import string
		char_set = string.ascii_uppercase + string.digits
		rn=''.join(random.sample(char_set*6,9))
		if res :
			rr="select auth_key from `tabauth keys` where name="+username
			rs=webnotes.conn.sql(rr)
			if rs:
				key={}
              	       		key['auth_key'] = rs[0][0]
				login.append(key)
				loginObj['status']='200'
				loginObj['key']=login
				return loginObj
			else:
				d = Document('auth keys')
				d.user_name=username[1:-1]
				d.password=password[1:-1]
				d.auth_key=''.join(random.sample(char_set*6,9))
		                d.save()
				webnotes.conn.commit()
				key={}
	                        key['auth_key'] = d.password
				login.append(key)
				loginObj['status']='200'
				loginObj['key']=login
				return loginObj
		else:
			key={}
			login.append(key)
			loginObj['status']='401'
			loginObj['error']='Incorrect User name or password '
			#loginObj['key']=login
			return loginObj

@webnotes.whitelist(allow_guest=True)
def search_subfranchise(auth_key,creation):
	login =[]
	key={}
	loginObj = {}
	qr="select name from `tabauth keys` where auth_key="+auth_key
	res=webnotes.conn.sql(qr)
	rgn=webnotes.conn.sql("select region from `tabFranchise` where contact_email='"+res[0][0]+"'")
	if res:
		qry="select name,sf_name,creation from `tabSub Franchise` where creation>='"+creation[1:-1]+"' and region='"+rgn[0][0]+"'"
		#return qry
		rs=webnotes.conn.sql(qry)
		if rs:
			for name,sf_name,creation in rs:
				key={}
				key['id']=name
				key['name']=sf_name
				key['creation']=creation
				login.append(key)
				loginObj['status']='200'
				loginObj['subfranchise']=login
			return loginObj			
		else:			
                        key={}
                        #login.append(key)
                        loginObj['status']='200'
                        loginObj['subfranchise']=login
			return loginObj
		
	else:
		key={}
		login.append(key)
		loginObj['status']='401'
		loginObj['error']='Invalid Auth Key'
		return loginObj

@webnotes.whitelist(allow_guest=True)
def search_customer(auth_key,creation):
	login =[]
	loginObj = {}
	qr="select name from `tabauth keys` where auth_key="+auth_key
	res=webnotes.conn.sql(qr)
	rgn=webnotes.conn.sql("select region from `tabFranchise` where contact_email='"+res[0][0]+"'")
	if res:
		qry="select name,customer_name,creation from `tabCustomer Details` where creation>='"+creation[1:-1]+"' and region='"+rgn[0][0]+"'"
		rs=webnotes.conn.sql(qry)
		
		if rs:
			for name,sf_name,creation in rs:
				key={}
				key['id']=name
				key['name']=sf_name
				key['creation']=creation
				login.append(key)
				loginObj['status']='200'
				loginObj['customers']=login
			return loginObj			
		else:	
			key={}		
			#login.append(key)
			loginObj['status']='200'
			loginObj['customers']=login
			return loginObj
		
	else:
		key={}
		login.append(key)
		loginObj['status']='401'
		loginObj['error']='Invalid Auth Key'
		return loginObj


@webnotes.whitelist(allow_guest=True)
def search_invoice(auth_key,date,battery_serial_no,subfranchise_id,invoice_number):
	login =[]
	loginObj = {}
	qr="select name from `tabauth keys` where auth_key="+auth_key
	res=webnotes.conn.sql(qr)
	rgn=webnotes.conn.sql("select region from `tabFranchise` where contact_email='"+res[0][0]+"'")
	dt=date[1:-1]
	nm=invoice_number[1:-1]
	sr=battery_serial_no[1:-1]
	sf=subfranchise_id[1:-1]
	if res:
		qry="select distinct(si.name),si.customer from `tabSales Invoice` si ,`tabSales Invoice Item` sii where si.name=sii.parent and si.name like '%"+nm+"%' or si.posting_date like '%"+dt+"%' or customer like '%"+sf+"%' or sii.serial_no like '%"+sr+"%' and si.region='"+rgn[0][0]+"'"
		rs=webnotes.conn.sql(qry)
		if rs:
			for ss in rs:
				key={}
				key['id']=ss[0]
				key['number']=ss[0]
				key['invoice_type']=ss[0]
				key['name']=ss[1]
				login.append(key)
			loginObj['status']='200'
			loginObj['invoices']=login
			return loginObj
		else:
			key={}
			login.append(key)
			loginObj['status']='400'
			loginObj['invoices']='[]'
			return loginObj
		
	else:
		key={}
		login.append(key)
		loginObj['status']='401'
		loginObj['error']='Invalid Auth key'
		return loginObj

@webnotes.whitelist(allow_guest=True)
def invoice_details(auth_key,creation):
	login =[]
	invObj={}
	qr="select name from `tabauth keys` where auth_key="+auth_key
	res=webnotes.conn.sql(qr)
	rgn=webnotes.conn.sql("select region from `tabFranchise` where contact_email='"+res[0][0]+"'")
	if res:
	    qry="select name,customer,invoice_type,customer_address,posting_date,creation from `tabSales Invoice` where region='"+rgn[0][0]+"' and creation>='"+creation[1:-1]+"'"
	    #return qry
	    rss=webnotes.conn.sql(qry,as_dict=1)
	    #return rss
    	    if rss:
		for rs in rss:
			rr="select item_name,serial_no,qty,export_rate,parent,name from `tabSales Invoice Item` where parent='"+cstr(rs['name'])+"'"
		        rr1=webnotes.conn.sql(rr,as_dict=1)
			inv=[]
			if rr1:
			   for item_data in rr1:
			   	inv.append({"item_name":item_data['item_name'],"serial_no":item_data['serial_no'],"qty":item_data['qty'],"rate":item_data['export_rate']})
		    	login.append({"name":rs['name'],"customer":rs['customer'],"invoice_type":rs['invoice_type'],"customer_address":rs['customer_address'],"creation":rs['creation'],"item_details":inv})
		invObj['status']='200'		
		invObj['invoice_details']=login
	    	#invObj.append({'status':'200','invoice_details':login})
		return invObj
            else:
		key={}
		invObj['status']='200'
		invObj['invoice_details']=login
		#invObj.append({'status':'400','message':'No data found'})
		return invObj
	else:
          invObj.append({'status':'401','error':'Invalid Auth Key'})
	  return invObj

@webnotes.whitelist(allow_guest=True)
def dashboard(auth_key):
	loginObj = {}
	qr="select name from `tabauth keys` where auth_key="+auth_key
	res=webnotes.conn.sql(qr)
	if res :
		rr="select account_id,name,region from `tabFranchise` where contact_email='"+res[0][0]+"'"
		r1=webnotes.conn.sql(rr)
		#webnotes.errprint(r1)
		
		if r1:
			aa="select sum(b.qty),a.modified from `tabStock Entry` a ,`tabStock Entry Detail` b where date_format(a.creation, '%Y-%m-%d')=CURDATE() and a.docstatus=1 and a.name=b.parent and a.purpose='Material Transfer' and lower(a.to_warehouse)=lower('"+r1[0][0]+"') "
			#webnotes.errprint(aa)
			r2=webnotes.conn.sql(aa)
			#webnotes.errprint(r2)
			if r2:
				bb="select name from `tabSales Invoice`  where date_format(creation, '%Y-%m-%d')=CURDATE() and territory='"+r1[0][2]+"'"
				r3=webnotes.conn.sql(bb)
				#webnotes.errprint(bb)
				if r3:
					cc="select sum(qty) from `tabSales Invoice Item`  where parent in ("+bb+")"
					r4=webnotes.conn.sql(cc)
					#webnotes.errprint(r2)
					#return r2
					if r4:
						loginObj['status']='200'
						loginObj['total_battery_load']=r2[0][0]
						loginObj['sales_invoices']=r3
						loginObj['total_battery_sold']=r4[0][0]
						loginObj['balance_batteries']=cstr(r2[0][0]-r4[0][0])
						loginObj['support_sms_no']='9960066444'
						return loginObj						
					else:
						loginObj['status']='200'
						loginObj['total_battery_load']=r2[0][0]
						loginObj['sales_invoices']=r3
						loginObj['total_battery_sold']='0'
						loginObj['balance_batteries']=r2[0][0]
						loginObj['support_sms_no']='9960066444'
						return loginObj						
				else:
					loginObj['status']='200'
					loginObj['total_battery_load']=r2[0][0]
					loginObj['sales_invoices']='0'
					loginObj['total_battery_sold']='0'
					loginObj['balance_batteries']=r2[0][0]
					loginObj['support_sms_no']='9960066444'
					return loginObj				
			else:
				loginObj['status']='200'
				loginObj['total_battery_load']='0'
				loginObj['sales_invoices']='0'
				loginObj['total_battery_sold']='0'
				loginObj['balance_batteries']='0'
				loginObj['support_sms_no']='9960066444'
				return loginObj				
		else:
			loginObj['status']='500'
			return loginObj
	else:
		loginObj['status']='401'
		loginObj['balance_batteries']='0'
		return loginObj

@webnotes.whitelist(allow_guest=True)
def dashboard1(auth_key):
        loginObj = {}
        qr="select name from `tabauth keys` where auth_key="+auth_key
        res=webnotes.conn.sql(qr)
        if res :
                rr="select account_id,name,region from `tabFranchise` where contact_email='"+res[0][0]+"'"
                r1=webnotes.conn.sql(rr)
                #webnotes.errprint(r1)
		lst=[]
		sr_no=webnotes.conn.sql("select name from `tabSerial No` where status='Available' and lower(warehouse)=lower('"+r1[0][0]+"')")
		#sr_no=webnotes.conn.sql("select count(name) from `tabSerial No` where status='Available' and warehouse=lower('"+r1[0][0]+"')")
                #sr=webnotes.conn.sql(sr_no)
                for sr in sr_no:
			lst.append(sr[0])
               	if r1:
                     	aa="select sum(b.qty),a.modified,b.serial_no from `tabStock Entry` a ,`tabStock Entry Detail` b where date_format(a.creation, '%Y-%m-%d')=CURDATE() and a.docstatus=1 and a.name=b.parent and a.purpose='Material Transfer' and lower(a.to_warehouse)=lower('"+r1[0][0]+"') "
                        #webnotes.errprint(aa)
	                r2=webnotes.conn.sql(aa)
				
		        if r2:
        		       	bb="select name from `tabSales Invoice`  where date_format(creation, '%Y-%m-%d')=CURDATE() and territory='"+r1[0][2]+"'"
                	       	r3=webnotes.conn.sql(bb)
                	       	#webnotes.errprint(bb)
                        	if r3:
                        		cc="select sum(qty) from `tabSales Invoice Item`  where parent in ("+bb+")"
                               		r4=webnotes.conn.sql(cc)
                             		if r4:	
                                       	        loginObj['status']='200'
                                       	        #loginObj['total_battery_load']=r2[0][0]
                                       	        loginObj['sales_invoices']=r3
                                               	loginObj['total_battery_sold']=r4[0][0]
                                               	loginObj['balance_batteries']=lst
                                               	loginObj['support_sms_no']='9960066444'
                                               	return loginObj
					else:
        	                                loginObj['status']='200'
                	                        #loginObj['total_battery_load']=r2[0][0]
                                                loginObj['sales_invoices']=r3
                                                loginObj['total_battery_sold']='0'
                                                loginObj['balance_batteries']=lst
                               	                loginObj['support_sms_no']='9960066444'
                                       	        return loginObj
                               	else:
                               	        loginObj['status']='200'
                               	        #loginObj['total_battery_load']=r2[0][0]
                               	        loginObj['sales_invoices']='0'
                               	        loginObj['total_battery_sold']='0'
                                       	loginObj['balance_batteries']=lst
                               		loginObj['support_sms_no']='9960066444'
                               		return loginObj
                        else:
                                loginObj['status']='200'
                                #loginObj['total_battery_load']='0'
                               	loginObj['sales_invoices']='0'
                               	loginObj['total_battery_sold']='0'
                               	loginObj['balance_batteries']='0'
                               	loginObj['support_sms_no']='9960066444'
                               	return loginObj
		else:
	               	loginObj['status']='500'
	              	return loginObj
        else:
               	loginObj['status']='401'
               	loginObj['balance_batteries']='0'
               	return loginObj

@webnotes.whitelist(allow_guest=True)
def create_customer(auth_key,name,mobile_number,email_id,datetime,version,_type='POST'):
	login =[]
	loginObj = {}	
	qr="select name from `tabauth keys` where auth_key="+auth_key
	res=webnotes.conn.sql(qr)
	if res:
		qr1="select name from `tabCustomer Details` where customer_name="+name+" and phone_number="+mobile_number
		rs=webnotes.conn.sql(qr1)
		rgn=webnotes.conn.sql("select region from `tabFranchise` where contact_email='"+res[0][0]+"'")
		if rs :
			key={}
                        key['customer_id']=rs[0][0]
                        login.append(key)
                        loginObj['status']='200'
                        loginObj['customer']=login

		        return loginObj
		else :
			from webnotes.model.doc import Document
			d = Document('Customer Details')
			if len(name)>3:
				d.customer_name=name[1:-1]
			if len(email_id)>3:
				d.customer_email=email_id[1:-1]
			if len(mobile_number)>3:
				d.phone_number=mobile_number[1:-1]
			d.region=rgn[0][0]
        	        d.save()

			webnotes.conn.commit()
			key={}
			key['customer_id']=d.name
			login.append(key)
			loginObj['status']='200'
			loginObj['customer']=login
			return loginObj
	else:
		loginObj['status']='401'
		return loginObj

@webnotes.whitelist(allow_guest=True)
def create_invoice(auth_key,invoice_type,customer,serial_number,dattime,_type='POST'):
	login =[]
	loginObj = {}
	if len(auth_key[1:-1])<=0 or len(dattime[1:-1])<=0 or len(customer[1:-1])<=0 or len(serial_number[1:-1])<=0 :
		loginObj['status']='401'
		loginObj['error']='Incomplete data to generate Sales Invoice , Please provide token no , Datetime,customer and serial no'
		return loginObj
	qr="select name from `tabauth keys` where auth_key="+auth_key
	res=webnotes.conn.sql(qr)
	rgn=webnotes.conn.sql("select region from `tabFranchise` where contact_email='"+res[0][0]+"'")
	zz=serial_number[1:-1].count(' ')
	xx=serial_number[1:-1].replace('[','').split(' ')
	#xxx=xx.replace(' ','\n')
	yy="select item_code,item_name,description from `tabSerial No` where name='"+cstr(xx[0])+"'"
	zzz=webnotes.conn.sql(yy)
	if not zzz:
          loginObj['status']='402'
          loginObj['error']='Invalid serails no, please try againg'
          return loginObj
	pp="select ref_rate from `tabItem Price` where price_list='Standard Selling' and item_code='"+zzz[0][0]+"'"
	ppp=webnotes.conn.sql(pp)
	if res:
		from webnotes.model.doc import Document
		d = Document('Sales Invoice')
		d.customer=customer[1:-1]
		d.customer_name=customer[1:-1]
		d.region=rgn[0][0]
		d.posting_date=dattime[1:-1]
		d.due_date=dattime[1:-1]
		d.selling_price_list='Standard Selling'
		d.currency='INR'
		d.territory='India'
		if ppp:
			d.net_total_export=ppp[0][0]*zz
			d.grand_total_export=ppp[0][0]*zz
			d.rounded_total_export=ppp[0][0]*zz
			d.outstanding_amount=ppp[0][0]*zz
		d.plc_conversion_rate=1
		from webnotes.utils import nowdate
  		from accounts.utils import get_fiscal_year
   		today = nowdate()
		d.fiscal_year=get_fiscal_year(today)[0]
		d.debit_to=customer[1:-1]+" - P"
		d.is_pos=1
		d.cash_bank_account='Cash - P'
                d.save()
		webnotes.conn.commit()
		e=Document('Sales Invoice Item')
		e.item_code=zzz[0][0]
		e.item_name=zzz[0][1]
		e.description=zzz[0][2]
		e.qty=zz
		e.stock_uom='Nos'
		if ppp:
			e.ref_rate=ppp[0][0]
			e.export_rate=ppp[0][0]
		e.export_amount='0'
		e.income_account='Sales - P'
		e.cost_center='Main - P'
		e.serial_no_=serial_number[1:-1].replace('[','').replace(']','')
		e.parent=d.name
		e.parenttype='Sales Invoice'
		e.parentfield='entries'
		e.save()
		webnotes.conn.commit()
		key={}
		key['invoice_id_id']=d.name
		login.append(key)
		loginObj['status']='200'
		loginObj['invoice']=login
		return loginObj
	else:
		loginObj['status']='401'
		loginObj['error']='invalid token please contact administrator'
		return loginObj


@webnotes.whitelist(allow_guest=True)
def send_message(number,email,message,_type='POST'):
	#webbrowser.open('http://192.168.5.102:2525/server.py?cmd=login&usr=administrator&pwd=admin')
	if len(message[1:-1])<=0 :
		return "Incomplete data to send message, Please provide token no and messages and number or email"
	#qr="select name from `tabauth keys` where auth_key="+token
	#res=webnotes.conn.sql(qr)
	#str='sent '
        from webnotes.utils.email_lib import sendmail
	import requests
	#if res:
	if len(number[1:-1])>0 and len(email[1:-1])>0:
			sendmail(email[1:-1], subject='test', msg = message[1:-1])
			url="http://api.mVaayoo.com/mvaayooapi/MessageCompose?user=samarthjori417@gmail.com:123456&senderID=TEST SMS&receipientno="+number[1:-1]+"&msgtxt="+message[1:-1]+"&state=4"
			r = requests.get(url)
                        login =[]
                        invObj={}
                        invObj['status']='200'
                        invObj['message']='email and sms sent'
                        return invObj

	elif len(number[1:-1])>0:
			url="http://api.mVaayoo.com/mvaayooapi/MessageCompose?user=samarthjori417@gmail.com:123456&senderID=TEST SMS&receipientno="+number[1:-1]+"&msgtxt="+message[1:-1]+"&state=4"
 			r = requests.get(url)
                        login =[]
                        invObj={}
                        invObj['status']='200'
                        invObj['meassage']='sms sent'
                        return invObj

	elif len(email[1:-1])>0:
			sendmail(email[1:-1], subject='test', msg = message[1:-1])
                        login =[]
                        invObj={}
                        invObj['status']='200'
                        invObj['message']='email sent'
                        return invObj
			
	else:
		        login =[]
		        invObj={}
		        invObj['status']='400'
		        invObj['error']='Invalid  data, Please contact Administrator.'
		        return invObj

@webnotes.whitelist(allow_guest=True)
def get_message(number,message,_type='POST'):
	if (cint(len(message[1:-1]))<=0  or cint(len(number[1:-1]))<=0):
		invObj={}
                invObj['status']='401'
                invObj['error']='Incomplete data to send message, Please provide messages and mobile number'
                return invObj
        from webnotes.model.doc import Document
	from webnotes.utils import nowdate,flt,cstr,add_months
        m=message[1:-1].split(',')

	#return m[2]
	bsrn=m[2]
	csrn=m[3]
	vm=m[4]
	un=m[5]
	va=m[6]
        a="select name from `tabCustomer Details` where name='"+m[0]+"-"+number[1:-1]+"'"
	b=webnotes.conn.sql(a)
	itm="select item_code from `tabSerial No` where name='"+cstr(m[2])+"'"
	itemm=webnotes.conn.sql(itm)
        #webnotes.errprint(itemm[0][0])
	#webnotes.errprint(itemm)
        qrs="select warranty_period from tabItem where name='"+cstr(itemm[0][0])+"'"
	#webnotes.errprint("item----------------")
        #webnotes.errprint(itemm[0][0])
        ress=webnotes.conn.sql(qrs)
	#webnotes.errprint("warrenty-----------")
        #webnotes.errprint(ress[0][0])
        if b:
		l = Document('Customer Details',b[0][0])
                l.customer_name=m[0]
		l.customer_email=m[1]
		l.phone_number=number[1:-1]
                l.save()
                webnotes.conn.commit()
		m = Document('Customer Data')
		m.serial_no=bsrn
                m.warranty_start_on=nowdate()
		m.vehical_make=vm
		m.vehical_age=un
		m.unit_no=va
		m.item=itemm[0][0]
		m.capacitor_serial_no=csrn
		m.warranty_end_on=add_months(cstr(nowdate()),cint(ress[0][0]))
		m.parent=l.name
                m.parenttype='Customer Details'
                m.parentfield='customer_data'
		#webnotes.errprint(m.item)
		#webnotes.errprint(add_months(cstr(nowdate()),cint(ress[0][0])))
	        m.save(new=1)
                webnotes.conn.commit()
	else:
                l = Document('Customer Details')
                l.customer_name=m[0]
                l.customer_email=m[1]
                l.phone_number=number[1:-1]
                l.save(new=1)
                webnotes.conn.commit()
                m = Document('Customer Data')
                m.serial_no=bsrn
                m.warranty_start_on=nowdate()
	        m.warranty_end_on=add_months(cstr(nowdate()),cint(ress[0][0]))
		m.item=itemm[0][0]
                m.vehical_make=vm
                m.vehical_age=un
                m.unit_no=va
		m.capacitor_serial_no=csrn
                m.parent=l.name
                m.parenttype='Customer Details'
                m.parentfield='customer_data'
                m.save(new=1)
                webnotes.conn.commit()
        import requests
	from webnotes.model.code import get_obj
	msg="Dear Customer, welcome to PowerCap You have purchased the battery with serail no. '"+bsrn+"' today, your warrenty will expire on 29/09/2015, \n Regards,\n PowerCap"	
	#msg1=msg.split(",")
	#return msg
	#number='9890865260'
	number1=number[1:-1]
	webnotes.errprint(number1)
	nos=[]
	nos.append(number1)
	webnotes.errprint(nos)
	get_obj('SMS Control', 'SMS Control').send_sms(nos, cstr(msg))
        login =[]
        invObj={}
	invObj['status']='200'
	invObj['message']='Updated the record'
        return invObj


@webnotes.whitelist(allow_guest=True)
def create_subfranchise(auth_key,name,address,map_location,mobile_number,email_id,datetime,version,_type='POST'):
	login =[]
	loginObj = {}
	if len(auth_key[1:-1])<=0 or len(name[1:-1])<=0 or len(address[1:-1])<=0:
		loginObj['status']='401'
		loginObj['error']='Incomplete data to create sub- franchise, Please provide token no,name and address'
		return loginObj	
	qr="select name from `tabauth keys` where auth_key="+auth_key
	res=webnotes.conn.sql(qr)
	if res:
          zz=webnotes.conn.sql("select name from `tabSub Franchise` where name='"+name[1:-1]+"'")
	  if zz:
                key={}
                key['subfranchise_id']=zz and zz[0][0] or ''
                login.append(key)
                loginObj['status']='200'
                loginObj['subfranchise']=login
                return loginObj
           
          else:
	        str='sent '
	        from webnotes.utils.email_lib import sendmail
	        import json,requests
	        url="http://maps.googleapis.com/maps/api/geocode/json?address="+address+"&sensor=true"
	        #return url
	        #webnotes.errprint(url)
	        r = requests.get(url)
	        data = json.loads(r.text)
	        #return data
	        e=''
	        sts=data['status']
		if sts=='OK':
			a=data['results']
		        b=a[0]
		        c=b['geometry']
		        e=c['location']


		rig="select region from `tabFranchise` where contact_email='"+res[0][0]+"' order by creation desc limit 1"
		rgn=webnotes.conn.sql(rig)
		from webnotes.model.doc import Document
		d = Document('Sub Franchise')
		d.sf_name=name[1:-1]
		d.creation=datetime[1:-1]
		d.region=rgn and rgn[0][0] or ''
		d.address=address[1:-1]
		if len(e)>1:
			d.lat=e['lat']
			d.lon=e['lng']
		if len(email_id)>3:
			d.email=email_id[1:-1]
		if len(mobile_number)>3:
			d.c_number=mobile_number[1:-1]
		d.save()
		key={}
		key['subfranchise_id']=d.name
		login.append(key)
		loginObj['status']='200'
		loginObj['subfranchise']=login
		return loginObj
	else:
		loginObj['status']='401'
		return loginObj



@webnotes.whitelist(allow_guest=True)
def create_subfranchise1(auth_key,name,address,map_location,mobile_number,email_id,datetime,version,_type='POST'):
        login =[]
        loginObj = {}
        if len(auth_key[1:-1])<=0 or len(name[1:-1])<=0 or len(address[1:-1])<=0:
                loginObj['status']='401'
                loginObj['error']='Incomplete data to create sub- franchise, Please provide token no,name and address'
                return loginObj
        qr="select name from `tabauth keys` where auth_key="+auth_key
        res=webnotes.conn.sql(qr)
        if res:
          zz=webnotes.conn.sql("select name from `tabSub Franchise` where name='"+name[1:-1]+"'")
          if zz:
                key={}
                key['subfranchise_id']=zz and zz[0][0] or ''
                login.append(key)
                loginObj['status']='200'
                loginObj['subfranchise']=login
                return loginObj

          else:
                str='sent '
                from webnotes.utils.email_lib import sendmail
                import json,requests
                url="http://maps.googleapis.com/maps/api/geocode/json?address="+address+"&sensor=true"
                #return url
                #webnotes.errprint(url)
                r = requests.get(url)
                data = json.loads(r.text)
                #return data
                e=''
                sts=data['status']
                if sts=='OK':
                        a=data['results']
                        b=a[0]
                        c=b['geometry']
                        e=c['location']
                rig="select region from `tabFranchise` where contact_email='"+res[0][0]+"' order by creation desc limit 1"
                rgn=webnotes.conn.sql(rig)
                from webnotes.model.doc import Document
                d = Document('Sub Franchise')
                d.sf_name=name[1:-1]
                d.creation=datetime[1:-1]
                d.region=rgn and rgn[0][0] or ''
                d.address=address[1:-1]
                if len(e)>1:
                        d.lat=e['lat']
                        d.lon=e['lng']
                if len(email_id)>3:
                        d.email=email_id[1:-1]
                if len(mobile_number)>3:
                        d.c_number=mobile_number[1:-1]
                d.save()
        	d1 = Document('Customer')
                d1.customer_name=name[1:-1]+'-'+mobile_number[1:-1]
		d1.territory=''
		d1.account_id=''
                d1.sf_name=''
		d1.customer_type='Company'
		d1.customer_group='Commercial'
                d1.company='PowerCap'
                d1.save(new=1)
		if cint(webnotes.defaults.get_global_default("auto_accounting_for_stock")):
                   if not webnotes.conn.get_value("Account", {"master_type": "Customer","master_name": d1.name}) and not webnotes.conn.get_value("Account", {"master_name": d1.name}):
                         if not webnotes.conn.get_value("Stock Ledger Entry", {"Warehouse": d1.name}):
                                ac_bean = webnotes.bean({
                                       	"doctype": "Account",
                                        'account_name': d1.name,
                                        'parent_account': "Accounts Receivable - P",
                                        'group_or_ledger':'Ledger',
					'debit_or_credit':'Debit',
                                        'company':"PowerCap",
                                        "master_type": "Customer",
                                        "master_name": d1.name,
					"freeze_account": "No"
                               	})
                               	ac_bean.ignore_permissions = True
                               	ac_bean.insert()
		webnotes.conn.commit()
                key={}
                key['subfranchise_id']=d.name
                login.append(key)
                loginObj['status']='200'
                loginObj['subfranchise']=login
                return loginObj
        else:
                loginObj['status']='401'
                return loginObj


@webnotes.whitelist(allow_guest=True)
def create_customer1(auth_key,name,mobile_number,email_id,datetime,version,_type='POST'):
        login =[]
        loginObj = {}
        qr="select name from `tabauth keys` where auth_key="+auth_key
        res=webnotes.conn.sql(qr)
        if res:
                qr1="select name from `tabCustomer Details` where customer_name="+name+" and phone_number="+mobile_number
                rs=webnotes.conn.sql(qr1)
                if rs :
                        key={}
                        key['customer_id']=rs[0][0]
                        login.append(key)
                        loginObj['status']='200'
                        loginObj['customer']=login

                        return loginObj
                else :
                        from webnotes.model.doc import Document
                        d = Document('Customer Details')
                        if len(name)>3:
                                d.customer_name=name[1:-1]
                        if len(email_id)>3:
                                d.customer_email=email_id[1:-1]
                        if len(mobile_number)>3:
                                d.phone_number=mobile_number[1:-1]
                        d.save()
                        d1 = Document('Customer')
                        d1.customer_name=name[1:-1]+'-'+mobile_number[1:-1]
			d1.territory=''
			d1.account_id=''
                        d1.sf_name=''
			d1.customer_type='Company'
			d1.customer_group='Commercial'
                        d1.company='PowerCap'
                        d1.save(new=1)
			if cint(webnotes.defaults.get_global_default("auto_accounting_for_stock")):
                          if not webnotes.conn.get_value("Account", {"master_type": "Customer","master_name": d1.name}) and not 		webnotes.conn.get_value("Account", {"master_name": d1.name}):
                                if not webnotes.conn.get_value("Stock Ledger Entry", {"Warehouse": d1.name}):
                                                ac_bean = webnotes.bean({
                                                	"doctype": "Account",
	                                                'account_name': d1.name,
	                                                'parent_account': "Accounts Receivable - P",
	                                                'group_or_ledger':'Ledger',
							'debit_or_credit':'Debit',
	                                                'company':"PowerCap",
	                                                "master_type": "Customer",
	                                                "master_name": d1.name,
							"freeze_account": "No"
                                        	})
                                        	ac_bean.ignore_permissions = True
                                        	ac_bean.insert()
                        webnotes.conn.commit()
                        key={}
                        key['customer_id']=d.name
                        login.append(key)
                        loginObj['status']='200'
                        loginObj['customer']=login
                        return loginObj
        else:
                loginObj['status']='401'
                return loginObj

@webnotes.whitelist(allow_guest=True)
def item_details(auth_key,creation):
	#return "hello"
	login =[]
	invObj={}
	qr="select name from `tabauth keys` where auth_key="+auth_key
	res=webnotes.conn.sql(qr)
	if res:
	    qry="select item_code,item_name,ref_rate from `tabItem Price` where selling=1 and price_list='Standard Selling' and creation>='"+creation[1:-1]+"'"
	    rss=webnotes.conn.sql(qry,as_dict=1)
	    #return rss
	    inv=[]
    	    if rss:
		for item_data in rss:
			inv.append({"item_code":item_data['item_code'],"item_name":item_data['item_name'],"ref_rate":item_data['ref_rate']})
		invObj['status']='200'
		invObj['item_details']=inv
		return invObj
            else:
		invObj['status']='200'
		invObj['item_details']=[]
		return invObj
	else:
          invObj['status']='401'
	  invObj['error']='Invalid Auth Key'
	  return invObj

@webnotes.whitelist(allow_guest=True)
def create_in(data,_type='POST'):
	from webnotes.model.doc import Document
	from webnotes.utils import nowdate,add_months
        data1=json.loads(data)	
        auth_key=data1['token']
        invoice_type=data1['invoice_type']
        customer=data1['customer']
        dattime=data1['datetime']
        item_details=data1['item_details']
        login =[]
        loginObj = {}
	amt=0
        qt=0
        srl=''
        cc=''
        zz=''
	#return data
        if len(auth_key[1:-1]) <=0 or len(dattime[1:-1]) <=0 or len(customer[1:-1])<=0 :
                loginObj['status']='401'
                loginObj['error']='Incomplete data to generate Sales Invoice , Please provide token no , Datetime,customer and serial no'
                return loginObj
 	
        for ff in item_details:
                   a=ff['barcode']
                   c="select item_code,warehouse from `tabSerial No` where name='"+a[:-1]+"'"
                   cc=webnotes.conn.sql(c)
		   #webnotes.errprint(c)
		   #webnotes.errprint(cc)
                   amt=cint(amt)+cint(ff['rate'])
                   qt+=1
                   srl+=a[:-2].replace(',','\n')
		   #return cc
                   if cc :
			qr="select name from `tabauth keys` where auth_key='"+auth_key+"'"
			#return qr
			res=webnotes.conn.sql(qr)
			if res :
		           rr="select region from `tabFranchise` where contact_email='"+res[0][0]+"'"
                           r1=webnotes.conn.sql(rr)
			   if r1[0][0]==cc[0][1] :
				#webnotes.errprint("same")
				pass
			   else:
				#webnotes.errprint("different warehouse")
				pass
				
                        zz+="'"+a[:-1].replace(',','')+"',"
                   else:
                   	if invoice_type=='CUSTOMER':
				l = Document('Customer Details',customer)
		                l.customer_name=customer
		                l.save()
		                webnotes.conn.commit()
				for ll in item_details:
				   m = Document('Customer Data')
				   m.serial_no=a[:-1]
		                   m.parent=l.name
		                   m.parenttype='Customer Details'
		                   m.parentfield='customer_data'
			           m.save(new=1)
				   webnotes.conn.commit()			
			qrt="select name from `tabauth keys` where auth_key='"+auth_key+"'"
		        res=webnotes.conn.sql(qrt)
        		net=0
		        if res:
                		a="select name from tabCustomer where name='"+customer+"'"
		                b=webnotes.conn.sql(a)
		                if b:
		                        a=''
		                else:
                		        d = Document('Customer')
                		        d.customer_name=customer
		                        d.name=customer
                		        d.save(new=1)
                		        webnotes.conn.commit()
               		qr="select name from `tabauth keys` where auth_key='"+auth_key+"'"
               		#webnotes.errprint(qr)
			res=webnotes.conn.sql(qr)
			rgn=''
			if res :
		           rr="select region from `tabFranchise` where contact_email='"+res[0][0]+"'"
		           #webnotes.errprint(qr)
                           r1=webnotes.conn.sql(rr,as_list=1)
                           #webnotes.errprint(r1[0][0])			   
                	d = Document('Sales Invoice')
	                d.customer=customer
	                d.customer_name=customer
        	        d.posting_date=dattime[1:-1]
        	        d.due_date=dattime[1:-1]
        	        d.remarks='Invalid QR code'
        	        d.selling_price_list='Standard Selling'
        	        d.currency='INR'
        	        if r1:
        	        	d.territory=r1[0][0]
        	        	d.region=r1[0][0]
        	        d.net_total_export=0
        	        d.grand_total_export=0
        	        d.rounded_total_export=0
        	        d.plc_conversion_rate=1			
        	        from webnotes.utils import nowdate
        	        from accounts.utils import get_fiscal_year
        	        today = nowdate()
        	        d.fiscal_year=get_fiscal_year(today)[0]
        	        d.debit_to=customer[1:-1]+" - P"
        	        d.is_pos=1
        	        d.cash_bank_account='Cash - P'
        	        d.docstatus=1
        	        d.save(new=1)
        	        webnotes.conn.commit()
        	        e=Document('Sales Invoice Item')
		        e.description="Invalid QR code"
		        e.qty='1'
		        e.stock_uom='Nos'
		        e.serial_no_=a[:-1]
		        e.parent=d.name
		        e.parenttype='Sales Invoice'
		        e.parentfield='entries'
		        e.save(new=1)        	        	        
        	        webnotes.conn.commit()
        	        key={}
        	        key['invoice_id']=d.name
        	        login.append(key)
        	        loginObj['status']='200'
        	        loginObj['invoice']=login
        	        return loginObj
                        #loginObj['status']='400'
                        #loginObj['error']='invalid serial no (QR Code) please contact administrator'
                        #return loginObj
        z=zz[:-1]
	u="select distinct item_code from `tabSerial No` where name in ("+z+")"
	s=webnotes.conn.sql(u,as_list=1)
	qty_dict={}
	rate_dict={}
	srl_dict={}
        for key in s:
		qty_dict.setdefault(key[0],0)
		rate_dict.setdefault(key[0],0)  
		srl_dict.setdefault(key[0],'')
        for sss in item_details:
		a=sss['barcode']
                c="select item_code from `tabSerial No` where name='"+a[:-1]+"'"
                cc=webnotes.conn.sql(c)
		d=cc and cc[0][0] or ''
		qty_dict[d]=cint(qty_dict[d])+1
		rate_dict[d]=cint(rate_dict[d])+cint(sss['rate'])
                srl_dict[d]=srl_dict[d]+a[:-1]+"\n"
        if invoice_type=='CUSTOMER':
            	#a="select name from `tabCustomer Details`where name like '"+customer+"-%'"
            	#b=webnotes.conn.sql(a)               
	    	#webnotes.errprint(a)
            	#if b:
                #a=''
            	#else:
		#webnotes.errprint("else "+a)
		l = Document('Customer Details',customer)
                l.customer_name=customer
                l.save()
                webnotes.conn.commit()
		for ll in item_details:
		   m = Document('Customer Data')
		   #.serial_no=ll['barcode']
		   #webnotes.errprint(a[:-1])
	           m.serial_no=a[:-1]
                   #m.start_date=nowdate()
		   m.parent=l.name
                   m.parenttype='Customer Details'
                   m.parentfield='customer_data'
	           m.save(new=1)
		   #webnotes.errprint("before g1")
		   g1="update `tabSerial No` set warehouse='',delivery_date=CURDATE(),status='Delivered',customer='"+customer+"' where name='"+cstr(ll['barcode']).replace(',','')+"'"
                   webnotes.conn.sql(g1)
                   webnotes.conn.commit()
	else:
		for gg in item_details:
		   g=gg['barcode']
	           #webnotes.errprint("in else gg")
		   #webnotes.errprint(g[:-2])
                   g1="update `tabSerial No` set warehouse='',delivery_date=CURDATE(),status='Delivered',customer='"+customer+"' where name='"+g[:-1]+"'"
                   webnotes.conn.sql(g1)
                   webnotes.conn.commit()
	for hh in item_details:
		   h=hh['barcode']
		   g=h[:-2] 
                   i="select item_code from `tabSerial No` where name='"+g+"'"
                   ii=webnotes.conn.sql(i)
        qrt="select name from `tabauth keys` where auth_key='"+auth_key+"'"
        res=webnotes.conn.sql(qrt)
        net=0
        if res:
                a="select name from tabCustomer where name='"+customer+"'"
                #webnotes.errprint(a)
                b=webnotes.conn.sql(a)
                #webnotes.errprint(b)                
                if b:
                        a=''
                else:
                        #webnotes.errprint("else")
                        d = Document('Customer')
                        d.customer_name=customer
                        d.name=customer
                        d.save(new=1)
                        webnotes.conn.commit()
                d = Document('Sales Invoice')
                d.customer=customer
                d.customer_name=customer
                d.posting_date=dattime[1:-1]
                d.due_date=dattime[1:-1]
                d.selling_price_list='Standard Selling'
                d.currency='INR'
                d.territory=r1[0][0]
                d.net_total_export=0
                d.grand_total_export=0
                d.rounded_total_export=0
                d.plc_conversion_rate=1
		d.region=r1[0][0]
                from webnotes.utils import nowdate
                from accounts.utils import get_fiscal_year
                today = nowdate()
                d.fiscal_year=get_fiscal_year(today)[0]
                d.debit_to=customer[1:-1]+" - P"
                d.is_pos=1
                d.cash_bank_account='Cash - P'
                d.save(new=1)
                webnotes.conn.commit()
                for x in qty_dict.keys():
	                e=Document('Sales Invoice Item')
	                e.item_code=x
	                e.item_name=x
	                e.description=x
	                e.qty=qty_dict[x]
	                e.stock_uom='Nos'
	                e.ref_rate=cint(rate_dict[x])/cint(qty_dict[x])
	                e.export_rate=cint(rate_dict[x])/cint(qty_dict[x])
	                e.export_amount=cint(rate_dict[x])
	                e.income_account='Sales - P'
	                e.cost_center='Main - P'
	                e.serial_no_=srl_dict[x]
	                e.parent=d.name
	                e.parenttype='Sales Invoice'
	                e.parentfield='entries'
	                e.save(new=1)
                        net+=cint(rate_dict[x])
			qrs="select warranty_period from tabItem where name='"+x+"'"
			#webnotes.errprint(qrs)
	 		ress=webnotes.conn.sql(qrs)
	 		#webnotes.errprint(ress[0][0])
	 		if ress:
	 			exdt=add_months(cstr(nowdate()),cint(ress[0][0]))
	 		else:
	 			exdt='null'
	 		#webnotes.errprint(cstr(srl_dict[x]))
			#webnotes.errprint(g)
			g2="update `tabSerial No` set warehouse='', warranty_expiry_date='"+cstr(exdt)+"',delivery_date=CURDATE(),status='Delivered',customer='"+customer+"' where name='"+cstr(h[:-1])+"'"
		 	#webnotes.errprint(g2)
			#webnotes.errprint("in x in qty dict")
                        webnotes.conn.sql(g2)
	                webnotes.conn.commit()
                d = Document('Sales Invoice',d.name)
                d.net_total_export=net
		d.net_total=net
                d.grand_total_export=net
                d.rounded_total_export=net
                d.outstanding_amount=net
		d.docstatus=1
                d.save()
                webnotes.conn.commit()
                key={}
                key['invoice_id']=d.name
                login.append(key)
                loginObj['status']='200'
                loginObj['invoice']=login
                return loginObj
        else:
                loginObj['status']='401'
                loginObj['error']='invalid token please contact administrator'
                return loginObj  
