pos = $(this.frm.parent)[0].childNodes[6].childNodes[5].childNodes[1].childNodes[1].childNodes[0].childNodes[4].childNodes[2].childNodes[0].childNodes[1]
$('<div id="map_canvas" style="width:550px; height:400px;margin-left:15%">HTML</div>').appendTo(pos);

ip = $(this.frm.parent)[0].childNodes[6].childNodes[5].childNodes[1].childNodes[1].childNodes[0].childNodes[4].childNodes[2].childNodes[0].childNodes[1].childNodes[2].childNodes[1].childNodes[3].childNodes[1]
var d = '';
ip.onkeypress=function(e){
		d = e.which
		//console.log($($(ip)[0]))
		cur_frm.cscript.map(e);
};

var myMarker= [];

cur_frm.cscript.onload=function(doc,cdt,cdn){
	//if(doc.__islocal){
	var o = new gmap(doc);
	cur_frm.cscript.create_pin_on_map(doc,doc.lat,doc.lon)
	//}
}

 cur_frm.cscript.create_pin_on_map=function(doc,lat,lon){
	var latLng = new google.maps.LatLng(lat, lon);
        var map = new google.maps.Map(document.getElementById('map_canvas'), {

    zoom: 13,

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
   // console.log(responses);
    if (responses && responses.length > 0) {
      updateMarkerAddress(responses[0].formatted_address);

    } else {
      if(doc.__islocal) {
console.log(responses.length);
      alert('Cannot determine address at this location.');
            }
    }

  });

}

function updateMarkerAddress(str) {
  doc=cur_frm.doc
  doc.address= str;
  refresh_field('address')

}

function updateMarkerStatus(str) {
var s=1;

}

function updateMarkerPosition(latLng) {
  doc=cur_frm.doc
  console.log(["update",latLng,doc.lat,doc.lon,latLng.lat(),latLng.lng()])
  doc.lat=latLng.lat()
  doc.lon=latLng.lng()
  console.log([doc.lat,doc.lon,doc.name])
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
	
cur_frm.cscript.map =function(doc, dt, dn){
	var searchBox;
	ip = $(this.frm.parent)[0].childNodes[6].childNodes[5].childNodes[1].childNodes[1].childNodes[0].childNodes[4].childNodes[2].childNodes[0].childNodes[1].childNodes[2].childNodes[1].childNodes[3].childNodes[1].childNodes

	geocoder.geocode( { 'address': cstr(cur_frm.doc.state)}, function(results, status) {
		  	 var latlong = results[0].geometry.location
		  	 cur_frm.cscript.callback(doc, dt, dn, latlong, ip)
		});
 }

cur_frm.cscript.callback = function(doc, dt, dn, ltln, ip){
	var latlong = new google.maps.LatLngBounds(new google.maps.LatLng(ltln.lb , ltln.mb));
	var options = {componentRestrictions: {country: 'in'}, bounds: latlong};
	var searchBox = new google.maps.places.Autocomplete(ip[0],options);
	console.log(searchBox)
	var o=new gmap(this.frm.doc);
	o.get_map(searchBox);

	var plc;
	google.maps.event.addListener(searchBox, 'place_changed', function() {
		var place = searchBox.getPlace();
		var doc=cur_frm.doc
		//cur_frm.cscript.create_pin_on_map(doc,place.geometry.location.d,place.geometry.location.e)		
		//cur_frm.set_value('lat',place.geometry.location.d)
		//cur_frm.set_value('lon',place.geometry.location.e)
		//cur_frm.set_value("address", place.formatted_address)
		console.log([place.formatted_address, place.geometry.location.B, place.geometry.location.k])
		cur_frm.cscript.create_pin_on_map(doc,place.geometry.location.k,place.geometry.location.B)		
		cur_frm.set_value('lat',place.geometry.location.k)
		cur_frm.set_value('lon',place.geometry.location.B)
		cur_frm.set_value("address", place.formatted_address)
	});

}

cur_frm.cscript.state = function(doc, dt, dn){
 	var o = new gmap(this.frm.doc);
 		o.codeAddress(doc.state)	
 }


var geocoder;
var map;
var markers = [];
gmap = Class.extend({
	init: function(doc) {
		me= this;
		geocoder = new google.maps.Geocoder();
		var latlng = new google.maps.LatLng(18.0623, 73.8940);
		var myOptions = {
			zoom: 6,
			center: latlng,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		};
		map = new google.maps.Map($("#map_canvas")[0], myOptions);
		me.successFunction(doc.address, map)
	},
	successFunction: function(position, map) {
		geocoder.geocode( { 'address': cstr(position)}, function(results, status) {

		  	map.setCenter(results[0].geometry.location);
			var marker = new google.maps.Marker({
			    map: map, 
			    position: results[0].geometry.location
			});
			markers.push(marker);
			map.setZoom(14);
		}); 
	},
	setAllMap: function(map) {
		for (var i = 0; i < markers.length; i++) {
			markers[i].setMap(map);
		}
	},
	clearOverlays: function (map) {
		this.setAllMap(map);
	},
	showOverlays: function () {
		this.setAllMap(map);
	},
	deleteOverlays: function (map) {
		this.clearOverlays(map);
		markers = [];
	},
	get_map:function(searchBox){
	var markers = [];  searchBox.bindTo('bounds', map);
		  var doc=cur_frm.doc
		   
		  var infowindow = new google.maps.InfoWindow();
		  var marker = new google.maps.Marker({
		    map: map
		  });

		  google.maps.event.addListener(searchBox, 'place_changed', function() {
		    infowindow.close();
		    marker.setVisible(false);
		    searchBox.className = '';
		    var place = searchBox.getPlace();
		    if (!place.geometry) {
		      searchBox.className = 'notfound';
		      return;
		    }

		    if (place.geometry.viewport) {
		      map.fitBounds(place.geometry.viewport);
		    } else {
		      map.setCenter(place.geometry.location);
		      map.setZoom(10);
		    }
		    marker.setIcon(({
		      url: place.icon,
		      size: new google.maps.Size(71, 71),
		      origin: new google.maps.Point(0, 0),
		      anchor: new google.maps.Point(17, 34),
		      scaledSize: new google.maps.Size(35, 35)
		    }));
		    marker.setPosition(place.geometry.location);
		    marker.setVisible(true);

		    var address = '';
		    if (place.address_components) {
		      address = [
		        (place.address_components[0] && place.address_components[0].short_name || ''),
		        (place.address_components[1] && place.address_components[1].short_name || ''),
		        (place.address_components[2] && place.address_components[2].short_name || '')
		      ].join(' ');
		    }

		    infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + address);
		    infowindow.open(map, marker);
		  });

		  
	},
	codeAddress: function (addr,str) {
		console.log(addr)
		me= this;
		var sAddress = addr
		geocoder.geocode( { 'address': sAddress}, function(results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				map.setCenter(results[0].geometry.location);
				var marker = new google.maps.Marker({
				    map: map, 
				    position: results[0].geometry.location
				});
				markers.push(marker);
				map.setZoom(6);
			} 
			else {
				alert("Geocode was not successful for the following reason: " + status);
			}
		});
	}
});


