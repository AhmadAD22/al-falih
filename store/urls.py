from django.urls import path
from .views import AddToCartView, ViewCartView

urlpatterns = [
    path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('view-cart/', ViewCartView.as_view(), name='view_cart'),
]