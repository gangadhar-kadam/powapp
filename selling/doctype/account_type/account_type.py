# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.utils import cint, now, cstr

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl


	def on_update(self):
		webnotes.errprint(self.doc.name)
		a=webnotes.conn.sql("select erp from Account where accountID='"+cstr(self.doc.account_id)+"'")
		webnotes.errprint(a)
		if a:
			res="update Account set password='"+cstr(self.doc.password)+"',isActive='"+cstr(self.doc.enabled)+"',description='"+cstr(self.doc.account_description)+"',contactEmail='"+cstr(self.doc.contact_email)+"',contactName='"+cstr(self.doc.contact_name)+"',contactPhone='"+cstr(self.doc.contact_phone)+"',notifyEmail='"+cstr(self.doc.notify_email)+"',speedUnits='"+cstr(self.doc.speed_units)+"',distanceUnits='"+cstr(self.doc.distance_units)+"',volumeUnits='"+cstr(self.doc.volume_units)+"',pressureUnits='"+cstr(self.doc.pressure_units)+"',economyUnits='"+cstr(self.doc.economy_units)+"',temperatureUnits='"+cstr(self.doc.temperature_units)+"',latLonFormat='"+cstr(self.doc.latitude_longitude_format)+"' where erp='"+cstr(self.doc.name)+"'"
			webnotes.conn.sql(res)
			webnotes.errprint(res)
		else:
			qry="insert into Account (accountID,password,isActive,description,contactName,contactPhone,contactEmail,notifyEmail,speedUnits,distanceUnits,volumeUnits,pressureUnits,economyUnits,temperatureUnits,latLonFormat,erp) values('"+cstr(self.doc.account_id)+"','"+cstr(self.doc.password)+"','"+cstr(self.doc.enabled)+"','"+cstr(self.doc.account_description)+"','"+cstr(self.doc.contact_name)+"','"+cstr(self.doc.contact_phone)+"','"+cstr(self.doc.contact_email)+"','"+cstr(self.doc.notify_email)+"','"+cstr(self.doc.speed_units)+"','"+cstr(self.doc.distance_units)+"','"+cstr(self.doc.volume_units)+"','"+cstr(self.doc.pressure_units)+"','"+cstr(self.doc.economy_units)+"','"+cstr(self.doc.temperature_units)+"','"+cstr(self.doc.latitude_longitude_format)+"','"+cstr(self.doc.name)+"')"
			webnotes.conn.sql(qry)
			webnotes.errprint(qry)

