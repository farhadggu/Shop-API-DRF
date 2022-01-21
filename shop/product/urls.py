from django.db.models import base
from django.urls import path
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('category', views.CategoryViewSet)
router.register('products', views.ProductViewSet)

comment_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
comment_router.register('comment', views.CommentViewSet, basename='comment')


urlpatterns = router.urls + comment_router.urls
