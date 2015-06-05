cur_frm.cscript.onload=function(doc,cdt,cdn){
	$("#map_canvas" ).remove();
	$(cur_frm.get_field("lon").wrapper).append('<div id="map_canvas" style="width: 1000px; height: 400px;margin-left:25%"></div>');
    ip = $(this.frm.parent)[0].childNodes[6].childNodes[5].childNodes[1].childNodes[1].childNodes[0].childNodes[4].childNodes[2].childNodes[0].childNodes[1].childNodes[2].childNodes[1].childNodes[3].childNodes[1]
    var d = '';
	if (doc.lat){
		cur_frm.cscript.create_pin_on_map(doc,doc.lat,doc.lon)
	}
	else{
		cur_frm.doc.address='Pune ,india'
		cur_frm.cscript.address(doc,cdt,cdn)
    }
}

cur_frm.cscript.create_pin_on_map=function(doc,lat,lon){
        var latLng = new google.maps.LatLng(lat, lon);
        var map = new google.maps.Map(document.getElementById('map_canvas'), {
            zoom: 12,
            center: latLng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
          });
        var marker = new google.maps.Marker({
            position: latLng,
            title: 'Point',
            map: map,
            draggable: true
          });

        updateMarkerPosition(latLng);
        geocodePosition(latLng);

        google.maps.event.addListener(marker, 'dragstart', function() {
            updateMarkerAddress('Dragging...');
        });

        google.maps.event.addListener(marker, 'drag', function() {
            updateMarkerStatus('Dragging...');
            updateMarkerPosition(marker.getPosition());
        });

        google.maps.event.addListener(marker, 'dragend', function() {
            updateMarkerStatus('Drag ended');
            geocodePosition(marker.getPosition());
          });
}

function geocodePosition(pos) {
      geocoder.geocode({
        latLng: pos
      }, function(responses) {
        if (responses && responses.length > 0) {
          updateMarkerAddress(responses[0].formatted_address);
        } else {
          if(doc.__islocal) {
            alert('Cannot determine address at this location.');
          }
        }
      });
      geocoder.geocode( { 'address': doc.address}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        doc.lat=results[0].geometry.location.lat();
        doc.lon=results[0].geometry.location.lng();
        refresh_field('lat')
        refresh_field('lon')
      } 
    });
}

function updateMarkerAddress(str) {
  doc=cur_frm.doc
  doc.address= str;
  refresh_field('address');
}

function updateMarkerStatus(str) {
var s=1;
}

function updateMarkerPosition(latLng) {
  doc=cur_frm.doc
  doc.lat=latLng.lat()
  doc.lon=latLng.lng()
  refresh_field('lat')
  refresh_field('lon')
}

var geocoder = new google.maps.Geocoder();

var getMarkerUniqueId= function(lat, lng) {
    return lat + '_' + lng;
}

var getLatLng = function(lat, lng) {
     return new google.maps.LatLng(lat, lng);
};

cur_frm.cscript.address = function(doc, dt, dn){
      geocoder.geocode( { 'address': doc.address}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
          doc.address=results[0].formatted_address;
          refresh_field('address');
          var latLng = new google.maps.LatLng(results[0].geometry.location.lat(), results[0].geometry.location.lng());

          var map = new google.maps.Map(document.getElementById('map_canvas'), {
              zoom: 12,
              center: latLng,
              mapTypeId: google.maps.MapTypeId.ROADMAP
            });

          var marker = new google.maps.Marker({
              position: latLng,
              title: 'Point',
              map: map,
              draggable: true
            });
          updateMarkerPosition(latLng);
          geocodePosition(latLng);

          google.maps.event.addListener(marker, 'dragend', function() {
              geocodePosition(marker.getPosition());
          });
      } else {
        alert("Geocode was not successful for the following reason: " + status);
      }
    });
}

cur_frm.fields_dict['region'].get_query = function(doc, cdt, cdn) {
        return "select name from `tabTerritory` where parent_territory='All Territories' and is_group='No'"
}

cur_frm.cscript.email = function(doc, dt, dn) {
   var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
   check=re.test(doc.email)
   if(check==false)
   {
        cur_frm.set_value("email_id", '')
        msgprint("Please Enter valid Email Id..! ");
        throw "Please Enter Correct Email ID!"
   }

}

