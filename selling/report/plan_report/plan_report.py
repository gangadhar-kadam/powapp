# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd.
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.utils import flt

def execute(filters=None):
        if not filters: filters = {}

        columns = get_columns()
        data = get_plan_details(filters)

        return columns, data

def get_columns():
        return ["Franchise Name:Data:160", "Region:Data:100", "Weekely:Int:100","Forth Noght:Int:100","One Month:Int:100"]

def get_plan_details(filters):
#       conditions = get_conditions(filters)
        return webnotes.conn.sql("""select account_id,regions,frequency from `tabFranchise Visiting Schedule` group by regions""")


