# Copyright (c) 2014, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.model.doc import Document
from webnotes.utils import get_last_day, getdate, add_days
from webnotes.utils import flt, cstr, cint
import datetime
from webnotes import msgprint, _

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl
	
	def on_update(self):
		k=webnotes.conn.sql("select account_id from `tabFranchise` where region='"+cstr(self.doc.regions)+"'")
		a=webnotes.conn.sql("select device_id from `tabFranchise` where region='"+cstr(self.doc.regions)+"'")
	        self.doc.device_id = a
	        ss=self.get_sub_franchise()
	        b=self.get_date_details()
	        self.generate_visiting_schedule(b,ss,a[0][0],k[0][0])
		return ("hi")

	def get_sub_franchise(self):
		s=webnotes.conn.sql("select sf_name from `tabSub Franchise` where region='"+cstr(self.doc.regions)+"'",as_list=1)
		if s:
		        return s
		else:
			msgprint(_("Sub-franchise is not created for this region.Please create sub-franchise first.."),
				raise_exception=True)

	def get_date_details(self):
		bb=get_last_day(self.doc.start_date)
	        return bb

	def generate_visiting_schedule(self,bb,s,a,k):
		j=0
		d = datetime.date.today()
	        if self.doc.visiting_frequency=='Weekely':
		        m = 7
			j = 4 * cint(self.doc.frequency)
	       	elif self.doc.visiting_frequency=='Fortnightly':
	       	        m = 15
			j = 2 * cint(self.doc.frequency)
	       	elif self.doc.visiting_frequency=='Monthly':
	       	        m = 30
			j = 1 * cint(self.doc.frequency)
	       	list1 = []
		list1.append(self.doc.start_date)
		dt=self.doc.start_date
		webnotes.errprint(j)
		for j in range(0,j):
	               	for ls in s:
	                       	for i in range(len(list1)):
					webnotes.errprint("generation")
	                       		d=Document('Sub Franchise Visiting Schedule')
	                       		d.account_id=k
					d.region=self.doc.regions
					d.device_id=a
	                       		d.sf_name=ls[0]
					if self.doc.visiting_frequency=='Weekely':
						webnotes.errprint("Weekely")
						d.weekly=self.doc.frequency
					elif self.doc.visiting_frequency=='Fortnightly':
                				webnotes.errprint("Fortnightly")
 						d.forth_nightly=self.doc.frequency
					elif self.doc.visiting_frequency=='Monthly':
						webnotes.errprint("Monthly")
						d.monthly=self.doc.frequency
					d.save(new=1)
		return ("Welcome..")
