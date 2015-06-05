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
        return ["Franchise:Link/Franchise:130", "Device ID:data:100", "Sub-Franchise:Link/Sub Franchise:120","Visited (Yes/No):data:120","Visited Date Time:datetime:150","Reason:data:300"]

def get_tracking_details(filters):
        #conditions = get_conditions(filters)
        return webnotes.conn.sql("""select account_id,device_id,sf_name,visited,visited_date,reason from `tabSub Franchise Visiting Schedule`  ORDER BY sf_name,visiting_date """)

