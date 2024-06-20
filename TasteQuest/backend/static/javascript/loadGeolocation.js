window.addEventListener('load', function() {
    console.log("HIIIIIII");
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;

            // Get CSRF token from the DOM
            var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            // Send location data to server using AJAX
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/save_location/', true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.setRequestHeader('X-CSRFToken', csrftoken); // Set CSRF token in the request header
            xhr.onload = function() {
                if (xhr.status === 200) {
                    console.log('Location saved successfully');
                } else {
                    console.error('Error saving location:', xhr.statusText);
                }
            };
            xhr.send('latitude=' + latitude + '&longitude=' + longitude);
        });
    } else {
        console.error("Geolocation is not supported by this browser");
    }
});