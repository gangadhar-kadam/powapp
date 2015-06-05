cur_frm.cscript.image = function(doc) {
	refresh_field("image_view");
}

cur_frm.cscript.refresh = function(doc, cdt, cdn) {
	if(doc.region && !doc.__islocal){
		//set_field_permlevel('region',1);
		cur_frm.set_value('region1',doc.region);
		refresh_field('region1');
	}
		
}

cur_frm.fields_dict['region'].get_query = function(doc, cdt, cdn) {
        return "select name from `tabTerritory` where parent_territory='All Territories' and is_group='No'"
}

cur_frm.cscript.contact_email = function(doc, dt, dn) {
   var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
   check=re.test(doc.contact_email)
   if(check==false)
   {
   	cur_frm.set_value("email_id", '')
   	msgprint("Please Enter valid Email Id..! ");
   	throw "Please Enter Correct Email ID!"
   }
  
}

cur_frm.cscript.notify_email = function(doc, dt, dn) {
   var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
   check=re.test(doc.notify_email)
   if(check==false)
   {
        cur_frm.set_value("email_id", '')
        msgprint("Please Enter valid Email Id..! ");
        throw "Please Enter Correct Email ID!"
   }

}


/*cur_frm.cscript.validate = function(doc, cdt, cdn) {
      if (doc.__islocal){
		get_server_fields('validate_imei','','',doc, cdt, cdn, 1 ,function(r){
		console.log(r.imei)
		if (r.imei){
			alert("This IMEI no. used for another franchise.Record not save..")
	  		throw "cannot create";
		}		
		if (r.email){
			alert("This Email_id used for another franchise.Record not save..");
	  		throw "cannot create";
		}
		});
	}
}*/
