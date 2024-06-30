from django.urls import path
from .views import ProductListView, ProductDetailView, CartView, CheckoutView, add_to_cart, cancel_order

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cancel_order/', cancel_order, name='cancel_order'),
]