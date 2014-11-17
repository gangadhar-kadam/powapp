

# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes import msgprint, _
from webnotes.utils import cstr, cint, flt, comma_or, nowdate, get_base_path,today,add_months
import os

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl
  
        def validate(self):
            import requests
            from webnotes.model.code import get_obj
            msg="send sms from packing item "
            #return msg
            #webnotes.errprint(number)
            nos=['9890865260']  
 	    #get_obj('SMS Control', 'SMS Control').send_sms(nos, cstr(msg))

            i=0
            import re
            for m in re.finditer(r"\n", self.doc.serial_no):
                i+=1
            #webnotes.msgprint(i)
            #webnotes.msgprint(self.doc.quantity)
            if i != self.doc.quantity :
               webnotes.msgprint("Sorry! the quantity and no of barcodes does not match..!",raise_exception=1)
               raise Exception, ""
	def on_update(self):
		#ebnotes.errprint("s")
		#ebnotes.errprint(self.doc.name)
		s='232242342'
		s=self.doc.name
                #ebnotes.errprint(s)
		import barcode
                from barcode.writer import ImageWriter
                ean = barcode.get('code39',s, writer=ImageWriter())
                path = os.path.join(get_base_path(), "public", "barcode_img")+"/"+s
                filename = ean.save(path)
                barcode_img = '<html>\
                        <table>\
                                  <tr>\
                                          <td >\
                                                  <img src="'"../barcode_img/"+s+".png"'" width="300px">\
                                          </td>\
                                  </tr>\
                          </table>\
                  </html>'
                self.doc.barcode_image = barcode_img
                #self.doc.img_dtl="<img src='../barcode_img/zzz.png' alt='Smiley face' height='80' width='300'>".replace('zzz',self.doc.name)
                self.doc.save()

        def on_submit(self):
		serial_nos = self.get_serial_nos(self.doc.serial_no)
                for serial_no in serial_nos:
	            self.make_serial_no(serial_no)
                from accounts.general_ledger import make_gl_entries
                self.sle() 

        def sle(self):
                make_bin=[]
		qry="select sum(actual_qty) from `tabStock Ledger Entry` where item_code='"+self.doc.item+"' and warehouse='Finished Goods - P'"	          
                #ebnotes.errprint(qry)
	        w3=webnotes.conn.sql(qry)
	        qty_after_transaction=cstr(cint(w3[0][0])+cint(self.doc.quantity))
	        actual_qty=self.doc.quantity
                import time
	        tim=time.strftime("%X")	   
                from webnotes.model.doc import Document     
		d = Document('Stock Ledger Entry')
		d.item_code=self.doc.item
		d.batch_no=self.doc.name
		d.stock_uom='Nos'
		d.warehouse='Finished Goods - P'
		d.actual_qty=actual_qty
		d.posting_date=today()
		d.posting_time=tim
                d.voucher_type='Purchase Receipt'
                d.serial_no=self.doc.serial_no.replace('\n','')
		d.qty_after_transaction=qty_after_transaction
		d.is_cancelled = 'No'
                d.company='PowerCap'
		d.docstatus = 1;
		d.name = 'Batch wise item updation'
		d.owner = webnotes.session['user']
		d.fields['__islocal'] = 1 
		d.save(new=1)
                make_bin.append({
                       "doctype": 'b',
                       "sle_id":d.name,
                       "item_code": self.doc.item,
		       			"warehouse": 'Finished Goods - P',
		       			"actual_qty": actual_qty 
		       			
		       })

        def get_serial_nos(self,serial_no):
	   return [s.strip() for s in cstr(serial_no).strip().upper().replace(',', '\n').split('\n') 
		if s.strip()]

        def make_serial_no(self,serial_no):
	 sr = webnotes.new_bean("Serial No")
	 sr.doc.serial_no = serial_no
	 sr.doc.item_code = self.doc.item
	 sr.make_controller().via_stock_ledger = True
	 sr.insert()
	 sr.doc.warehouse = 'Finished Goods - P'
	 sr.doc.status = "Available"
	 sr.doc.purchase_document_type = 'Packing Items'
	 sr.doc.purchase_document_no = self.doc.name
	 sr.doc.purchase_date = self.doc.creation
	 sr.save()
	 qr="select warranty_period from tabItem where name='"+self.doc.item+"'"
	 res=webnotes.conn.sql(qr)
	 if res:
	 	exdt=add_months(cstr(nowdate()),cint(res[0][0]))
	 	qr1="update `tabSerial No` set warranty_expiry_date='"+cstr(exdt)+"' where name='"+sr.doc.name+"'"
	 	webnotes.conn.sql(qr1) 
	 webnotes.msgprint(_("Serial No created") + ": " + sr.doc.name)
	 return sr.doc.name
