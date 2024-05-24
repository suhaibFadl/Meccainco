$('.star-rating label.star').on('click', function() {
    console.log('Running')

    const ratingValue = $(this).prev('input[type="radio"]').val();
    console.log('rating', ratingValue)
    $.ajax({
        url: rating_url,
        data: { 
            'businessType': businessType,
            'rating': ratingValue,
            'businessId': businessId,
         },
        success: function(response) {
            document.getElementById('rating').innerHTML = response.new_average
            if (response.success) {
                // Rating saved successfully, perform any necessary UI updates
                console.log('Rating saved successfully');
            } else {
                // Rating submission failed, handle the error
                console.error('Rating submission failed');
            }
        },
        error: function() {
            console.error('Error submitting rating');
        }
    });
    console.log('Selected rating: ' + ratingValue);
  });