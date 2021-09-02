from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Index"),
    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="Contact Us"),
    path('search/', views.search, name="Search"),
    path('order_details/', views.order_details, name="OrderDetails"),
    path('product/<slug:product_slug>/', views.productView, name="ProductView"),
    path('cart/', views.cart, name="Cart"),
    path('checkout/', views.checkout, name="Checkout"),
    path(r'getsubcategory/',views.get_subcategory),
    path('handlepayment/', views.handlepayment, name="HandlePayment"),
    
]
