$(document).ready(function() {
    // Minimum and maximum values
    var minValue = 1;
    var maxValue = 10; // Change this to your desired maximum value

    // When the minus button is clicked
    $(".qtyminus").click(function() {
        var quantityInput = $("#product-quantity");
        var currentValue = parseInt(quantityInput.val());
        console.log(currentValue)

        // Check if the current value is greater than the minimum
        if (currentValue < minValue) {
            quantityInput.val(minValue);
        }
    });

    // When the plus button is clicked
    $(".qtyplus").click(function() {
        var quantityInput = $("#product-quantity");
        var currentValue = parseInt(quantityInput.val());

        // Check if the current value is less than the maximum
        if (currentValue > maxValue) {
            quantityInput.val(maxValue);
        }
    });

    $("#product-quantity").change(function() {
        console.log($(this).val())
        if ($(this).val() > maxValue){
            $(this).val(maxValue);
        }
        else if($(this).val() < minValue){
            $(this).val(minValue);
        }
    });

    $('.order-btn').click(function(){   
        var productQ = $("#product-quantity").val();
        var productId = $(this).attr("product-id");
        $.ajax({
        url: url,
        data: {
            'productId': productId,
            'productQuantity': productQ
        },
        success: function (data) {
            console.log('data', data['data']);
            $(`.product-quantity`).remove();
            $(`.product-submit`).html(` 
            <div class="product-form-item product-submit btn-block">
                <a href="#" class="btn btn-primary disabled btn-block product-btn-cart add-cart" disabled>Ordered</a>
            </div>`);
            
        }
        });
    })
    
});



