//cur_frm.cscript.refresh  =function(doc, cdt, cdn) {
//	console.log("hiiii")
//	return get_server_fields('get_profile', '', '', doc, cdt, cdn, 1,function(r,rt) {console.log(r)} );
//	if (r.message)
//		hide_field('profile')
//		refresh_field('profile');
//		console.log("helloo")
// }


//cur_frm.get_field("profile_user").get_query = function(doc) {
//	console.log("Hii...");
//	var qs="select name from `tabUser` where account_id='"+doc.account_id+"' and profile_user is not null"
//	console.log(qs);
//	a= "select p.name from`tabProfile` p,`tabUserRole` r,`tabDefaultValue` y where r.role='Franchise' AND y.defkey='account_id' AND y.defvalue='"+doc.account_id+"' AND r.parent=p.name AND p.name=y.parent AND p.enabled=1"
//        return a					
//}

