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
        #return ["Region:Data:150", "Franchise Name:Data:160","Sub-Franchise Name:Data:160", "Weekely:Int:100","Forth Nightly:Int:100","One Monthly:Int:100"]
	return ["Region:Data:90", "Franchise Name:Data:130","Sub-Franchise Name:Data:160","Planned Weekly visits:Data:160","Planned Fort Nightly visits:Data:160","Planned Monthly visits:Data:160","Actutal Visits:Data:100","Average visited days difference:Data:160","See Details:Data:160"]
	

def get_plan_details(filters):
	#res = webnotes.conn.sql("SELECT region,account_id,sf_name,coalesce((case when exists(select true from `tabFranchise Visiting Schedule` s where regions=t.region and visiting_frequency='Weekely' and creation in(select max(creation) from `tabFranchise Visiting Schedule` where regions=s.regions)) then (select frequency from `tabFranchise Visiting Schedule` st where regions=t.region and visiting_frequency='Weekely' and creation in(select max(creation) from `tabFranchise Visiting Schedule` where regions=st.regions and visiting_frequency='Weekely')) end),'-') as weekly_freq,coalesce((case when exists(select true from `tabFranchise Visiting Schedule` s where regions=t.region and visiting_frequency='Forth Night' and creation in(select max(creation) from `tabFranchise Visiting Schedule` where regions=s.regions)) then (select frequency from `tabFranchise Visiting Schedule` st where regions=t.region and visiting_frequency='Forth Night' and creation in(select max(creation) from `tabFranchise Visiting Schedule` where regions=st.regions and visiting_frequency='Forth Night')) end),'-') as forthly_freq,coalesce((case when exists(select true from `tabFranchise Visiting Schedule` s where regions=t.region and visiting_frequency='One Month' and creation in(select max(creation) from `tabFranchise Visiting Schedule` where regions=s.regions)) then (select frequency from `tabFranchise Visiting Schedule` st where regions=t.region and visiting_frequency='One Month' and creation in(select max(creation) from `tabFranchise Visiting Schedule` where regions=st.regions and visiting_frequency='One Month')) end),'-') as monthly_freq from `tabSub Franchise Visiting Schedule` t WHERE region IS NOT NULL group by region,account_id,sf_name")
        #conditions = get_conditions(filters) 
	#return webnotes.conn.sql("""select account_id,sf_name, region from `tabSub Franchise Visiting Schedule`""")
	qry="""SELECT region,account_id,sf_name,COALESCE(weekly,'-') AS weekly,COALESCE(forth_nightly,'-') AS forth_nightly,COALESCE(monthly,'-') AS monthly,( SELECT COUNT(*) FROM `tabSub Franchise Visiting Schedule` WHERE sf_name=t.sf_name AND region=t.region AND date_format(visited_date,'%Y-%m')=date_format(t.creation,'%Y-%m')) AS visited_count,rpad( COALESCE(( CASE WHEN ( SELECT COUNT(*) FROM `tabSub Franchise Visiting Schedule` WHERE sf_name=t.sf_name AND region=t.region AND date_format(visited_date,'%Y-%m')=date_format(t.creation,'%Y-%m'))>1 THEN ( SELECT DATEDIFF(MAX(visited_date),MIN(visited_date)) FROM `tabSub Franchise Visiting Schedule` WHERE sf_name=t.sf_name AND date_format(visited_date,'%Y-%m')=date_format(t.creation,'%Y-%m') )/ ( SELECT COUNT(*) FROM `tabSub Franchise Visiting Schedule` WHERE sf_name=t.sf_name AND region=t.region AND date_format(visited_date,'%Y-%m')=date_format(t.creation,'%Y-%m')) ELSE 0  END ),0),4,0)AS average,'<a href="http://54.251.111.127:8000/app.html#query-report/Sub Franchise Visiting Schedule">Check Details</a>'FROM `tabSub Franchise Visiting Schedule` t GROUP BY  sf_name,date_format(creation,'%Y-%m')"""
	res = webnotes.conn.sql(qry)
	return res

