/**
 * Created by asus on 06.03.18.
 */
socket.on('newnumber', function(data){
    lat = data.number[0];
    lng = data.number[1];

    $('#locationText').text(data.number[3]);
    console.log("Lat: " + lat + " Long: " + lng);

    // Construct new LatLong Object
    var myLatlng = new google.maps.LatLng(lng, lat);
    latLong = myLatlng;

    // Draw marker on the map
    var marker = new google.maps.Marker({
        position: myLatlng,
        map: map,
        title: data.number[3]
    });
    // Move map to new coordinates w/o refreshing page
    map.panTo(latLong);
});