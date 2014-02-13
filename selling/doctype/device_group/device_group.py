# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes import msgprint, _
from webnotes.utils import cint,cstr

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def autoname(self):
		if self.doc.account_id and self.doc.group_id:
                       	self.doc.name = self.doc.account_id+"_"+self.doc.group_id
                else:
			msgprint("Please Create Device Group",raise_exception=1)

	def on_update(self):	
		self.doc.account_id=self.doc.account_id.lower()
		self.doc.group_id=self.doc.group_id.lower()
		self.doc.name=self.doc.name.lower()

		self.doc.group_id=self.doc.name
		#if self.doc.account_id:
		#a=webnotes.conn.sql("select account_id from `tabFranchise`")
		
		qry= "insert into DeviceGroup (accountID,groupID) values ('"+cstr(self.doc.account_id)+"','"+cstr(self.doc.group_id)+"')"
		webnotes.conn.sql(qry)
		webnotes.errprint(qry)
		#else:
		#	pass
