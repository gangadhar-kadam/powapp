# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.utils import cint,cstr

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl


	def on_update(self):
#		m=webnotes.conn.sql("select profile_user from `tabUser`")
#		webnotes.errprint(m)
		self.doc.account_id=self.doc.account_id.lower()
		self.doc.user_id=self.doc.user_id.lower()
		self.doc.authorized_group=self.doc.authorized_group.lower()
		self.doc.device_id=self.doc.device_id.lower()
		self.doc.name=self.doc.name.lower()
		a=webnotes.conn.sql("select erp from User where userID='"+cstr(self.doc.user_id)+"'")
		webnotes.errprint(a)
		if a:
			res= "update User set accountID='"+cstr(self.doc.account_id)+"',userID='"+cstr(self.doc.user_id)+"',password='"+cstr(self.doc.password)+"',preferredDeviceID='"+cstr(self.doc.device_id)+"',isActive='"+cstr(self.doc.active)+"',contactName='"+cstr(self.doc.contact_name)+"',contactPhone='"+cstr(self.doc.contact_phone)+"',contactEmail='"+cstr(self.doc.contact_email)+"',notifyEmail='"+cstr(self.doc.notify_email)+"',description='"+cstr(self.doc.user_description)+"' where erp='"+cstr(self.doc.name)+"'"
			webnotes.conn.sql(res)
			webnotes.errprint(res)
			
		else:	
			qry= "insert into User (accountID,userID,password,preferredDeviceID,isActive,contactName,contactPhone,contactEmail,notifyEmail,description,erp) values('"+cstr(self.doc.account_id)+"','"+cstr(self.doc.user_id)+"','"+cstr(self.doc.password)+"','"+cstr(self.doc.device_id)+"','"+cstr(self.doc.active)+"','"+cstr(self.doc.contact_name)+"','"+cstr(self.doc.contact_phone)+"','"+cstr(self.doc.contact_email)+"','"+cstr(self.doc.notify_email)+"','"+cstr(self.doc.user_description)+"','"+cstr(self.doc.name)+"')"
			webnotes.conn.sql(qry)
			webnotes.errprint(qry)
			r="insert into GroupList (accountID,groupID,userID) values('"+cstr(self.doc.account_id)+"','"+cstr(self.doc.authorized_group)+"','"+cstr(self.doc.user_id)+"')"
			webnotes.conn.sql(r)
			webnotes.errprint(r)
 				
