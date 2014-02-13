
# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd.
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.utils import flt

def execute(filters=None):
	if not filters: filters = {}
	
	columns = get_columns()
	data = get_tracking_details(filters)
	
	return columns, data
	
def get_columns():
	return ["Date Time::160", "Latitude:Float:100", "Longitude:Float:100","Speed KPH:Float:100","Address:Data:120","Status Code:Int:100"]

def get_tracking_details(filters):
#	conditions = get_conditions(filters)
	return webnotes.conn.sql("""select FROM_UNIXTIME(timestamp) as timestamp, latitude, longitude,speedKPH,address,statusCode 
			from EventData ORDER BY timestamp DESC""")


#def get_conditions(filters):
#	conditions = ""
#	return conditions
