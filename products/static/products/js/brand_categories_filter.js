$(document).ready(function () { 
    const no_results = `
    <!-- Start Empty Cart -->
    <div class="empty-content-page my-5 mx-auto">
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-12 col-sm-10 col-md-8 col-lg-8 col-xl-7 text-center">
                    <div class="empty-page my-5">
                        <i class="fa fa-search" aria-hidden="true"></i>
                        <h2>Your Search Returns No Results!</h2>
                       
                        <a href="{% url 'products:index' %}" class="continue-shop btn btn-primary">Continue Shopping</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- End Empty Cart -->
    `
    if($('#products-container').children().length === 0){
        $("#products-container").append(no_results);   
    }    

    const brandSelect = $('#brand');
    const categorySelect = $('#category');
    const citySelect = $('#city');
    const carSelect = $('#car');
    const yearSelect = $('#year');
    const min_price = $('#min-price');
    const max_price = $('#max-price');

    brandSelect.on('change', function() {
        const selectedBrand = $(this).val();
        console.log('Brand',selectedBrand);
        if (selectedBrand) {
            carSelect.prop('disabled', false);
            yearSelect.prop('disabled', true);

            // Load cars using AJAX
            $.get(load_cars_url, { brand: selectedBrand }, function(data) {
                // carSelect.empty().append('<option value="">Select Car</option>');
                console.log(data);
                console.log(data.cars);
                data.cars.forEach(function(car) {
                    carSelect.append(`<option value="${car.name}">${car.name}</option>`);
                });
            });
        } else {
            carSelect.prop('disabled', true);
            yearSelect.prop('disabled', true);
            carSelect.empty().append('<option value="">Select Car</option>');
            yearSelect.empty().append('<option value="">Select Year</option>');
        }
    });

    carSelect.on('change', function() {
        const selectedCar = $(this).val();
        if (selectedCar) {
            yearSelect.prop('disabled', false);

            // Load years using AJAX
            $.get(load_years_url, { car: selectedCar }, function(data) {
                yearSelect.empty().append('<option value="" disabled selected>Year</option>');
                data.years.forEach(function(year) {
                    yearSelect.append(`<option value="${year}">${year}</option>`);
                });
            });
        } else {
            yearSelect.prop('disabled', true);
            yearSelect.empty().append('<option value="" disabled selected>Select Year</option>');
        }
    });

    $("#Brand-Category-Form").on("submit", function (event) {
        event.preventDefault();
        const MEDIA_URL = "{% get_media_prefix %}";

        console.log(
                'category', categorySelect.val(),
                'city', citySelect.val(),
                'car', carSelect.val(),
                'year', yearSelect.val(),
                'min_price', min_price.val(),
                'max_price', max_price.val(),
        )        
        $.ajax({
            url: brand_categories_filter_url,
            data: { 
                'brand': brandSelect.val(),
                'category': categorySelect.val(),
                'city': citySelect.val(),
                'car': carSelect.val(),
                'year': yearSelect.val(),
                'min_price': min_price.val(),
                'max_price': max_price.val(),
            },

            dataType: "json",
            success: function (response) {
                console.log('hereeeee' ,response.products)
                // Append the new search results
                // $("#Brand-Category-Form").empty();
                $('#products-container').empty();
                console.log('length',response.products.length)
                if(response.products.length > 0) {
                    response.products.forEach(function (result) {
                        const url = `products/${result.product_id}/`
                        const store_url = `/profiles/stores/${result.store.name}`;
                        var stars = ''
                        for(let i = 1; i <= 5; i++ ){  
                            if( i<= result.product_rating){
                            stars += `<i class="spr-icon fa fa-star"></i>`
                            }  
                            else{
                            stars += `<i class="spr-icon fa fa-star-o"></i>`                           
                            } 
                        }
                        $("#products-container").append(`
                        <div class="col-sp col-6 col-sm-4 col-md-4 col-lg-4 col-xl-4">
                        <div class="product-item">
                            <div class="product-image-action">
                                <div class="product-image">
                                    <a href="${url}">
                                        <img class="img-fluid blur-up lazyload" src="${result.part.image}" data-src="${result.part.image}" alt="image" title="image" />
                                        <img class="img-fluid blur-up lazyload product-imghover" src="${result.part.image}" data-src="${result.part.image}" alt="image" title="image" />
                                    </a>
                                </div>
                               
                                <div class="product-action">
                                    <ul>
                                        <li class="actions-addcart" data-toggle="tooltip" data-placement="top" title="add to cart"><a href="#open-addtocart-popup" class="btn open-addtocart-popup"><i class="icon ti-shopping-cart"></i></a></li>
                                        <li class="actions-quickview" data-toggle="tooltip" data-placement="top" title="quick view"><a href="#open-quickview-popup" class="btn open-quickview-popup"><i class="icon ti-zoom-in"></i></a></li>
                                        <li class="actions-wishlist" data-toggle="tooltip" data-placement="top" title="add to wishlist"><a href="#open-wishlist-popup" class="btn open-wishlist-popup"><i class="icon ti-heart"></i></a></li>
                                    </ul>
                                </div>
                            </div>
                            <div class="product-details">
                                <h3 class="product-title"><a href="${url}">${result.part.name}</a></h3>
                                <h4 class="product-vendor">
                                    <a href="${store_url}">
                                    ${result.store.name}  Store
                                    </a>
                                </h4>                                  
                                <div class="product-starrating">`
                                + stars 
                                + `</div>
                                <div class="product-price">
                                    <span class="sale-price">${result.price}</span>
                                </div>
                                
                            </div>
                        </div>
                    </div>
                       
                        `);
            
                    });
                }
                if($('#products-container').is(":empty")){
                    $("#products-container").append(`
                    <!-- Start Empty Cart -->
                    <div class="empty-content-page my-5 mx-auto">
                        <div class="container">
                            <div class="row justify-content-center">
                                <div class="col-12 col-sm-10 col-md-8 col-lg-8 col-xl-7 text-center">
                                    <div class="empty-page my-5">
                                        <i class="fa fa-search" aria-hidden="true"></i>
                                        <h2>Your Search Returns No Results!</h2>
                                       
                                        <a href="{% url 'products:index' %}" class="continue-shop btn btn-primary">Continue Shopping</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- End Empty Cart -->
                    `);   
                }
            },
            error: function () {
                console.error('Error performing search');
            }
        });   
   
    });
});