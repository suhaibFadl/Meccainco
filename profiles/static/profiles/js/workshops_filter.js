$(document).ready(function () {
    const no_results = `
    <!-- Start Empty Cart -->
    <div class="mx-auto empty-content-page my-5">
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
            url: workshops_filter_url,
            data: { 
                'brand': brandSelect.val(),
                'category': categorySelect.val(),
                'city': citySelect.val(),
            },

            dataType: "json",
            success: function (response) {
                // console.log('hereeeee' ,response.stores)
                // Append the new search results
                // $("#Brand-Category-Form").empty();
                $('#products-container').empty();
                // console.log('length',response.stores.length)
                if(response.workshops.length > 0) {
                    response.workshops.forEach(function (result) {

                        console.log(MEDIA_URL,result.logo)
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
                        console.log('categories', result.categories.length)
                        console.log('categories', result.categories)
                        var categories = '';
                        for(let i=0; i <  result.categories.length; i++ ){ 
                            categories += `<li class="active" data-toggle="tooltip" data-placement="top">${result.categories[i]}</li>`
                        }
                        $("#products-container").append(`
                        <div class="col-12 col-sm-12 col-md-12 col-sp">
                            <div class="product-item row no-gutters">
                                <div class="product-image-action col-12 col-sm-12 col-md-3">
                                    <div class="product-image">
                                        <a href="${workshop_url}">
                                            <img class="img-fluid blur-up lazyload" src="${MEDIA_URL}${result.logo}" data-src="${MEDIA_URL}${result.logo}" alt="image" title="image" />
                                            <img class="img-fluid blur-up lazyload product-imghover" src="${MEDIA_URL}${result.logo}" data-src="${MEDIA_URL}${result.logo}" alt="image" title="image" />
                                        </a>
                                    </div>
                                </div>
                                <div class="product-details col-12 col-sm-12 col-md-9">
                                    <h1 class="product-title"><a class="font-weight-bold" href="${workshop_url}">${result.name}<a></h1>
                                    <h4 class="product-vendor">${result.bio}</h4>

                                    <div class="product-starrating">  
                       `   
                                 + stars +                                                        
                            `       </div>
                                    <div class="mt-3">
                                        <ul class="d-flex flex-row align-items-center">
                                           `
                                            + categories +
                                            `     
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                        `);
            
                    });
                }
                if($('#products-container').is(":empty")){
                    $("#products-container").append(no_results);   
                }
            },
            error: function () {
                console.error('Error performing search');
            }
        });   
   
    });
});