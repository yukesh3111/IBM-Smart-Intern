let total_distance = 0;

function showNearbyChargingStations() {
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(function (position) {
      var latitude = position.coords.latitude;
      var longitude = position.coords.longitude;

      // Construct Google Maps URL with the current location and search query for EV charging stations
      var googleMapsUrl = `https://www.google.com/maps/search/EV+charging+stations/@${latitude},${longitude},15z`;

      // Open the Google Maps URL in a new window/tab
      window.open(googleMapsUrl, "_blank");
    });
  } else {
    alert("Geolocation is not available in this browser.");
  }
}
function finder() {
  let source = document.querySelector("#source");
  let destination = document.querySelector("#destination");
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);

  var sourceName = source.value; // Source location name
  var destinationName = destination.value; // Destination location name

  // Use Nominatim for geocoding
  function geocodeLocation(locationName, callback) {
    fetch(
      "https://nominatim.openstreetmap.org/search?q=" +
        encodeURIComponent(locationName) +
        "&format=json"
    )
      .then((response) => response.json())
      .then((data) => {
        if (data.length > 0) {
          var lat = parseFloat(data[0].lat);
          var lon = parseFloat(data[0].lon);
          callback(L.latLng(lat, lon));
          errormessage2.innerHTML = "";
        } else {
          errormessage2.innerHTML = "Location not found. Please refer map";
        }
      });
  }

  geocodeLocation(sourceName, function (source) {
    var sourceLatLng = source;
    geocodeLocation(destinationName, function (destination) {
      var destinationLatLng = destination;

      var routingControl = L.Routing.control({
        waypoints: [L.latLng(sourceLatLng), L.latLng(destinationLatLng)],
        routeWhileDragging: true,
      }).addTo(map);

      routingControl.on("routesfound", function (e) {
        var route = e.routes[0];
        distance = route.summary.totalDistance; // Distance in meters
        total_distance = (distance / 1000).toFixed(2);
      });
    });
  });
}
function cost() {
  let errormessage = document.querySelector("#errormessage");
  let cost_balance_distance_kilowatt = document.querySelector(
    "#cost_balance_distance_kilowatt"
  );
  let kilowatt_requied = document.querySelector("#kilowatt_requied");
  let distance_balance = document.querySelector("#distance_cover");
  let costperkwatt = 6;
  let kwattperkm = 0.0761;
  let kmperkwatt = 13.125;
  let total = parseInt(document.querySelector("#total").innerHTML);
  console.log(total);
  let remain_persent = parseInt(document.querySelector("#remain").value);
  console.log(remain_persent);
  balance_watt = ((remain_persent / 100) * total).toFixed(2);
  console.log(distance_balance.innerHTML);
  let source = document.querySelector("#source");
  let destination = document.querySelector("#destination");
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);

  var sourceName = source.value; // Source location name
  var destinationName = destination.value; // Destination location name

  // Use Nominatim for geocoding
  function geocodeLocation(locationName, callback) {
    fetch(
      "https://nominatim.openstreetmap.org/search?q=" +
        encodeURIComponent(locationName) +
        "&format=json"
    )
      .then((response) => response.json())
      .then((data) => {
        if (data.length > 0) {
          var lat = parseFloat(data[0].lat);
          var lon = parseFloat(data[0].lon);
          callback(L.latLng(lat, lon));
        } else {
          errormessage.innerHTML = "Location not found.";
          distance_balance.innerHTML = "";
        }
      });
  }

  geocodeLocation(sourceName, function (source) {
    var sourceLatLng = source;
    geocodeLocation(destinationName, function (destination) {
      var destinationLatLng = destination;

      var routingControl = L.Routing.control({
        waypoints: [L.latLng(sourceLatLng), L.latLng(destinationLatLng)],
        routeWhileDragging: true,
      }).addTo(map);

      routingControl.on("routesfound", function (e) {
        var route = e.routes[0];
        distance = route.summary.totalDistance; // Distance in meters
        total_distance = (distance / 1000).toFixed(2);
        balance_distance = (
          total_distance - distance_balance.innerHTML
        ).toFixed(2);
        kilowatt_requied.innerHTML =
          (balance_distance * kwattperkm).toFixed(2) +
          "  Kilowatts required for balance distance";
        cost_balance_distance_kilowatt.innerHTML =
          "₹ " +
          ((balance_distance * kwattperkm).toFixed(2) * costperkwatt).toFixed(
            2
          ) +
          "  Cost required for balance distance";
        distance_balance.innerHTML =
          (balance_watt * kmperkwatt).toFixed(2) +
          "  km Distance cover by balance percentage of battery";
        console.log(balance_distance);
        console.log(kilowatt_requied);
        console.log(cost_balance_distance_kilowatt);
        if (kilowatt_requied.innerHTML > 0) {
          errormessage.innerHTML = "";
        }
        console.log((kilowatt_requied.innerHTML * costperkwatt).toFixed(2));
      });
    });
  });
}
document
  .getElementById("trip-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const destinationInput = document.getElementById("destination");
    const dateInput = document.getElementById("date");
    const destinationList = document.getElementById("destination-list");

    const destination = destinationInput.value;
    const date = dateInput.value;

    const listItem = document.createElement("li");
    listItem.textContent = `Destination: ${destination}, Date: ${date}`;
    destinationList.appendChild(listItem);

    destinationInput.value = "";
    dateInput.value = "";
  });
