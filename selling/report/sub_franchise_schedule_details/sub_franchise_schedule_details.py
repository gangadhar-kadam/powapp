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
        return ["Region:Data:150", "Franchise Name:Data:160","Sub-Franchise Name:Data:160", "Weekely:Int:100","Forth Night:Int:100","One Month:Int:100"]

def get_plan_details(filters):
	res = webnotes.conn.sql("SELECT region,account_id,sf_name,coalesce((case when exists(select true from `tabFranchise Visiting Schedule` s where regions=t.region and visiting_frequency='Weekely' and creation in(select max(creation) from `tabFranchise Visiting Schedule` where regions=s.regions)) then (select frequency from `tabFranchise Visiting Schedule` st where regions=t.region and visiting_frequency='Weekely' and creation in(select max(creation) from `tabFranchise Visiting Schedule` where regions=st.regions and visiting_frequency='Weekely')) end),'-') as weekly_freq,coalesce((case when exists(select true from `tabFranchise Visiting Schedule` s where regions=t.region and visiting_frequency='Forth Night' and creation in(select max(creation) from `tabFranchise Visiting Schedule` where regions=s.regions)) then (select frequency from `tabFranchise Visiting Schedule` st where regions=t.region and visiting_frequency='Forth Night' and creation in(select max(creation) from `tabFranchise Visiting Schedule` where regions=st.regions and visiting_frequency='Forth Night')) end),'-') as forthly_freq,coalesce((case when exists(select true from `tabFranchise Visiting Schedule` s where regions=t.region and visiting_frequency='One Month' and creation in(select max(creation) from `tabFranchise Visiting Schedule` where regions=s.regions)) then (select frequency from `tabFranchise Visiting Schedule` st where regions=t.region and visiting_frequency='One Month' and creation in(select max(creation) from `tabFranchise Visiting Schedule` where regions=st.regions and visiting_frequency='One Month')) end),'-') as monthly_freq from `tabSub Franchise Visiting Schedule` t WHERE region IS NOT NULL group by region,account_id,sf_name")
        #conditions = get_conditions(filters) 
	#return webnotes.conn.sql("""select account_id,sf_name, region from `tabSub Franchise Visiting Schedule`""")
	return res

