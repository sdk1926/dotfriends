from django.urls import path
from .views import ProductsView, ProductDetailView, UserProductLikesView

urlpatterns = [
    path('', ProductsView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('/likes',UserProductLikesView.as_view()),
    path('/private'),
]
