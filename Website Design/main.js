function getLocation(){
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(showPosition);
    }
    else{
        document.getElementById("").innerHTML = "Didnt work"
    }
}
function showPosition(position) {
    document.getElementById("").innerHTML = "Latitude: " + position.coords.latitude +
        "<br>Longitude: " + position.coords.longitude;
}