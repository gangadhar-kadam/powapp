# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.utils import cint, cstr
from webnotes.model.doc import Document

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl


	def on_update(self):
		lt=self.doc.lat
		ln=self.doc.lon
		ac=self.doc.account_id
		qry="SELECT MBRContains(( SELECT GeomFromText(concat('Polygon((', latitude1,' ' ,longitude1,' ,',latitude2,' ' ,longitude2 , ' , ',latitude3,' ' ,longitude3 ,' , ',latitude4,' ' ,longitude4 ,' , ',latitude5,' ' , longitude5 ,' , ',latitude6,' ' ,longitude6 ,' , ',latitude7,' ' ,longitude7 ,' , ',latitude8, ' ' ,longitude8 ,' , ',latitude9,' ' ,longitude9 ,' , ',latitude10,' ' ,longitude10,' , ', latitude1,' ' ,longitude1 ,'))')) AS t FROM Geozone WHERE accountID = '"+cstr(ac)+"'),GeomFromText('Point("+cstr(lt)+" "+cstr(ln)+")'));"
		webnotes.errprint(qry)
		rs=webnotes.conn.sql(qry)
		webnotes.errprint(rs[0][0])
		if rs[0][0]=='0':
			webnotes.msgprint("Sorry ! the select sub-franchiese address does not included in your area.",raise_exception=1)
		else:
			webnotes.errprint("done")
		#s=webnotes.conn.sql("select name from `tabWarehouse` where name='"+self.doc.sf_name+"'")
		#if not s:
		#	d=Document('Warehouse')
		#	d.warehouse_name=self.doc.sf_name
		#	d.subf_name=self.doc.sf_name
		#	d.f_name=self.doc.account_id
		#	d.save(new=1)
		#else:
		#	pass


@webnotes.whitelist()
def get_state(doctype, txt, searchfield, start, page_len, filters):
	if filters.get('country'):
		return webnotes.conn.sql("select state from tabState where country = '%s'"%filters.get(country))	


