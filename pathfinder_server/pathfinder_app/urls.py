from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RtImageListCreateView,
    AiModelUpdateView,
    DefectViewSet,
    Test,
)

'''
    사용자(전문가)가 접근할 수 있는 리스트

    /rt-images/                         # 목록 조회  GET
    /rt-images/                         # 생성      POST
    /rt-image/<int:pk>                  # 단일 조회  GET
    /rt-image/<int:pk>/                 # 삭제      DELETE

    /ai-models/<int:pk>/                # 수정      PATCH

    /defects/                           # 생성      POST
    /defects/<int:pk>/                  # 수정      PATCH
    /defects/<int:pk>/                  # 삭제      DELETE
'''

router = DefaultRouter()
router.register('defects', DefectViewSet)

urlpatterns = [
    path('rt-images/', RtImageListCreateView.as_view()),
    path('ai-models/<int:pk>/', AiModelUpdateView.as_view()),
    path('', include(router.urls)),
    path('test/', Test.as_view()),
]