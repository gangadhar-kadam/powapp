cur_frm.cscript.track_battery_location=function(doc,cdt,cdn)
{
   //alert("in tracking location");
  wn.call({
	method: "manufacturing.doctype.production_order.production_order.get_detail1",
  args: {"serial_no":doc.barcode},
	callback: function(r) {
                if(r.message) {
                        if (r.message=="Not"){
                          alert (" Item Not found or you don't have permission for view ...!");
                        }
                        else if (r.message=="adm"){
                          alert ("The item is in administrator warehouse 'Finished Goods - P'...!");
                        }
                        else {
                        console.log(r.message)
                        console.log(r.message[0][0][0])
                        console.log(r.message[0][0][1])
                        console.log(r.message[1])
                        var ac=r.message[0][0][0].toLowerCase();
                        var pass=r.message[0][0][1].toLowerCase();
                        var device = r.message[1].toLowerCase();
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

