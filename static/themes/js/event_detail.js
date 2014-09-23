
// This example adds a search box to a map, using the Google Place Autocomplete
// feature. People can enter geographical searches. The search box will return a
// pick list containing a mix of places and predicted search terms.
var markersArray = [];
var map;
function initialize() {

  //var markers = [];
  map = new google.maps.Map(document.getElementById('map-event'), {
  //map = new google.maps.Map(document.getElementsByClassName('map-canvas'), {
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });
  
  var defaultBounds = new google.maps.LatLngBounds(
       new google.maps.LatLng(26.824071, -127.705078),
      new google.maps.LatLng(49.496675, -59.0625));
  map.fitBounds(defaultBounds);
  

  // Create the search box and link it to the UI element.
  var input = /** @type {HTMLInputElement} */(
      document.getElementById('pac-input1'));
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

  // [END region_getplaces]

  // Bias the SearchBox results towards places that are within the bounds of the
  // current map's viewport.



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

