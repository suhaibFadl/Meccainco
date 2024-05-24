from django.urls import path
from .views import index, product_details, categories_list, category_details,\
        brands_list,brand_details, brand_categories_details, add_comment,\
        AddProduct, load_parts, update_product, delete_product, add_product_image,\
        delete_product_image, ajax_search_view, search_results_view, load_brands, \
        load_cars, load_years, ajax_filter_view, filter_results_view,\
        brand_stores_details, brand_workshops_details, brand_categories_filter, \
        brand_stores_filter, brand_workshops_filter, ajax_delete_product


app_name = 'products'
urlpatterns = [
    path('', index, name='index'),
    path('categories', categories_list, name='categories_list'),
    path('categories/<str:category>/', category_details, name='category_details'),
    path('cars/', brands_list, name='brands_list'),
    path('cars/<str:brand>/', brand_details, name='brand_details'),
    path('cars/<str:brand>/categories/<str:category>/', brand_categories_details,
        name='brand_categories_details'
    ),
    path('cars/brand_categories_filter', brand_categories_filter,
        name='brand_categories_filter'
    ),
    path('cars/brand_stores_filter', brand_stores_filter,
        name='brand_stores_filter'
    ),
    path('cars/brand_workshops_filter', brand_workshops_filter,
        name='brand_workshops_filter'
    ),
    path('cars/<str:brand>/stores/', brand_stores_details,
        name='brand_stores_details'
    ),
    path('cars/<str:brand>/workshops/', brand_workshops_details,
        name='brand_workshops_details'
    ),
    path('products/<int:id>/', product_details, name='product_details'),
    path('products/add_product', AddProduct.as_view(), name='add_product'),
    path('products/update_product/<int:id>', update_product, name='update_product'),
    path('products/delete_product/<int:id>', delete_product, name='delete_product'),
    path('ajax/load-parts/', load_parts, name='ajax_load_parts'),  # <-- this one here
    path('ajax/load-brands/', load_brands, name='ajax_load_brands'),  # <-- this one here
    path('ajax/load-cars/', load_cars, name='ajax_load_cars'),  # <-- this one here
    path('ajax/load-years/', load_years, name='ajax_load_years'),  # <-- this one here
    path('ajax/add_comment', add_comment, name='add_comment'),  # <-- this one here
    path('products/add_image/<int:id>', add_product_image, name='add_product_image'),
    path('products/delete_product_image/<int:id>', delete_product_image, name='delete_product_image'),
    path('ajax_search/', ajax_search_view, name='ajax_search'),
    path('search_results/', search_results_view, name='search_results'),
    path('ajax_filter/', ajax_filter_view, name='ajax_filter'),
    path('filter_results/', filter_results_view, name='filter_results'),
    path('ajax-delete-product/', ajax_delete_product, name='ajax-delete-product'),
]
