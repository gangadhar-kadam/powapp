# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import webnotes

from webnotes.utils import cstr
from webnotes.model import db_exists
from webnotes.model.bean import copy_doclist
from webnotes.model.code import get_obj
from webnotes import msgprint

  
# ----------

class DocType:
  def __init__(self, doc, doclist=[]):
    self.doc = doc
    self.doclist = doclist
      
  def create_receiver_list(self):
    rec, where_clause = '', ''
    if self.doc.send_to == 'All Customer':
      rec = webnotes.conn.sql("select customer_name, phone_number from `tabCustomer Details` where phone_number is not null")
    elif self.doc.send_to == 'All Sub -franchiese':
      rec = webnotes.conn.sql("select c_name, c_number from `tabSub Franchise` where c_number is not null and c_name is not null")
    else :
      rec = webnotes.conn.sql("select contact_name, contact_phone from `tabFranchise` where contact_phone is not null")    
    rec_list = ''
    for d in rec:
      rec_list += d[0] + ' - ' + d[1] + '\n'
    self.doc.receiver_list = rec_list

  def get_receiver_nos(self):
    receiver_nos = []
    #webnotes.errprint(self.doc.receiver_list)
    for d in self.doc.receiver_list.split('\n'):
      receiver_no = d
      if '-' in d:
        receiver_no = receiver_no.split('-')[1]
      if receiver_no.strip():
        receiver_nos.append(cstr(receiver_no).strip())
      #webnotes.errprint(receiver_nos)
    return receiver_nos

  def send_sms(self):
    if not self.doc.message:
      msgprint("Please enter message before sending")
    else:
      receiver_list = self.get_receiver_nos()
      #webnotes.errprint(receiver_list)
      if receiver_list:
        msgprint(get_obj('SMS Control', 'SMS Control').send_sms(receiver_list, cstr(self.doc.message)))
