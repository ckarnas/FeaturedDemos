// // Function to determine marker size based on population
//Change to color to match the result
function markerSize(earthquake_size) {
    return 200;
}
  
function createMap(magnitudes, shootings) {

  //function createMap(shootings) {
    // Define streetmap and darkmap layers
    var streetmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?" +
      "access_token=pk.eyJ1IjoiY2thcm5hcyIsImEiOiJjamh4aHJzcXgwYndpM3dydmV6aHNtNXdqIn0.LkWE7jBeB8nZmUqZNLgLvg");
  
    var darkmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/dark-v9/tiles/256/{z}/{x}/{y}?" +
      "access_token=pk.eyJ1IjoiY2thcm5hcyIsImEiOiJjamh4aHJzcXgwYndpM3dydmV6aHNtNXdqIn0.LkWE7jBeB8nZmUqZNLgLvg");
  
    // Define a baseMaps object to hold our base layers
    var baseMaps = {
      "Street Map": streetmap,
      "Dark Map": darkmap
    };
  
    // Create overlay object to hold our overlay layer
    var overlayMaps = {
        Magnitudes: magnitudes,
        Shootings: shootings
    };
    console.log("++++++++++++++++")
    console.log(overlayMaps.Shootings)
    console.log(overlayMaps.Magnitudes)
    console.log("++++++++++++++")
    // Create our map, giving it the streetmap and earthquakes layers to display on load
    var myMap = L.map("map", {
      center: [
        35.2271,-80.8431
      ],
      zoom: 10,
      layers: [streetmap, magnitudes, shootings]
    });
  
  
  
  
    //Another Test...this plots the magnitude
    // sizeMarkers.forEach(function(element) {
    //   console.log(element);
    //   element.addTo(myMap);
    // });
  //Another Test
  
    // Create a layer control
    // Pass in our baseMaps and overlayMaps
    // Add the layer control to the map
    L.control.layers(baseMaps, overlayMaps, {
      collapsed: false
    }).addTo(myMap);
  }
  
  
  function createFeatures(shootingData) {
    console.log("I'm in createFeatures")
    console.log("This is shootingData: "+shootingData)
    var sizeMarkers = [];
    // Define a function we want to run once for each feature in the features array
    // Give each feature a popup describing the place and time of the earthquake
    function onEachFeature(feature, layer) {
        console.log("I'm in onEachFeature")
        layer.bindPopup("<h3>" + feature.properties.YEAR_MONTH +
            "</h3><hr><p>" + feature.properties.NARRATIVE + "</p>");
        
        var two_coords =[]
        two_coords.push(feature.properties.Longitude); 
        two_coords.push(feature.properties.Latitude); 
        console.log(two_coords);
        console.log("Year" +feature.properties.YR);
  
        
  
        sizeMarkers.push(
          L.circle(two_coords, {
            color: 'red',
            stroke: false,
            fillColor: '#f03',
            fillOpacity: 1,//(feature.properties.mag/5),
            radius: 50//markerSize(feature.properties.mag)
          })
        );
    }
    console.log("I'm still in createFeatures");
    // Create a GeoJSON layer containing the features array on the earthquakeData object
    // Run the onEachFeature function once for each piece of data in the array
    //onEachFeature(shootingData[0],L);
    var shootings = L.geoJSON(shootingData, {
      onEachFeature: onEachFeature
    });
    //myMap won't work because it is not here
    //L.geoJSON(shootingData,{onEachFeature: onEachFeature
    //}).addTo(myMap);
    console.log("If we were in onEachFeatures we would have this sizeMarker array filled: " + sizeMarkers);
    var magnitudes = L.layerGroup(sizeMarkers);
    console.log("magnitudes = " +magnitudes)
    //console.log("let's compare")
    console.log("If we were in onEachFeature we would have this shooting array filled: "+shootings)
    
    
    
        // Define streetmap and darkmap layers
        var streetmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?" +
        "access_token=pk.eyJ1IjoiY2thcm5hcyIsImEiOiJjamh4aHJzcXgwYndpM3dydmV6aHNtNXdqIn0.LkWE7jBeB8nZmUqZNLgLvg");
    
      var darkmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/dark-v9/tiles/256/{z}/{x}/{y}?" +
        "access_token=pk.eyJ1IjoiY2thcm5hcyIsImEiOiJjamh4aHJzcXgwYndpM3dydmV6aHNtNXdqIn0.LkWE7jBeB8nZmUqZNLgLvg");
    
      // Define a baseMaps object to hold our base layers
      var baseMaps = {
        "Street Map": streetmap,
        "Dark Map": darkmap
      };
    
      // Create overlay object to hold our overlay layer
      var overlayMaps = {
          Magnitudes: magnitudes,
          Shootings: shootings
      };
      console.log("++++++++++++++++")
      console.log(overlayMaps.Shootings)
      console.log(overlayMaps.Magnitudes)
      console.log("++++++++++++++")
      // Create our map, giving it the streetmap and earthquakes layers to display on load
      var myMap = L.map("map", {
        center: [
          35.2271,-80.8431
        ],
        zoom: 10,
        layers: [streetmap, magnitudes, shootings]
      });
    
      //L.geoJSON(shootingData,{onEachFeature: onEachFeature
      //  }).addTo(myMap);
      // Add the layer control to the map
      //L.control.layers(baseMaps, overlayMaps, {
      //  collapsed: false
      //}).addTo(myMap);
    
      var geojsonMarkerOptions = {
        radius: 800,
        fillColor: "#ff7800",
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
    };
    latlng=L.latLng(35.2273,-80.8431);
    L.geoJSON(shootingData.features).addTo(myMap);
    L.geoJSON(shootingData.features, {
        pointToLayer: function (feature, latlng) {
            return L.circleMarker(latlng, geojsonMarkerOptions);
        }
    }).addTo(myMap);
    
    function onEachFeature2(feature, layer) {
        // does this feature have a property named popupContent?
        console.log("CALLED************************************")
        if (feature.properties && feature.properties.popupContent) {
            layer.bindPopup(feature.properties.popupContent);
        }
    }
    
    var geojsonFeature = {
        "type": "Feature",
        "properties": {
            "name": "Coors Field",
            "amenity": "Baseball Stadium",
            "popupContent": "This is where the Rockies play!"
        },
        "geometry": {
            "type": "Point",
            "coordinates": [35.2271, -80.84]
        }
    };
    //var geojsonLayer = new L.GeoJSON.AJAX("http://clt-charlotte.opendata.arcgis.com/datasets/36b534fc414640fa843fc780f6d9aaf5_4.geojson", {onEachFeature:onEachFeature2});
    L.geoJSON(geojsonFeature, {
        onEachFeature2: onEachFeature2
    }).addTo(myMap);
    
    // Sending our earthquakes layer to the createMap function
    //createMap(magnitudes,shootings);
    //console.log(sizeMarkers)
  
  
  
  }
  
  
  
  
  // Store our API endpoint inside queryUrl
  //var queryUrl = "http://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=" +
  //  "2014-01-02&maxlongitude=-69.52148437&minlongitude=-123.83789062&maxlatitude=48.74894534&minlatitude=25.16517337";
  var queryUrl="data.geojson";
  //var geojsonLayer = new L.GeoJSON.AJAX("http://clt-charlotte.opendata.arcgis.com/datasets/36b534fc414640fa843fc780f6d9aaf5_4.geojson"
  //var queryUrl="https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson";
  // Perform a GET request to the query URL
  d3.json(queryUrl, function(data) {
    // Once we get a response, send the data.features object to the createFeatures function
    createFeatures(data.features);
  });
  
  
   
  