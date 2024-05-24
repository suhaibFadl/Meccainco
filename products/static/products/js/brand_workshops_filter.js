$(document).ready(function () {
    console.log('here')
    const no_results = `
    <!-- Start Empty Cart -->
    <div class="empty-content-page my-5">
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


    $("#Brand-Category-Form").on("submit", function (event) {
        event.preventDefault();
        const brandSelect = $('#brand');
        const categorySelect = $('#category');
        const citySelect = $('#city');
    
        $.ajax({
            url: brand_workshops_filter_url,
            data: { 
                'brand': brandSelect.val(),
                'category': categorySelect.val(),
                'city': citySelect.val(),
            },

            dataType: "json",
            success: function (response) {
                console.log('hereeeee' ,response.workshops)
                // Append the new search results
                // $("#Brand-Category-Form").empty();
                $('#products-container').empty();
                console.log('length',response.workshops.length)
                if(response.workshops.length > 0) {
                    response.workshops.forEach(function (result) {
                        const workshop_url = `/profiles/workshops/${result.name}`;
                        
                        var stars = ''
                        for(let i = 1; i <= 5; i++ ){  
                            if( i<= result.workshop_rating){
                            stars += `<i class="spr-icon fa fa-star"></i>`
                            }  
                            else{
                            stars += `<i class="spr-icon fa fa-star-o"></i>`                           
                            } 
                        }
                        $("#products-container").append(`

                        <div class="col-sp col-xl-3 col-lg-3 col-md-4 col-sm-6 col-6">
                        <div class="product-item">
                            <div class="product-image-action">
                                <div class="product-image">
                                    <a href="${workshop_url}">
                                        <img class="img-fluid blur-up lazyload" src="${MEDIA_URL}${result.logo}" data-src="${MEDIA_URL}${result.logo}" alt="image" title="image" />
                                        <img class="img-fluid blur-up lazyload product-imghover" src="${MEDIA_URL}${result.logo}" data-src="${MEDIA_URL}${result.logo}" alt="image" title="image" />
                                    </a>
                                </div>
                            </div>
                            <div class="product-details">
                                <h3 class="product-title"><a href="${workshop_url}">${result.name}</a></h3>
                                <h4 class="product-vendor">${result.bio}</h4>
                                <div class="product-starrating">    `   
                                 + stars +                                                        
                            `   </div>
                            </div>
                        </div>
                    </div>
                        `);
            
                    });
                }
                if($('#products-container').is(":empty")){
                    $(".products").append(no_results);   
                }
            },
            error: function () {
                console.error('Error performing search');
            }
        });   
   
    });
});