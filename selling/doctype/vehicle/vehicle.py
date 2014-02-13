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
		self.doc.device_id=self.doc.device_id.lower()
		#self.doc.vehicle_id=self.doc.vehicle_id.lower()
		#self.doc.unique_id=self.doc.unique_id.lower()
		#self.doc.driver_id=self.doc.driver_id.lower()
		self.doc.group_membership=self.doc.group_membership.lower()
		self.doc.name=self.doc.name.lower()

		a=webnotes.conn.sql("select erp from Device where deviceID='"+cstr(self.doc.device_id)+"'")
   		webnotes.errprint(a)
		if a:
			res= "update Device set isActive='"+cstr(self.doc.active)+"',accountID='"+cstr(self.doc.account_id)+"',deviceID='"+cstr(self.doc.device_id)+"',vehicleID='"+cstr(self.doc.vehicle_id)+"',uniqueID='"+cstr(self.doc.unique_id)+"',vehicleMake='"+cstr(self.doc.vehicle_make)+"',vehicleModel='"+cstr(self.doc.vehicle_model)+"',equipmentType='"+cstr(self.doc.equipment_type)+"',serialNumber='"+cstr(self.doc.serial_number)+"',fuelCapacity='"+cstr(self.doc.fuel_capacity)+"',lastOdometerKM='"+cstr(self.doc.reported_odometer)+"',description='"+cstr(self.doc.vehicle_description)+"',groupID='"+cstr(self.doc.group_membership)+"',imeiNumber='"+cstr(self.doc.imei_number)+"',simPhoneNumber='"+cstr(self.doc.sim_phone)+"',licensePlate='"+cstr(self.doc.license_plate)+"',driverID='"+cstr(self.doc.driver_id)+"',lastEngineHours='"+cstr(self.doc.reported_engine_hours)+"',displayColor='"+cstr(self.doc.map_route_color)+"',creationTime='"+cstr(self.doc.creation_time)+"' where erp='"+cstr(self.doc.name)+"'"
			webnotes.conn.sql(res)
			webnotes.errprint(res)
			r="update DeviceList set groupID='"+cstr(self.doc.group_membership)+"' where accountID='"+cstr(self.doc.account_id)+"'"
			webnotes.conn.sql(r)
			webnotes.errprint(r)
		else:
			qry= "insert into Device (isActive,deviceID,accountID,vehicleID,uniqueID,vehicleMake,vehicleModel,equipmentType,serialNumber,fuelCapacity,lastOdometerKM,description,imeiNumber,simPhoneNumber,licensePlate,driverID,lastEngineHours,displayColor,creationTime,erp) values ('"+cstr(self.doc.active)+"','"+cstr(self.doc.device_id)+"','"+cstr(self.doc.account_id)+"','"+cstr(self.doc.vehicle_id)+"','"+cstr(self.doc.unique_id)+"','"+cstr(self.doc.vehicle_make)+"','"+cstr(self.doc.vehicle_model)+"','"+cstr(self.doc.equipment_type)+"','"+cstr(self.doc.serial_number)+"','"+cstr(self.doc.fuel_capacity)+"','"+cstr(self.doc.reported_odometer)+"','"+cstr(self.doc.vehicle_description)+"','"+cstr(self.doc.imei_number)+"','"+cstr(self.doc.sim_phone)+"','"+cstr(self.doc.license_plate)+"','"+cstr(self.doc.driver_id)+"','"+cstr(self.doc.reported_engine_hours)+"','"+cstr(self.doc.map_route_color)+"','"+cstr(self.doc.creation_time)+"','"+cstr(self.doc.name)+"')"
			#webnotes.conn.sql(qry)
			webnotes.errprint(qry)
			webnotes.conn.sql(qry)
			s="insert into DeviceList (accountID,groupID,deviceID) values('"+cstr(self.doc.account_id)+"','"+cstr(self.doc.group_membership)+"','"+cstr(self.doc.device_id)+"')"
			webnotes.conn.sql(s)
			webnotes.errprint(s)
	
