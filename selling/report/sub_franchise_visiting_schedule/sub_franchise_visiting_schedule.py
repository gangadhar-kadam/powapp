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
        return [
                "Freanchise:Link/Franchise:160", "Device ID:data:100", "Sub Franchise:Link/Sub Franchise:100","Sheduled Visting Date:date:100","Visted(Yes/No):data:100","Vistited Date Time:datetime:120","Reason:data:100"
        ]

def get_tracking_details(filters):
        #conditions = get_conditions(filters)
        return webnotes.conn.sql("""select account_id,device_id,sf_name,visiting_date,visited,visited_date,reason from `tabSub Franchise Visiting Schedule`  ORDER BY name """)


