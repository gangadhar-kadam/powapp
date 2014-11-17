import webnotes
from webnotes.utils import flt

def execute(filters=None):
	if not filters: filters = {}
	
	columns = get_columns()
	data = get_tracking_details(filters)
	
	return columns, data
	
def get_columns():
	return ["Account Id:Data:120","Device Id:Data:120","Date Time::160", "Latitude:Float:100", "Longitude:Float:100","Address:Data:120","Status Code:Data:100"]

def get_tracking_details(filters):
#	conditions = get_conditions(filters)
	return webnotes.conn.sql("""select accountID,deviceID,date_format(from_unixtime(timestamp),'%d-%m-%Y %H:%i:%s'),latitude,longitude,address,SCode from EventData""")

