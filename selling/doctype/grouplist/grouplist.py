# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.utils import cint, now, cstr

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

#	def on_update(self):
#		a=webnotes.conn.sql("select erp from User where accountID='"+cstr(self.doc.account_id)+"'")
#		webnotes.errprint(a)
#		if a:
#			qry="insert into GroupList (accountID,groupID,userID) values ('"+cstr(self.doc.account_id)+"','"+cstr(self.doc.authorized_group)+"','"+cstr(self.doc.user_id)+"')"
#			webnotes.conn.sql(qry)
#			webnotes.errprint(qry)
#		else:
#			pass
