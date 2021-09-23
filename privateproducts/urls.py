from django.urls import path
from .views import PrivateProductsView, PrivateProductDetailView

urlpatterns = [
    path('', PrivateProductsView.as_view()),
    path('/<int:product_id>', PrivateProductDetailView.as_view()),
    
]
