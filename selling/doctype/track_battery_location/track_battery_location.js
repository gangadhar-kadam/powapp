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

                        if (r.message=="Not"){
                          document.getElementById('map_canvas').style.display = 'none';
                          alert (" Item Not found ...!");
                          doc.customer_data='Item Not found ...!'
                          refresh_field('customer_data')

                        }
                        else if (r.message[0]=="admin"){
                          document.getElementById('map_canvas').style.display = 'none';
                          alert ("The item is in administrator warehouse '"+r.message[1]+"'...!");
                          doc.customer_data='The item is in administrator warehouse \n'+'Warehouse Name :- '+r.message[1]
                          refresh_field('customer_data')
                        }
                        else  if(r.message[0]=="sub franchise"){
                                doc.customer_data='Status :- Deliverd \n'+'Sub Franchise Name :- '+r.message[1]
                                document.getElementById('map_canvas').style.display = 'block';
                                var latLng = new google.maps.LatLng(r.message[2], r.message[3]);
                                var map = new google.maps.Map(document.getElementById('map_canvas'), {
                                zoom: 18,
                                center: latLng,
                                mapTypeId: google.maps.MapTypeId.ROADMAP
                                });
                                var marker = new google.maps.Marker({
                                 position: latLng,
                                 title: 'Point',
                                 map: map,
                                 draggable: true
                                });

                                refresh_field('customer_data')
                        }
                        else if(r.message[0]=="usr")
                        {
                        //console.log(r.message)
                        //console.log(r.message[1][0][0])
                        //console.log(r.message[1][0][1])
                        //console.log(r.message[2])
                        document.getElementById('map_canvas').style.display = 'none';
                        var ac=r.message[1][0][0].toLowerCase();
                        var pass=r.message[1][0][1].toLowerCase();
                        var device = r.message[2].toLowerCase();
                        console.log(ac)
                        console.log(pass)
                        console.log(device)
                        canop('POST', 'http://54.251.111.127:8080/PowerCap/ERPnext?page=map.device', {account:ac, password:pass, device:device},'_blank');
                        }
                        else if(r.message[0]=='Customer')
                        {
                                document.getElementById('map_canvas').style.display = 'none';
                                doc.customer_data='Status :- Deliverd \n'+'Customer Name :- '+r.message[1]+' \n Contact Number:- '+r.message[2]
                                refresh_field('customer_data')
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

