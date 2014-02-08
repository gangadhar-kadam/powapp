# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl


#	def on_update(self):
#		a=webnotes.conn.sql("select erp from Device where accountID='"+cstr(self.doc.account_id)+"'")
#               webnotes.errprint(a)
#               if a:
#                      qry="insert into DeviceList (accountID,groupID,userID) values ('"+cstr(self.doc.account_id)+"','"+cstr(self.doc.group_membership)+"','"+cstr(self.doc.user_id)+"')"
#                    webnotes.conn.sql(qry)
#                     webnotes.errprint(qry)
#          else
#                  pass

#		a=webnotes.conn.sql("select groupID from Device where acconutID='"+cstr(self.doc.name)+"'")
#		webnotes.errprint(a)
#		if a:
#			res="update DeviceList set groupID='"+cstr(self.doc.group_id)+"',deviceID='"+cstr(self.doc.device_id)+"' where accountID='"+cstr(self.doc.account_id)+"'"
#			webnotes.conn.sql(res)
#			webnotes.errprint(res)
#		else:
#			qry="insert into DeviceList (accountID,groupID,deviceID) values('"+cstr(self.doc.account_id)+"','"+cstr(self.doc.group_membership)+"','"+cstr(self.doc.device_id)+"')"
#			webnotes.conn.sql(qry)
#			webnotes.errprint(qry)

