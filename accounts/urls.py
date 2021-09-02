from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name="Profile"),
    path('signup/', views.signup, name="SignUp"),
    path('login/', views.login, name="Login"),
    path('logout/', views.logout, name="LogOut"),
    path('verifyaccount/', views.verifyaccount, name="VerifyAccount"),
    path('change_password/', views.change_password, name="ChangePassword"),
    path('addresses/', views.addresses, name="Addresses"),
    path('addresses/edit/<slug:slug>/', views.edit_address, name="EditAddress"),
    path('addresses/delete/<slug:slug>/', views.delete_address, name="DeleteAddress"),
    path('addresses/make_default_address/<slug:slug>/', views.make_default_address, name="MakeDefaultAddress"),
    path('orders/', views.orders, name="Orders")
]
