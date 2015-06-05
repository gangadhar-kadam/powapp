# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import webnotes
from webnotes import msgprint, _
from webnotes.model.bean import getlist
from webnotes.utils import flt
from webnotes.utils import flt, cstr, cint
from webnotes.utils.nestedset import DocTypeNestedSet
	
class DocType(DocTypeNestedSet):
	def __init__(self, doc, doclist=[]):
		self.doc = doc
		self.doclist = doclist
		self.nsm_parent_field = 'parent_territory'

	def validate(self): 
		if self.doc.name.isalpha():
			pass
		else:
			msgprint("Space not allowed in Territory name..!" , raise_exception=1)

		for d in getlist(self.doclist, 'target_details'):
			if not flt(d.target_qty) and not flt(d.target_amount):
				msgprint("Either target qty or target amount is mandatory.")
				raise Exception

	def on_update(self):
		super(DocType, self).on_update()
		self.validate_one_root()
		gzone="insert into Geozone VALUES ('sysadmin','"+cstr(self.doc.name)+"',0,0,0,0,0,'',1,1,1,0,0,'',3,500,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'','','','','','','','','Custom Zone',1412941401,1412941401)"
		g=webnotes.conn.sql(gzone)
