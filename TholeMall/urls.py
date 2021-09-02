"""TholeMall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from mall import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
import mall

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mall.urls')),
    path('accounts/', include('accounts.urls')),
    path('<slug:slug>/', mall.views.product_list_category, name="ProdListCategory"),
    path('<slug:slug1>/<slug:slug2>/',mall.views.product_list_subcategory, name="ProdListSubcategory"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

