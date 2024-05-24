$('.star-rating label.star').on('click', function() {
    const ratingValue = $(this).prev('input[type="radio"]').val();
    const productId = $(this).parent('.star-rating').data('product-id');
    console.log('rating', ratingValue)
    $.ajax({
        url: rating_url,
        data: { 
            'rating': ratingValue,
            'product_id': productId,
         },
        success: function(response) {
            // document.getElementById('rating').innerHTML = response.new_average
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