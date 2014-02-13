cur_frm.cscript.track_battery_location=function(doc,cdt,cdn)
{
  doc.customer_data=''
  refresh_field('customer_data')
   //alert("in tracking location");
  wn.call({
	method: "manufacturing.doctype.production_order.production_order.get_detail1",
  args: {"serial_no":doc.barcode},
	callback: function(r) {
                if(r.message) {
			console.log(r.message[0])
                        if (r.message=="Not"){
                          alert (" Item Not found ...!");
                          doc.customer_data='Item Not found ...!'
                          refresh_field('customer_data')

                        }
                        else if (r.message[0]=="admin"){
                          alert ("The item is in administrator warehouse '"+r.message[1]+"'...!");
                          doc.customer_data='The item is in administrator warehouse \n'+'Warehouse Name :- '+r.message[1]
                          refresh_field('customer_data')
                        }
                        else  if(r.message[0]=="customer"){
				doc.customer_data='Status :- Deliverd \n'+'Customer Name :- '+r.message[1]
				refresh_field('customer_data')
			}
			else if(r.message[0]=="usr")
			{
                        console.log(r.message)
                        console.log(r.message[1][0][0])
                        console.log(r.message[1][0][1])
                        console.log(r.message[2])
                        var ac=r.message[1][0][0].toLowerCase();
                        var pass=r.message[1][0][1].toLowerCase();
                        var device = r.message[2].toLowerCase();
                        canop('POST', 'http://54.251.111.127:8080/PowerCap/ERPnext?page=map.device', {account:ac, password:pass, device:device},'_blank');
                        }
			
                        
                }
                }
        });
}

function canop(verb, url, data, target) {

var form = document.createElement("form");
form.action = url;
form.method = verb;
form.target = target || "_blank";
if (data) {
for (var key in data) {
  var input = document.createElement("input");
  input.name = key;
  //alert(data[key]);
  input.value = data[key];
  form.appendChild(input);
}
}
form.style.display = 'none';
document.body.appendChild(form);
form.submit();
};

