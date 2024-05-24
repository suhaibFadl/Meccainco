const start_lat= JSON.parse(document.getElementById('start_lat').textContent);
const destination_lat= JSON.parse(document.getElementById('destination_lat').textContent);
const start_longt= JSON.parse(document.getElementById('start_longt').textContent);
const destination_longt= JSON.parse(document.getElementById('destination_longt').textContent);
console.log(start_lat, start_longt)
console.log(destination_lat, destination_longt)
mapboxgl.accessToken = 'pk.eyJ1Ijoic3VoYWliZmFkbDk4IiwiYSI6ImNsajNnM3duMjFoczYza3Q4ZjIxb2x4djgifQ.RZwpWD4Q-tYhp_iGpmLIog';
    const map = new mapboxgl.Map({
      container: 'map', // container ID
      style: 'mapbox://styles/mapbox/streets-v12', // style URL
      center: [(start_longt + destination_longt)/2, (start_lat + destination_lat)/2], // centerstarting position [lng, lat]
      zoom: 7 // starting zoom
  });

const marker = new mapboxgl.Marker()
  .setLngLat([destination_longt, destination_lat])
  .addTo(map);

//   const bounds = [
//   [-123.069003, 45.395273],
//   [-122.303707, 45.612333]
//   ];
  //map.setMaxBounds(bounds);
  const start = [start_longt, start_lat];
  const destination =  [destination_longt, destination_lat]

  async function getRoute(end) {
    // make a directions request using cycling profile
    // an arbitrary start will always be the same
    // only the end or destination will change
    const query = await fetch(
      `https://api.mapbox.com/directions/v5/mapbox/cycling/${start[0]},${start[1]};${end[0]},${end[1]}?steps=true&geometries=geojson&access_token=${mapboxgl.accessToken}`,
      { method: 'GET' }
    );
    const json = await query.json();
    const data = json.routes[0];
    const route = data.geometry.coordinates;
    const geojson = {
      type: 'Feature',
      properties: {},
      geometry: {
        type: 'LineString',
        coordinates: route
      }
    };
    // if the route already exists on the map, we'll reset it using setData
    if (map.getSource('route')) {
      map.getSource('route').setData(geojson);
    }
    // otherwise, we'll make a new request
    else {
      map.addLayer({
        id: 'route',
        type: 'line',
        source: {
          type: 'geojson',
          data: geojson
        },
        layout: {
          'line-join': 'round',
          'line-cap': 'round'
        },
        paint: {
          'line-color': '#f30',
          'line-width': 5,
          'line-opacity': 0.50
        }
      });
    }
    // add turn instructions here at the end
  }
  
  map.on('load', () => {
    // make an initial directions request that
    // starts and ends at the same location
    getRoute(start);
  
    // Add starting point to the map
    map.addLayer({
      id: 'point',
      type: 'circle',
      source: {
        type: 'geojson',
        data: {
          type: 'FeatureCollection',
          features: [
            {
              type: 'Feature',
              properties: {},
              geometry: {
                type: 'Point',
                coordinates: start
              }, 
            },
          ]
        }
      },
      paint: {
        'circle-radius': 10,
        'circle-color': '#3887be'
      }
    });
    // this is where the code from the next step will go
    
    map.addLayer({
        id: 'end',
        type: 'circle',
        source: {
          type: 'geojson',
          data: {
            type: 'FeatureCollection',
            features: [
              {
                type: 'Feature',
                properties: {},
                geometry: {
                  type: 'Point',
                  coordinates: destination
                }
              }
            ]
          }
        },
        paint: {
          'circle-radius': 10,
          'circle-color': '#f30'
        }
      });
  });

  
  function direction(){
      getRoute(destination);
  }


  // var geocoder = new mapboxgl.mapboxGeocoder({
  //   accessToken: mapboxgl.accessToken,
  //   marker: false
  // });
  
  // var coordinates = start; // Replace with your specific coordinates
  
  // geocoder.query({ coordinates: coordinates }, function (error, result) {
  //   if (error) {
  //     console.log(error);
  //     return;
  //   }
  
  //   // Access the reverse geocoding result
  //   var address = result.features[0].place_name;
  //   console.log(address);
  // });

  const longitude = -122.4194; // Replace with your longitude
  const latitude = 37.7749; // Replace with your latitude
  const accessToken = mapboxgl.accessToken; // Replace with your Mapbox access token
const geocodingUrl = `https://api.mapbox.com/geocoding/v5/mapbox.places/${longitude},${latitude}.json?access_token=${accessToken}`;

fetch(geocodingUrl)
  .then(response => response.json()).then(data => {
    // Access the reverse geocoding result
    console.log(data);
    const address = data.features[0].place_name;
    console.log(address);
  })
  .catch(error => {
    console.log(error);
  });