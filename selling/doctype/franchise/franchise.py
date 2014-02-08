# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.model.doc import Document
from webnotes.utils import cint,cstr

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl


	def on_update(self):
		self.doc.account_id=self.doc.account_id.lower()
		self.doc.name=self.doc.name.lower()
                webnotes.errprint(self.doc.name)
                a=webnotes.conn.sql("select erp from Account where accountID='"+cstr(self.doc.account_id)+"'")
                webnotes.errprint(a)
                if a:
                        res="update Account set password='"+cstr(self.doc.password)+"',isActive='"+cstr(self.doc.active)+"',description='"+cstr(self.doc.account_description)+"',contactEmail='"+cstr(self.doc.contact_email)+"',contactName='"+cstr(self.doc.contact_name)+"',contactPhone='"+cstr(self.doc.contact_phone)+"',notifyEmail='"+cstr(self.doc.notify_email)+"',speedUnits='"+cstr(self.doc.speed_units)+"',distanceUnits='"+cstr(self.doc.distance_units)+"',volumeUnits='"+cstr(self.doc.volume_units)+"',pressureUnits='"+cstr(self.doc.pressure_units)+"',economyUnits='"+cstr(self.doc.economy_units)+"',temperatureUnits='"+cstr(self.doc.temperature_units)+"',latLonFormat='"+cstr(self.doc.latitude_longitude_format)+"' where erp='"+cstr(self.doc.name)+"'"
                        webnotes.conn.sql(res)
                        webnotes.errprint(res)
                else:
                        qry="insert into Account (accountID,password,isActive,description,contactName,contactPhone,contactEmail,notifyEmail,speedUnits,distanceUnits,volumeUnits,pressureUnits,economyUnits,temperatureUnits,latLonFormat,erp) values('"+cstr(self.doc.account_id)+"','"+cstr(self.doc.password)+"','"+cstr(self.doc.active)+"','"+cstr(self.doc.account_description)+"','"+cstr(self.doc.contact_name)+"','"+cstr(self.doc.contact_phone)+"','"+cstr(self.doc.contact_email)+"','"+cstr(self.doc.notify_email)+"','"+cstr(self.doc.speed_units)+"','"+cstr(self.doc.distance_units)+"','"+cstr(self.doc.volume_units)+"','"+cstr(self.doc.pressure_units)+"','"+cstr(self.doc.economy_units)+"','"+cstr(self.doc.temperature_units)+"','"+cstr(self.doc.latitude_longitude_format)+"','"+cstr(self.doc.name)+"')"
                        webnotes.conn.sql(qry)
                        webnotes.errprint(qry)

		s=webnotes.conn.sql("select name from `tabWarehouse` where f_name='"+cstr(self.doc.account_id)+"'")
		webnotes.errprint(s)
		if not s:
			d = Document('Warehouse')
			d.f_name=self.doc.account_id
			d.warehouse_name=self.doc.account_id
			d.company='PowerCap'
			d.save()
		else:
			pass
		#webnotes.errprint("Done...")
		self.profile_ceation()
	def profile_ceation(self):
			webnotes.errprint("creating profile_ceation")
			ch=webnotes.conn.sql("select name from tabProfile where name like '%"+cstr(self.doc.contact_email)+"%'")
			if ch:
				pass
			else :
				pp=Document('Profile')
				pp.email=self.doc.contact_email
				pp.first_name=self.doc.contact_name
				webnotes.errprint(self.doc.password)
				pp.new_password=self.doc.password
				pp.account_id=self.doc.name
				pp.franchise_admin='1'
				pp.enabled='1'
				pp.save(new=1)
				ur=Document('UserRole')
				ur.parent=self.doc.contact_email
				ur.parentfield='user_roles'
				ur.parenttype='Profile'
				ur.role='Franchise'
				ur.save(new=1)
				dv=Document('DefaultValue')
				dv.parent=self.doc.contact_email
				dv.parentfield='system_defaults'
				dv.parenttype='Control Panel'
				dv.defkey='account_id'
				dv.defvalue=self.doc.name
				dv.save(new=1)
				aa="insert into __Auth(user,password) values('"+self.doc.contact_email+"',password('"+self.doc.password+"'))"
				webnotes.errprint(aa)
				webnotes.conn.sql(aa)
