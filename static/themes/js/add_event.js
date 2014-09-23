
// This example adds a search box to a map, using the Google Place Autocomplete
// feature. People can enter geographical searches. The search box will return a
// pick list containing a mix of places and predicted search terms.
var markersArray = [];
var map;
function initialize() {

  //var markers = [];
  map = new google.maps.Map(document.getElementById('map-canvas'), {
  //map = new google.maps.Map(document.getElementsByClassName('map-canvas'), {
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });
  
  var defaultBounds = new google.maps.LatLngBounds(
       new google.maps.LatLng(26.824071, -127.705078),
      new google.maps.LatLng(49.496675, -59.0625));
  map.fitBounds(defaultBounds);
  

  // Create the search box and link it to the UI element.
  var input = /** @type {HTMLInputElement} */(
      document.getElementById('pac-input'));
	  //document.getElementsByClassName('pac-input'));
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  var searchBox = new google.maps.places.SearchBox(
    /** @type {HTMLInputElement} */(input));
	
	if(($( '#lat' ).val() != "") && ($( '#lon' ).val() != "")) {
	//alert("here");
	var latLng = new google.maps.LatLng(parseFloat($( '#lat' ).val()), parseFloat($( '#lon' ).val()));
	console.log(latLng);
	placeMarker(latLng);
  }
  // [START region_getplaces]
  // Listen for the event fired when the user selects an item from the
  // pick list. Retrieve the matching places for that item.
  google.maps.event.addListener(searchBox, 'places_changed', function() {
    var places = searchBox.getPlaces();

    for (var i = 0, marker; marker = markersArray[i]; i++) {
      marker.setMap(null);
    }

    // For each place, get the icon, place name, and location.
    markersArray = [];
    var bounds = new google.maps.LatLngBounds();
    for (var i = 0, place; place = places[i]; i++) {
      var image = {
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25)
      };

      //Create a marker for each place.
      var marker = new google.maps.Marker({
        map: map,
        //icon: image,
        //title: place.name,
        position: place.geometry.location
      });
      console.log( place.geometry.location.lat() +" "+ place.geometry.location.lng())
      // var marker = new google.maps.Marker({
      //           position: location, 
      //           map: map
      //       });
	  $( '#lat' ).attr( "value", place.geometry.location.lat());
	  //$('#lat').val() = place.geometry.location.lat().toString();
	  $( '#lon' ).attr( "value", place.geometry.location.lng());
	  //$('#lon').val() = place.geometry.location.lng().toString();
      markersArray.push(marker);

      bounds.extend(place.geometry.location);
    }

    map.fitBounds(bounds);
  });
  // [END region_getplaces]

  // Bias the SearchBox results towards places that are within the bounds of the
  // current map's viewport.
  google.maps.event.addListener(map, 'bounds_changed', function() {
    var bounds = map.getBounds();
    searchBox.setBounds(bounds);
  });


            // add a click event handler to the map object
            google.maps.event.addListener(map, "click", function(event)
            {
                //alert("hello");
                // place a marker
                 placeMarker(event.latLng);
				 console.log(event.latLng);

                // // display the lat/lng in your form's lat/lng fields
                //document.getElementById("latFld").value = event.latLng.lat();
                //document.getElementById("lngFld").value = event.latLng.lng();
                console.log(event.latLng.lat()+ " "+event.latLng.lng());
				$( '#lat' ).attr( "value", event.latLng.lat());
				//$('#lat').val() = event.latLng.lat().toString();
				//$('#lon').val() = event.latLng.lng().toString();
				$( '#lon' ).attr( "value", event.latLng.lng());
            });


}
function placeMarker(location) {
			
            // first remove all markers if there are any
            deleteOverlays();

            var marker = new google.maps.Marker({
                position: location, 
                map: map
            });

            // add marker in markers array
            markersArray.push(marker);

            //map.setCenter(location);
        }

        // Deletes all markers in the array by removing references to them
        function deleteOverlays() {
            if (markersArray) {
                for (i in markersArray) {
                    markersArray[i].setMap(null);
                }
            markersArray.length = 0;
            }
        }

google.maps.event.addDomListener(window, 'load', initialize);

