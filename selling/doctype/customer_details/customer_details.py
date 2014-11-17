# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.model.doc import Document,make_autoname
from webnotes.utils import cint, cstr
from webnotes.model.bean import getlist
from webnotes.utils import getdate, add_days, validate_email_add
from datetime import date, timedelta
import time
from webnotes import msgprint

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

        def autoname(self):
                self.doc.name = self.doc.customer_name+'-'+self.doc.phone_number

	def validate(self):
		#coust name
		cn=self.doc.customer_name
                if cn:
                        if cn.isalpha():
                                pass
                        else:
                                msgprint("Please Enter only Letters in Costomer Name",raise_exception=1)
		#Phone number
		ph=self.doc.phone_number
                if ph:
                        if ph.isdigit() and len(ph)>9 and len(ph)<13 :
                                pass
                        else:
                                msgprint("Please Enter valid phone number",raise_exception=1)

        def on_update(self):
                serial_no_list=[]
                for data in getlist(self.doclist,'customer_data'):
                        serial_no_list.append(data.serial_no)
                if any(serial_no_list.count(x) > 1 for x in serial_no_list)==True:
                        webnotes.msgprint("You have enter duplicate serial number, Please correct",raise_exception=1)
		
		self.validate_email()
		
	def validate_email(self):
                if self.doc.customer_email and not validate_email_add(self.doc.customer_email):
                        webnotes.msgprint("Please enter valid Email...",raise_exception=1)


	def get_details(self,serial_no):
		s=webnotes.conn.sql("select item_name from `tabSerial No` where serial_no='"+serial_no+"'",as_list=1)		
		p=s[0][0]
		self.doc.item_name=p
		a=webnotes.conn.sql("select warranty_period from `tabItem` where item_name='"+cstr(self.doc.item_name)+"'",as_list=1)
		if a:
			from webnotes.utils import get_first_day, get_last_day, add_to_date, nowdate, getdate,add_months
   			today = nowdate()
			date=add_days(today,cint(a[0][0])-1)
			d=m=y=0
			y=int(a[0][0])/12
			m=int(a[0][0])%12
			date1=add_to_date(today,years=y,months=m,days=0)
			webnotes.errprint(date1)
			ret={
			   'warranty_start_on':today,
		           'warranty_end_on':date1
			}
			webnotes.errprint(ret)
			return ret		
		return 'hi'
