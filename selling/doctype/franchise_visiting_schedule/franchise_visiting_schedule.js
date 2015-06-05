cur_frm.fields_dict['regions'].get_query = function(doc, cdt, cdn) {
        return "select name from `tabTerritory` where parent_territory='All Territories' and is_group='No'"
}


//cur_frm.cscript.generate = function(doc, dt, dn)  {
//	console.log("inside generate...")
//		return wn.call({
//			method: "selling.doctype.franchise_visiting_schedule.franchise_visiting_schedule.on_update1",
//		});
//}

