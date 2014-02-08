# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.utils import flt, cstr
from webnotes.utils import get_last_day, todate

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def on_update(self):
		webnotes.errprint("Hiii...")
		a=webnotes.conn.sql("select device_id from tabVehicle where account_id='"+self.doc.account_id+"'")
		webnotes.errprint(a)
		self.doc.device_id = a
		ss=get_sub_franchise()
		b=get_date_details()
		self.generate_visiting_schedule(b,ss)
	def get_sub_franchise(self):
		s=webnotes.conn.sql("select sf_name from `tabSub Franchise Name` where parent='"+self.doc.route+"'", as_list=1)
		webnotes.errprint(s)
		return s

	def get_date_details(self):
		bb=get_last_day(self.doc.start_date)
		webnotes.errprint(bb)
		return bb

	def generate_visiting_schedule(self,bb,s):
		
		if self.doc.visiting_frequency=='Daily':
			m = 1
		elif self.doc.visiting_frequency=='Weekely':
			n = 7
		elif self.doc.visiting_frequency=='15 Days':
			p= 15
		list1 = []
		date=add_days(todate(self.doc.start_date),m)
		if date < bb:
			list1.append(date)
		for ls in s:
			for l in list1:
				d=Document('Sub Franchise Visiting Schedule')
                        	d.account_id=self.doc.account_id
                        	d.device_id=self.doc.device_id
				d.sf_name=ls
				d.visiting_date=l
				d.save()
	


	
