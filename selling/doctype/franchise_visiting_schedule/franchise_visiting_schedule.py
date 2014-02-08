# Copyright (c) 2014, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.model.doc import Document
from webnotes.utils import get_last_day, getdate, add_days
from webnotes.utils import flt, cstr
import datetime

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl
	
	def on_update(self):
		#webnotes.errprint("Hiii...")
		a=webnotes.conn.sql("select device_id from tabVehicle where account_id='"+self.doc.account_id+"'")
                #webnotes.errprint(a)
                self.doc.device_id = a
                ss=self.get_sub_franchise()
                b=self.get_date_details()
                self.generate_visiting_schedule(b,ss,a[0][0])
		return ("hi")
        def get_sub_franchise(self):
                s=webnotes.conn.sql("select sf_name from `tabSub Franchise Name` where parent='"+self.doc.route+"'", as_list=1)
                #webnotes.errprint(s)
                return s

        def get_date_details(self):
		bb=get_last_day(self.doc.start_date)
                #webnotes.errprint(bb)
                return bb

        def generate_visiting_schedule(self,bb,s,a):
		d = datetime.date.today()
		n="delete from `tabSub Franchise Visiting Schedule` where account_id='"+cstr(self.doc.account_id)+"' and route='"+cstr(self.doc.route)+"' and visiting_date between '"+cstr(d)+"' and '"+cstr(bb)+"'"
		webnotes.conn.sql(n)
		webnotes.errprint(n)
                if self.doc.visiting_frequency=='Daily':
                        m = 1
			j=  31
                elif self.doc.visiting_frequency=='Weekely':
                        m = 7
                        j= 5
                elif self.doc.visiting_frequency=='15 Days':
                        m = 15
			j=2
                list1 = []
		list1.append(self.doc.start_date)
		dt=self.doc.start_date
		for j in range (0,j):
                	date=add_days(getdate(dt),m)
			#webnotes.errprint(self.doc.start_date)
			webnotes.errprint(date)
                	if date <= bb:
                        	list1.append(date)
			dt=date
		#webnotes.errprint(self.doc.start_date)
		#webnotes.errprint(bb)
		#webnotes.errprint(list1)
                for ls in s:
                        for i in range(len(list1)):
				#webnotes.errprint(list1[i])
				#webnotes.errprint(a)
                                d=Document('Sub Franchise Visiting Schedule')
                                d.account_id=self.doc.account_id
                                d.device_id=a
                                d.sf_name=ls[0]
				d.route=self.doc.route
				webnotes.errprint(d.route)
                                d.visiting_date=list1[i]
				d.save(new=1)
		return ("Welcome..")

	#def get_records(self):
		#self.doc.device_id = a
        	#ss=self.get_sub_franchise()
        	#b=self.get_date_details()
        	#self.generate_visiting_schedule(b,ss,a[0][0])
