cur_frm.fields_dict.customer_data.grid.get_field("serial_no").get_query = function(doc) {
                return "select a.name from `tabSerial No` as a where status='Delivered' and name not in(select serial_no from `tabCustomer Data` where serial_no=a.name);"
        }

cur_frm.fields_dict.customer_data.grid.get_field("replaced_using_warrenty").get_query = function(doc) {
		aa="select serial_no from `tabCustomer Data` where parent='"+doc.name+"' and replaced_using_warrenty is null;"
		console.log(aa);
                return "select serial_no from `tabCustomer Data` where parent=doc.name and replaced_using_warrenty is null;"
        }

cur_frm.cscript.serial_no = function(doc, cdt, cdn) {
  //alert('serial no');
  var d = locals[cdt][cdn];
  //alert(d.serial_no);
  get_server_fields('get_details', d.serial_no, 'customer_data', doc, cdt, cdn, 1);
}
