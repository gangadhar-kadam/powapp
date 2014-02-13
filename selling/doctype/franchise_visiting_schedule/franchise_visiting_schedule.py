# Copyright (c) 2014, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.model.doc import Document
from webnotes.utils import get_last_day, getdate, add_days
from webnotes.utils import flt, cstr, cint
import datetime

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl
	
	def on_update(self):
		k=webnotes.conn.sql("select account_id from `tabFranchise` where region='"+cstr(self.doc.regions)+"'")
		webnotes.errprint(k)
		#self.doc.account_id=k
		a=webnotes.conn.sql("select device_id from `tabFranchise` where region='"+cstr(self.doc.regions)+"'")
                webnotes.errprint(a)
                self.doc.device_id = a
                ss=self.get_sub_franchise()
                b=self.get_date_details()
                self.generate_visiting_schedule(b,ss,a[0][0],k[0][0])
		return ("hi")
        def get_sub_franchise(self):
		s=webnotes.conn.sql("select sf_name from `tabSub Franchise` where region='"+cstr(self.doc.regions)+"'",as_list=1)
		webnotes.errprint(s)
                return s

        def get_date_details(self):
		bb=get_last_day(self.doc.start_date)
                return bb

        def generate_visiting_schedule(self,bb,s,a,k):
		j=0
		d = datetime.date.today()
		#n="delete from `tabSub Franchise Visiting Schedule` where region='"+cstr(self.doc.regions)+"' and visiting_date between '"+cstr(d)+"' and '"+cstr(bb)+"'"
		#webnotes.conn.sql(n)
		#webnotes.errprint(n)
                if self.doc.visiting_frequency=='Weekely':
                        m = 7
			j = 4 * cint(self.doc.frequency)
			#j=  5
                elif self.doc.visiting_frequency=='Forth Night':
			#webnotes.errprint("hellooo")
                        m = 15
			j = 2 * cint(self.doc.frequency)
                        #j= 2
                elif self.doc.visiting_frequency=='One Month':
                        m = 30
			j = 1 * cint(self.doc.frequency)
			#j=1
		#webnotes.errprint(j)
                list1 = []
		list1.append(self.doc.start_date)
		dt=self.doc.start_date
		#for j in range (0,j):
                #	date=add_days(getdate(dt),m)
		#	webnotes.errprint(date)
                #	if date <= bb:
                #       	list1.append(date)
		#	dt=date
		#webnotes.errprint(self.doc.start_date)
		#webnotes.errprint(bb)
		#webnotes.errprint(list1)
		webnotes.errprint(j)
		for j in range(0,j):
			#webnotes.errprint("hii")
                	for ls in s:
			        #webnotes.errprint("hello")
                        	for i in range(len(list1)):
					#webnotes.errprint(k)
					#webnotes.errprint(list1[i])
                               		d=Document('Sub Franchise Visiting Schedule')
                               		d.account_id=k
					#webnotes.errprint(d.account_id)
					d.region=self.doc.regions
					d.device_id=a
                               		d.sf_name=ls[0]
					#visiting_date=list1[i]
					d.save(new=1)
		return ("Welcome..")


