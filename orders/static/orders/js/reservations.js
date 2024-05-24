$("#id_brand").change(function () {
    var url = $("#personForm").attr("data-parts-url");  // get the url of the `load_cities` view
    var brandId = $(this).val();  // get the selected country ID from the HTML input
    $.ajax({                       // initialize an AJAX request
      url: url,                    // set the url of the request (= localhost:8000/hr/ajax/load-cities/)
      data: {
        'brand': brandId       // add the country id to the GET parameters
      },
      success: function (data) {   // `data` is the return of the `load_cities` view function
        $("#id_car").html(data);  // replace the contents of the city input with the data that came from the server
      }
    });

  });

  function confirmReservation() {
    var dateInput = document.getElementById('newDate');
    var timeInput = document.getElementById('newTime');
    var datetimeError = document.getElementById('datetimeError');

    var currentDate = new Date(); // Get the current date and time
    var selectedDate = new Date(dateInput.value + 'T' + timeInput.value);

    if (selectedDate < currentDate) {
        datetimeError.textContent = 'Please select a date and time in the future.';
        return;
    }

    var date = dateInput.value;
    var time = timeInput.value;

    if (!date || !time) {
        datetimeError.textContent = 'Please select both a date and a time.';
        return;
    }

    // Validate the date format (YYYY-MM-DD)
    var dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(date)) {
        datetimeError.textContent = 'Invalid date format.';
        return;
    }

    // Validate the time format (HH:mm)
    var timeRegex = /^\d{2}:\d{2}$/;
    if (!timeRegex.test(time)) {
        datetimeError.textContent = 'Invalid time format.';
        return;
    }

    // Combine the date and time into a single datetime string
    var datetime = date + 'T' + time;

    // Clear any previous error messages
    datetimeError.textContent = '';

    $.ajax({
        url: confirm_reservation_url,
        data: {
            'reservationId': reservationId,
            'time': datetime,
        },
        success: function (data) {
          location.reload(); 
        },
    });
}

// Attach the confirmReservation function to a button click event
document.getElementById('confirmButton').addEventListener('click', function () {
    confirmReservation();
});



function update_reservation(new_status) {
  $.ajax({  
    url: update_reservation_url,
    data: {
        'reservationId': reservationId,
        'status': new_status,
    },
    success: function (data) {
      location.reload(); 
    }
  });

};