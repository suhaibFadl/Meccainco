console.log("exit")
const latitude= JSON.parse(document.getElementById('lat').textContent);
const longtitude= JSON.parse(document.getElementById('longt').textContent);
console.log(latitude, longtitude)
mapboxgl.accessToken = 'pk.eyJ1Ijoic3VoYWliZmFkbDk4IiwiYSI6ImNsajNnM3duMjFoczYza3Q4ZjIxb2x4djgifQ.RZwpWD4Q-tYhp_iGpmLIog';
const coordinates = document.getElementById('coordinates');
const map = new mapboxgl.Map({
container: 'map',
// Choose from Mapbox's core styles, or make your own style with Mapbox Studio
style: 'mapbox://styles/mapbox/streets-v12',
center: [ 
    longtitude,
    latitude
    ],
zoom: 10
});
 
const marker = new mapboxgl.Marker({
draggable: true
})
.setLngLat([longtitude, latitude])
.addTo(map);
 
function onDragEnd() {
const lngLat = marker.getLngLat();
coordinates.style.display = 'block';
coordinates.innerHTML = `Longitude: ${lngLat.lng}<br/>Latitude: ${lngLat.lat}`;
}
 
marker.on('dragend', onDragEnd);

// function get_address(lng, lat){
//   const longitude = lng; // Replace with your longitude
//   const latitude = lat; // Replace with your latitude
//   const accessToken = mapboxgl.accessToken; // Replace with your Mapbox access token
//   const geocodingUrl = `https://api.mapbox.com/geocoding/v5/mapbox.places/${longitude},${latitude}.json?access_token=${accessToken}`;
  
//   fetch(geocodingUrl)
//     .then(response => response.json()).then(data => {
//       // Access the reverse geocoding result
      
//       const address = data.features[0].place_name;
      
//       return address;
      
//     })
//     .catch(error => {
//       console.log(error);
//     });
// }

async function get_address(lng, lat) {
  const longitude = lng; // Replace with your longitude
  const latitude = lat; // Replace with your latitude
  const accessToken = mapboxgl.accessToken; // Replace with your Mapbox access token
  const geocodingUrl = `https://api.mapbox.com/geocoding/v5/mapbox.places/${longitude},${latitude}.json?access_token=${accessToken}`;

  try {
    const response = await fetch(geocodingUrl);
    const data = await response.json();

    const cityFeature = data.features.find(feature => feature.place_type.includes('region'));
    const countryFeature = data.features.find(feature => feature.place_type.includes('country'));

    // Extract city and country names from the features
    const city = cityFeature ? cityFeature.text : '';
    const country = countryFeature ? countryFeature.text : '';
    // Create an object with city and country properties
    const address = {
      city: city,
      country: country
    };

    return address; // Return the address object
  } catch (error) {
    throw error;
  }

}


$("#confirm-btn").click(function () {
  const lngLat = marker.getLngLat();
  // var addressObject = {}
  (async () => {
    try {
      const addressObject = await get_address(lngLat.lng, lngLat.lat);
      const address = addressObject; // Assign the object to a const variable
      $.ajax({                       
        url: url,                    
        data: {
          'locationId': locationId,
          'longitude': lngLat.lng,
          'latitude': lngLat.lat,
          'city': address.city,
          'country': address.country
        },
        success: function (data) {   
          document.referrer ? window.location = document.referrer : history.back()
        }
      });
    } catch (error) {
      console.log(error);
    }
  })();

});
