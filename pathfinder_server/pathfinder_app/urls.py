from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RtImageViewSet,
    ExpertDefectViewSet,
    WelderViewSet,
)

'''
    사용자(전문가)가 접근할 수 있는 리스트

    /rt-images/                         # 목록 조회  GET     OK
    /rt-images/                         # 생성      POST    OK
    /rt-image/<int:pk>                  # 단일 조회  GET     OK
    /rt-image/<int:pk>/                 # 삭제      DELETE  OK

    /ai-models/<int:pk>/                # 수정      PATCH   OK

    /defects/                           # 생성      POST    OK
    /defects/<int:pk>/                  # 수정      PATCH   OK
    /defects/<int:pk>/                  # 삭제      DELETE  OK
'''

router = DefaultRouter()
router.register('expert-defects', ExpertDefectViewSet)
router.register('rt-images', RtImageViewSet)
router.register('welders', WelderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]