from django.urls import path, include, re_path

urlpatterns = [
    path('public/product', include('products.urls')),
    path('private/product', include('privateproducts.urls')),
    path('user', include('users.urls')),
    path('cart', include('carts.urls'))
]
