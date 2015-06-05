from __future__ import unicode_literals
import webnotes
from webnotes.utils import flt,cstr
def execute(filters=None):
        if not filters: filters = {}
        columns = get_columns()
        data = get_plan_details(filters)
        return columns, data
def get_columns():
        return ["Sub Franchise:Link/Sub Franchise:230"]

def get_plan_details(filters):
	#conditions = get_conditions(filters)
	qry="""select name,region,lat,lon from `tabSub Franchise` """
        webnotes.errprint(qry)
        res = webnotes.conn.sql(qry)
        suib=[]
        #webnotes.errprint(res)
        for r in res:
                #webnotes.errprint(r[0])
                qry="SELECT MBRContains(( SELECT GeomFromText(concat('Polygon((', latitude1,' ' ,longitude1,' ,',latitude2,' ' ,longitude2 , ' , ',latitude3,' ' ,longitude3 ,' , ',latitude4,' ' ,longitude4 ,' , ',latitude5,' ' , longitude5 ,' , ',latitude6,' ' ,longitude6 ,' , ',latitude7,' ' ,longitude7 ,' , ',latitude8, ' ' ,longitude8 ,' , ',latitude9,' ' ,longitude9 ,' , ',latitude10,' ' ,longitude10,' , ', latitude1,' ' ,longitude1 ,'))')) AS t FROM Geozone WHERE accountID = 'sysadmin' and geozoneID='"+cstr(r[1])+"' order by lastUpdateTime desc limit 1 ),GeomFromText('Point("+cstr(r[2])+" "+cstr(r[3])+")'));"
                #webnotes.errprint(qry)
                sb=webnotes.conn.sql(qry)
                if sb[0][0]==0:
                   suib.append(r)
                   webnotes.errprint(r) 
                   #webnotes.errprint(qry)

	return suib
