const lat = JSON.parse(document.getElementById('lat').textContent); 
const longt = JSON.parse(document.getElementById('longt').textContent); 
const stores = document.getElementsByClassName('stores'); 

console.log(longt, lat)
mapboxgl.accessToken = 'pk.eyJ1Ijoic3VoYWliZmFkbDk4IiwiYSI6ImNsajNnM3duMjFoczYza3Q4ZjIxb2x4djgifQ.RZwpWD4Q-tYhp_iGpmLIog';
    const map = new mapboxgl.Map({
      container: 'map', // container ID
      style: 'mapbox://styles/mapbox/streets-v12', // style URL
      center: [longt, lat], // centerstarting position [lng, lat]
      zoom: 13 // starting zoom
  });

const marker = new mapboxgl.Marker()
.setLngLat([longt, lat])
.addTo(map);