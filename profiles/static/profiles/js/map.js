const count = JSON.parse(document.getElementById('branches_count').textContent); 
const branches = document.getElementsByClassName('branches'); 
console.log(branches)
mapboxgl.accessToken = 'pk.eyJ1Ijoic3VoYWliZmFkbDk4IiwiYSI6ImNsajNnM3duMjFoczYza3Q4ZjIxb2x4djgifQ.RZwpWD4Q-tYhp_iGpmLIog';
    const map = new mapboxgl.Map({
      container: 'map', // container ID
      style: 'mapbox://styles/mapbox/streets-v12', // style URL
      center: [17.189339372932267, 27.469072321807346], // centerstarting position [lng, lat]
      zoom: 4 // starting zoom
  });
var min_lat = 500
var max_lat = -500
var min_longt = 500
var max_longt = -500
for(var i = 0; i < branches.length; i++)
{
    var lat = parseFloat(branches[i].getElementsByClassName('lat')[0].value);
    var longt = parseFloat(branches[i].getElementsByClassName('longt')[0].value);
    console.log(lat, longt)
    if(lat < min_lat) min_lat = lat;
    if(lat > max_lat) max_lat = lat;
    if(longt < min_longt) min_longt = longt;
    if(longt > max_longt) max_longt = longt;
    const marker = new mapboxgl.Marker()
    .setLngLat([longt, lat])
    .addTo(map);
}

const longitude = (min_longt+max_longt)/2
const latitude =  (min_lat+max_lat)/2
const center = new mapboxgl.LngLat(longitude, latitude);
map.setCenter(center);