from django.urls import path
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('carts', views.CartViewSet)

cart_items = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_items.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + cart_items.urls
