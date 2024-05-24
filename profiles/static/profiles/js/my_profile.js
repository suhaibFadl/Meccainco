const latitude= JSON.parse(document.getElementById('lat').textContent);
const longtitude= JSON.parse(document.getElementById('longt').textContent);
mapboxgl.accessToken = 'pk.eyJ1Ijoic3VoYWliZmFkbDk4IiwiYSI6ImNsajNnM3duMjFoczYza3Q4ZjIxb2x4djgifQ.RZwpWD4Q-tYhp_iGpmLIog';
const map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v12', // style URL
    center: [longtitude, latitude], // centerstarting position [lng, lat]
    zoom: 7 // starting zoom
  });

const marker = new mapboxgl.Marker()
    .setLngLat([longtitude, latitude])
    .addTo(map);