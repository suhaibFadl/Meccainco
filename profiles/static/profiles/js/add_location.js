console.log("exit")
mapboxgl.accessToken = 'pk.eyJ1Ijoic3VoYWliZmFkbDk4IiwiYSI6ImNsajNnM3duMjFoczYza3Q4ZjIxb2x4djgifQ.RZwpWD4Q-tYhp_iGpmLIog';
const coordinates = document.getElementById('coordinates');
const map = new mapboxgl.Map({
container: 'map',
// Choose from Mapbox's core styles, or make your own style with Mapbox Studio
style: 'mapbox://styles/mapbox/streets-v12',
center: [ 
    13.177064886055632,
    32.896667501832155
    ],
zoom: 5
});
 
const marker = new mapboxgl.Marker({
draggable: true
})
.setLngLat([13.177064886055632, 32.896667501832155])
.addTo(map);
 
function onDragEnd() {
const lngLat = marker.getLngLat();
coordinates.style.display = 'block';
coordinates.innerHTML = `Longitude: ${lngLat.lng}<br />Latitude: ${lngLat.lat}`;
}
 
marker.on('dragend', onDragEnd);

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
    (async () => {
      try {
        const addressObject = await get_address(lngLat.lng, lngLat.lat);
        const address = addressObject; // Assign the object to a const variable
        console.log(address.city);
        $.ajax({                       
          url: url,                    
          data: {
            'branchId': branchId,
            'businessType': businessType,
            'longitude': lngLat.lng,
            'latitude': lngLat.lat,
            'city': address.city,
            'country': address.country
          },
          success: function (data) {   
            document.referrer ? window.location = document.referrer : history.back()
          }
        });
        // Now you can use the address variable outside the function
        // console.log(address.city);    // Access the city name
        // console.log(address.country); // Access the country name
      } catch (error) {
        console.log(error);
      }
    })();
    
});
