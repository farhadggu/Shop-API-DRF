from django.contrib import admin
from django.urls import path, include
# from .views import hello


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('admin/', admin.site.urls),
    path('api-product/', include('product.urls')),
    path('api-cart/', include('cart.urls')),
    path('api-order/', include('order.urls')),
# path('', hello),
]
