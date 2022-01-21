from django.urls import path
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('order', views.OrderViewSet, basename='order')


urlpatterns = router.urls


urlpatterns += [
    path('request/', views.SendRequestAPIView.as_view(), name='request'),
    path('verify/', views.VerifyAPIView.as_view(), name='verify'),
]

