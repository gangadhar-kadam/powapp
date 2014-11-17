
#copyright (c) 2013, Web Notes Technologies Pvt. Ltd.
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
        return ["Sales Invoice Name:Link/Sales Invoice:130", "Customer Name:data:130","Date:Date:120","Total Amount:Currency:100"]

def get_plan_details(filters):
	#conditions = get_conditions(filters)
	qry="""select name,customer,posting_date,net_total_export from `tabSales Invoice` order by creation asc"""
        webnotes.errprint(qry)
	res = webnotes.conn.sql(qry)
	return res
