from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # RtImageViewSet,
    RtImageListCreateView,
    Test
)

# router = DefaultRouter()
# router.register('rt-images', RtImageViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('rt-image/', RtImageListCreateView.as_view()),
    path('test/', Test.as_view()),
]