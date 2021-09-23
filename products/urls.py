from django.urls import path
from .views import PublicProductsView, PublicProductDetailView, UserProductLikesView

urlpatterns = [
    path('', PublicProductsView.as_view()),
    path('/<int:product_id>', PublicProductDetailView.as_view()),
    path('/likes',UserProductLikesView.as_view()),
]
