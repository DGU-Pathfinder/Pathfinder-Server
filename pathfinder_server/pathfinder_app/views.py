from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import (
    RtImage,
    AiModel,
    Defect,
)
from .serializers import (
    RtImageCreateSerializer,
    RtImageListSerializer,
    RtImageDetailSerializer,
    # AiModelDetailSerializer,
)
from .tasks import (
    test_task,
    computer_vision_process_task,
)
from .enums import AiModelName


class RtImageListCreateView(generics.ListCreateAPIView):
    queryset = RtImage.objects.all()
    permission_classes = [AllowAny,]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        instance_id = response.data['pk']
        for model_name in AiModelName:
            computer_vision_process_task.delay(instance_id, model_name.value)
        return Response({
            'message': 'Processing started',
            'task_id': instance_id,
        })

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RtImageListSerializer
        elif self.request.method == 'POST':
            return RtImageCreateSerializer


class RtImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RtImage.objects.all()
    serializer_class = RtImageDetailSerializer


class Test(APIView):
    def get(self, request):
        test_task.delay(2, 5)
        return Response("Celery Task Running")