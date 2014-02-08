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
		self.doc.account_id=self.doc.account_id.lower()
		self.doc.driver_id=self.doc.driver_id.lower()
		self.doc.device_id=self.doc.device_id.lower()
		self.doc.name=self.doc.name.lower()

		a=webnotes.conn.sql("select erp from Driver where driverID='"+cstr(self.doc.driver_id)+"'")
		webnotes.errprint(a)
		if a:
			res= "update Driver set driverID='"+cstr(self.doc.driver_id)+"',accountID='"+cstr(self.doc.account_id)+"',contactPhone='"+cstr(self.doc.contact_phone)+"',contactEmail='"+cstr(self.doc.contact_email)+"',birthdate='"+cstr(self.doc.birth_date)+"',driverStatus='"+cstr(self.doc.driver_status)+"',deviceID='"+cstr(self.doc.device_id)+"',lastUpdateTime='"+cstr(self.doc.last_update_time)+"',creationTime='"+cstr(self.doc.creation_time)+"',licenseType='"+cstr(self.doc.license_type)+"',licenseNumber='"+cstr(self.doc.license_number)+"',licenseExpire='"+cstr(self.doc.license_expire)+"',badgeID='"+cstr(self.doc.badge_id)+"',displayName='"+cstr(self.doc.display_name)+"',address='"+cstr(self.doc.address)+"' where erp='"+cstr(self.doc.name)+"'"
			webnotes.conn.sql(res)
			webnotes.errprint(res)
		else:
			qry= "insert into Driver (driverID,accountID,contactPhone,contactEmail,birthdate,driverStatus,deviceID,lastUpdateTime,creationTime,licenseType,licenseNumber,licenseExpire,badgeID,displayName,address,erp) values ('"+cstr(self.doc.driver_id)+"','"+cstr(self.doc.account_id)+"','"+cstr(self.doc.contact_phone)+"','"+cstr(self.doc.contact_email)+"','"+cstr(self.doc.birth_date)+"','"+cstr(self.doc.driver_status)+"','"+cstr(self.doc.device_id)+"','"+cstr(self.doc.last_update_time)+"','"+cstr(self.doc.creation_time)+"','"+cstr(self.doc.license_type)+"','"+cstr(self.doc.license_number)+"','"+cstr(self.doc.license_expire)+"','"+cstr(self.doc.badge_id)+"','"+cstr(self.doc.display_name)+"','"+cstr(self.doc.address)+"','"+cstr(self.doc.name)+"')"
			webnotes.conn.sql(qry)
			webnotes.errprint(qry)
