from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # RtImageViewSet,
    RtImageListCreateView,
    # RtImageDetailView,
    DefectViewSet,
    Test,
)

'''
    /rt-images/                         # 목록 조회  GET
    /rt-images/                         # 생성      POST
    /rt-image/<int:pk>                  # 단일 조회  GET
    /rt-image/<int:pk>/                 # 삭제      DELETE

    /ai-models/<int:pk>/                # 수정     PATCH
    /ai-models/<int:pk>/                # 삭제     DELETE

    /defects/                           # 생성     POST
    /defects/<int:pk>/                  # 수정     PATCH
    /defects/<int:pk>/                  # 삭제     DELETE
'''

router = DefaultRouter()
router.register('defects', DefectViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('rt-images/', RtImageListCreateView.as_view()),
    path('test/', Test.as_view()),
]