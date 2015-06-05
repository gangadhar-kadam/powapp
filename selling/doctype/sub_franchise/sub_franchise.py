# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.utils import cint, cstr,validate_email_add
from webnotes.model.doc import Document
from webnotes import msgprint, _
import re

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl


	def validate(self):
		if self.doc.fields.get('__islocal') or not self.doc.name:
			adr=webnotes.conn.sql("select name from `tabSub Franchise` where address='"+self.doc.address+"'")
			if adr :
				#webnotes.msgprint("Address Already exist for another Sub-franchise...",raise_exception=1)
				pass
			
			lt=self.doc.lat
			ln=self.doc.lon
			acnt="select account_id from tabFranchise where region='"+self.doc.region+"'"
			ecn=webnotes.conn.sql(acnt)
			#webnotes.errprint(ecn)
			ac=ecn and ecn[0][0] or ''	
			#ac=self.doc.account_id
			qry="SELECT MBRContains(( SELECT GeomFromText(concat('Polygon((', latitude1,' ' ,longitude1,' ,',latitude2,' ' ,longitude2 , ' , ',latitude3,' ' ,longitude3 ,' , ',latitude4,' ' ,longitude4 ,' , ',latitude5,' ' , longitude5 ,' , ',latitude6,' ' ,longitude6 ,' , ',latitude7,' ' ,longitude7 ,' , ',latitude8, ' ' ,longitude8 ,' , ',latitude9,' ' ,longitude9 ,' , ',latitude10,' ' ,longitude10,' , ', latitude1,' ' ,longitude1 ,'))')) AS t FROM Geozone WHERE accountID = 'sysadmin' and geozoneID='"+cstr(self.doc.region)+"' order by lastUpdateTime desc limit 1 ),GeomFromText('Point("+cstr(lt)+" "+cstr(ln)+")'));"
			#qry="SELECT MBRContains(( SELECT GeomFromText(concat('Polygon((', latitude1,' ' ,longitude1,' ,',latitude2,' ' ,longitude2 , ' , ',latitude3,' ' ,longitude3 ,' , ',latitude4,' ' ,longitude4 ,' , ',latitude5,' ' , longitude5 ,' , ',latitude6,' ' ,longitude6 ,' , ',latitude7,' ' ,longitude7 ,' , ',latitude8, ' ' ,longitude8 ,' , ',latitude9,' ' ,longitude9 ,' , ',latitude10,' ' ,longitude10,' , ', latitude1,' ' ,longitude1 ,'))')) AS t FROM Geozone WHERE accountID = '"+cstr(ac)+"'),GeomFromText('Point("+cstr(lt)+" "+cstr(ln)+")'));"
			#webnotes.errprint(qry)
			rs=webnotes.conn.sql(qry)
			#webnotes.errprint(rs[0][0])
			if rs[0][0]==0:
				
				#webnotes.msgprint("Sorry ! the select sub-franchiese address does not included in your area.",raise_exception=1)
				pass
		
		#Contact Name
		n1=self.doc.c_name
                if n1:
                        if n1.isalpha():
                                pass
                        else:
                                webnotes.msgprint("Please enter only letters in contact name",raise_exception=1)
		#Cont Name
		cn=self.doc.c_number
                if cn:
                        if cn.isdigit() and len(cn)>9 and len(cn)<13:
                                pass
                        else:
                                msgprint("Please enter valid contact number",raise_exception=1)
		#Account No
		acc=self.doc.account_number
                if acc :
                        if len(acc)>8 and len(acc)<16 and acc.isdigit() :
                                pass    
                        else:
                                msgprint("Please enter min 9 digids Account Number",raise_exception=1)
		#Branch name
		br_name=self.doc.branch_name
                if br_name:
                        if br_name.isalpha():
                                pass    
                        else:
                                msgprint("Please Enter only characters in Branch name",raise_exception=1)
		#Bank IFSC Code
		ifsc=self.doc.bank_ifsc_code
                if ifsc:
                        if ifsc.isdigit() and len(ifsc)>5 and len(ifsc)<12:
                                pass    
                        else:
				pass
		#Contact Name
		n1=self.doc.c_name
                if n1:
                        #if n1.isalpha():
			import re
			if re.match(r'^[a-zA-Z][ A-Za-z_-]*$', n1):
                                pass
                        else:
                                webnotes.msgprint("Please enter only letters in contact name",raise_exception=1)
		#Cont Name
		cn=self.doc.c_number
                if cn:
                        if cn.isdigit() and len(cn)>9 and len(cn)<13:
                                pass
                        else:
                                msgprint("Please enter valid contact number",raise_exception=1)
		#Account No
		acc=self.doc.account_number
                if acc :
			#webnotes.errprint(len(acc))
			#webnotes.errprint("length")
                        if len(acc)>8 and len(acc)<17 and acc.isdigit() :
                                pass    
                        else:
                                msgprint("Please enter valid(min.9 and max.16 digits) Account Number",raise_exception=1)
		#Branch name
		br_name=self.doc.branch_name
                if br_name:
                        if re.match(r'^[a-zA-Z][ A-Za-z_-]*$', br_name):
                                pass    
                        else:
                                msgprint("Please Enter only characters in Branch name",raise_exception=1)
		#Bank IFSC Code
		ifsc=self.doc.bank_ifsc_code
                if ifsc:
                        if ifsc.isdigit() and len(ifsc)>5 and len(ifsc)<12:
                                pass    
                        else:
                                msgprint("Please enter min 6 digits IFSC Code",raise_exception=1)

	
	def on_update(self):
		#res="select account_id from `tabFranchise` where region='"+self.doc.region+"'"
		#rs=webnotes.conn.sql(res)
        	#webnotes.errprint(rs)
		#self.doc.account_id=rs[0][0]
		#webnotes.errprint(self.doc.account_id)
		#self.doc.save()
                s=webnotes.conn.sql("select customer_name from `tabCustomer` where territory='"+cstr(self.doc.region)+"' and name='"+self.doc.name+"'")
                #webnotes.errprint(s)
                if not s:
                        d = Document('Customer')
                        d.customer_name=self.doc.sf_name
                        d.territory=self.doc.region
                        d.account_id=self.doc.account_id
                        d.sf_name=self.doc.sf_name
                        d.customer_type='Company'
                        d.customer_group='Commercial'
