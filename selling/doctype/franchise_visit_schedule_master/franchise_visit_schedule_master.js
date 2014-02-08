
cur_frm.cscript.generate = function(doc, dt, dn)  {
	console.log("inside generate...")
//     console.log([doc.code_contact,"Hello"])
	return wn.call({ 
		method: "selling.doctype.franchise_visit_schedule_master.franchise_visit_schedule_master.generate_visiting_schedule",
//             args: {
//                     verification_code: doc.code_contact,
//                       user_agent: doc.user_agent
//             }
	});
}
