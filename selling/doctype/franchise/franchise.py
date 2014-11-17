# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.model.doc import Document
from webnotes.model.bean import getlist
from webnotes.utils import cint,cstr,validate_email_add
import re
from webnotes import msgprint, _

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl

	def validate(self):
		if self.doc.fields.get('__islocal') or not self.doc.name:
			res=webnotes.conn.sql("select count(name) from tabFranchise")
			webnotes.errprint(res)
			if res[0][0]<=50:
				pass
			else:
				webnotes.msgprint("The maximun franchises creation limit is reached, Please contact administrator...!" , raise_exception=1)
		#Franchise
		if self.doc.account_id:
			if self.doc.account_id.isalpha():
				pass
			else:
				msgprint("Please enter only letters, space not allowed in Franchise name..",raise_exception=1)

		#Contact Number
		cont=self.doc.contact_phone
                if cont:
                        if cont.isdigit() and len(cont)>9 and len(cont)<13:
                                pass    
                        else:
                                msgprint("Please enter valid phone no...",raise_exception=1)
		#Contact Name
		name=self.doc.contact_name
                if re.match(r'^[a-zA-Z][ A-Za-z_-]*$', name):
                        pass
                else:
                        msgprint("Please Enter Only letters in Contact Name..!" , raise_exception=1)
		#User Id
		user=self.doc.user_id
		if re.match(r'^[a-zA-Z][ A-Za-z_-]*$', user):
			pass
                else:
			msgprint("Please enter valid User ID..",raise_exception=1)
		#Device Id
                dvc=self.doc.device_id
                if len(dvc) == 15 and dvc.isdigit():
                        pass  
                else:
                        msgprint("Please enter 15 digits IMEI number for Device Id...",raise_exception=1)
		#IMEI Number
		#p = self.doc.imei
                #if len(p) == 15 and p.isdigit():
                #        pass
                #else:
                #        msgprint("Please Enter 15 Digits IMEI Number..!" , raise_exception=1)	
		
		#User id
		#usr=webnotes.conn.sql("select user_id from `tabFranchise` where region='"+self.doc.region+"' and user_id='"+self.doc.user_id+"'",as_list=1)
		#webnotes.errprint(usr)
                #if usr==self.doc.user_id:
			#validate='false'
		#	msgprint("User Id Already Exist",raise_exception=1)
		#else:
		#	pass

		#Device Id
		#dvc=webnotes.conn.sql("select name from `tabFranchise` where region='"+self.doc.region+"' and device_id='"+self.doc.device_id+"'",as_list=1)
                #if dvc:
                #       validate='false'
                #      msgprint("Device Id Already Exist",raise_exception=1)

	def on_update(self):
		#self.profile_ceation()
		self.doc.account_id=self.doc.account_id.lower()
		self.doc.user_id=self.doc.user_id.lower()
                self.doc.authorized_group=self.doc.account_id+"_"+self.doc.region
                self.doc.device_id=self.doc.device_id.lower()
		#Franchise.....
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
		#USER.......
		webnotes.errprint("in user")
		webnotes.errprint(self.doc.user_id)
		b=webnotes.conn.sql("select erp from User where accountID='"+cstr(self.doc.account_id)+"'")
                webnotes.errprint(b)
                if b:
			webnotes.errprint("Update user...")
                        res1= "update User set accountID='"+cstr(self.doc.account_id)+"',userID='"+cstr(self.doc.user_id)+"',password='"+cstr(self.doc.password1)+"',isActive='"+cstr(self.doc.active)+"',preferredDeviceID='"+cstr(self.doc.device_id)+"',contactName='"+cstr(self.doc.contact_name)+"',contactPhone='"+cstr(self.doc.contact_phone)+"',contactEmail='"+cstr(self.doc.contact_email)+"',notifyEmail='"+cstr(self.doc.notify_email)+"',description='"+cstr(self.doc.user_description)+"' where erp='"+cstr(self.doc.name)+"'" 
			webnotes.errprint(res1)
                        webnotes.conn.sql(res1)
                        #webnotes.errprint(res1)
			gl="update GroupList set groupID='"+cstr(self.doc.authorized_group)+"',userID='"+cstr(self.doc.user_id)+"' where accountID='"+cstr(self.doc.account_id)+"'"
			webnotes.conn.sql(gl)
			webnotes.errprint(gl)
                else:   
                        qry1= "insert into User (accountID,userID,password,preferredDeviceID,isActive,contactName,contactPhone,contactEmail,notifyEmail,description,erp) values('"+cstr(self.doc.account_id)+"','"+cstr(self.doc.user_id)+"','"+cstr(self.doc.password1)+"','"+cstr(self.doc.device_id)+"','"+cstr(self.doc.active)+"','"+cstr(self.doc.contact_name)+"','"+cstr(self.doc.contact_phone)+"','"+cstr(self.doc.contact_email)+"','"+cstr(self.doc.notify_email)+"','"+cstr(self.doc.user_description)+"','"+cstr(self.doc.name)+"')" 
                        webnotes.conn.sql(qry1)
                        webnotes.errprint(qry1)
                        #r="insert into GroupList (accountID,groupID,userID) values('"+cstr(self.doc.account_id)+"','"+cstr(self.doc.authorized_group)+"','"+cstr(self.doc.user_id)+"')"
                        #webnotes.conn.sql(r)
                        #webnotes.errprint(r)
		#Device.....
		webnotes.errprint("In Device...")
		c=webnotes.conn.sql("select erp from Device where accountID='"+cstr(self.doc.account_id)+"'")
                webnotes.errprint(c)
                if c:
                        res2= "update Device set isActive='"+cstr(self.doc.enabled)+"',accountID='"+cstr(self.doc.account_id)+"',deviceID='"+cstr(self.doc.device_id)+"',groupID='"+cstr(self.doc.authorized_group)+"',imeiNumber='"+cstr(self.doc.imei)+"' where erp='"+cstr(self.doc.name)+"'"
                        webnotes.conn.sql(res2)
                        webnotes.errprint(res2)
                        r1="update DeviceList set groupID='"+cstr(self.doc.authorized_group)+"',deviceID='"+cstr(self.doc.device_id)+"' where accountID='"+cstr(self.doc.account_id)+"'"
                        webnotes.conn.sql(r1)
                        webnotes.errprint(r1)
                else:
                        qry1= "insert into Device (isActive,deviceID,accountID,imeiNumber,erp) values ('"+cstr(self.doc.enabled)+"','"+cstr(self.doc.device_id)+"','"+cstr(self.doc.account_id)+"','"+cstr(self.doc.imei)+"','"+cstr(self.doc.name)+"')"
                        webnotes.errprint(qry1)
                        webnotes.conn.sql(qry1)
                        #s1="insert into DeviceList (accountID,groupID,deviceID) values('"+cstr(self.doc.account_id)+"','"+cstr(self.doc.authorized_group)+"','"+cstr(self.doc.device_id)+"')"
                        #webnotes.conn.sql(s1)
                        #webnotes.errprint(s1)


		s=webnotes.conn.sql("select warehouse_name from `tabWarehouse` where f_name='"+cstr(self.doc.account_id)+"'")
		webnotes.errprint(s)
		if not s:
			d = Document('Warehouse')
			d.f_name=self.doc.account_id
			d.warehouse_name=self.doc.account_id
			d.company='PowerCap'
			d.save()
                        if cint(webnotes.defaults.get_global_default("auto_accounting_for_stock")):
                          if not webnotes.conn.get_value("Account", {"account_type": "Warehouse",
                                        "master_name": self.doc.name}) and not webnotes.conn.get_value("Account",
                                        {"account_name": self.doc.warehouse_name}):
                                if self.doc.fields.get("__islocal") or not webnotes.conn.get_value(
                                                "Stock Ledger Entry", {"warehouse": d.name}):
                                        #self.validate_parent_account()
                                        ac_bean = webnotes.bean({
                                                "doctype": "Account",
                                                'account_name': d.name,
                                                'parent_account': "Stock Assets - P",
                                                'group_or_ledger':'Ledger',
                                                'company':"PowerCap",
                                                "account_type": "Warehouse",
                                                "master_name": d.name,
                                                "freeze_account": "No"
                                        })
                                        ac_bean.ignore_permissions = True
                                        ac_bean.insert()

		else:
			pass
		#webnotes.errprint("Done...")
		self.profile_ceation()
		self.validate_email()
		self.validate_notify_email()
		
	def validate_email(self):
		if self.doc.contact_email and not validate_email_add(self.doc.contact_email):
  			msgprint("Please enter valid Email..." , raise_exception=1)
  	
	def validate_notify_email(self):
		if self.doc.notify_email:
                	if self.doc.notify_email and not validate_email_add(self.doc.notify_email):
                        	msgprint("Please enter valid Email...",raise_exception=1)		

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
				dv.defkey='region'
				dv.defvalue=self.doc.region
				dv.save(new=1)
				dv1=Document('DefaultValue')
                                dv1.parent=self.doc.contact_email
                                dv1.parentfield='system_defaults'
                                dv1.parenttype='Control Panel'
                                dv1.defkey='regions'
                                dv1.defvalue=self.doc.regions
                                dv1.save(new=1)
				aa="insert into __Auth(user,password) values('"+self.doc.contact_email+"',password('"+self.doc.password+"'))"
				webnotes.errprint(aa)
				webnotes.conn.sql(aa)
				zz=webnotes.conn.sql("select accountID from Geozone where accountID='"+self.doc.region+"' and geozoneID='"+self.doc.region+"'",debug=1)
				if not zz:
					bb="INSERT INTO Geozone select '"+self.doc.account_id+"', geozoneID,sortID, minLatitude,maxLatitude,minLongitude,maxLongitude,zonePurposeID,reverseGeocode,arrivalZone,departureZone,autoNotify,zoomRegion,shapeColor,zoneType,radius,latitude1,longitude1,latitude2,longitude2,latitude3,longitude3,latitude4,longitude4,latitude5,longitude5,latitude6,longitude6,latitude7,longitude7,latitude8,longitude8,latitude9,longitude9,latitude10,longitude10,clientUpload,clientID,groupID,streetAddress,city,stateProvince,postalCode,country,subdivision,displayName,description,lastUpdateTime,creationTime from Geozone where accountID='sysadmin' and geozoneID='"+self.doc.region+"'"
					webnotes.errprint (bb)
					webnotes.conn.sql(bb)				
                                #dvc="select groupID from DeviceList where accountID='"+self.doc.account_id+"'"
				#webnotes.errprint(dvc)
			
                                #webnotes.conn.sql(dvc)
				#if dvc:
				#	pass
				#else:
				dg=Document('Device Group')
				dg.group_id=self.doc.region.lower()
				dg.account_id=self.doc.account_id.lower()
				dg.region=self.doc.region.lower()
				dg.save(new=1)
				self.doc.authorized_group=dg.name	
				#DEVICE List
				dlist=webnotes.conn.sql("select groupID from DeviceList where deviceID='"+self.doc.device_id+"'")
				webnotes.errprint(dlist)
				if dlist:
					pass
				else:
					dl="insert into DeviceList (accountID,groupID,deviceID) values('"+cstr(self.doc.account_id)+"','"+cstr(self.doc.authorized_group)+"','"+cstr(self.doc.device_id)+"')"
				webnotes.conn.sql(dl)
				webnotes.errprint(dl)
				#GROUP List
				glist=webnotes.conn.sql("select groupID from GroupList where accountID='"+cstr(self.doc.account_id)+"' and userID='"+cstr(self.doc.user_id)+"'")
				webnotes.errprint(glist)
				if glist:
					pass
				else:
					gl="insert into GroupList (accountID,groupID,userID) values('"+cstr(self.doc.account_id)+"','"+cstr(self.doc.authorized_group)+"','"+cstr(self.doc.user_id)+"')"
					webnotes.conn.sql(gl)	
					webnotes.errprint(gl)
