# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

# For license information, please see license.txt

from __future__ import unicode_literals
import webnotes
from webnotes.utils import cint,cstr

class DocType:
	def __init__(self, d, dl):
		self.doc, self.doclist = d, dl


#	def on_update(self):
#		self.doc.ids=self.doc.name

		
