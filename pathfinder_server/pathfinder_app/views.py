from django.http import JsonResponse
from celery.result import AsyncResult
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import (
#     SearchFilter,
#     OrderingFilter,
# )
from rest_framework import (
    generics,
    viewsets,
    mixins,
    status,
)
from .models import (
    RtImage,
    AiModel,
    Defect,
)
from .serializers import (
    RtImageCreateSerializer,
    RtImageListSerializer,
    AiModelUpdateSerializer,
    DefectSerializer,
)
from .tasks import (
    test_task,
    computer_vision_process_task,
)
# from .filters import RtImageFilter
from .enums import AiModelName

class RtImageVIewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = RtImage.objects.all()
    permission_classes = [AllowAny,] # should be changed to IsAuthenticated

    def create(self, request, *args, **kwargs):
        response            = super().create(request, *args, **kwargs)
        instance_id         = response.data['pk']
        # ai_model_task_id    = []
        # for model_name in AiModelName:
        #    result = computer_vision_process_task.delay(instance_id, model_name.value)
        #    ai_model_task_id.append({ model_name : result.id })
        return Response({
            'message'           : 'Processing started',
            'rt_image_id'       : instance_id,
            # 'ai_model_task_id'  : ai_model_task_id,
        })

    def get_serializer_class(self):
        if self.action == 'create':
            return RtImageCreateSerializer
        return RtImageListSerializer


class AiModelUpdateView(generics.UpdateAPIView):
    queryset            = AiModel.objects.all()
    serializer_class    = AiModelUpdateSerializer
    permission_classes  = [AllowAny,] # should be changed to IsAuthenticated


class DefectViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    queryset            = Defect.objects.all()
    serializer_class    = DefectSerializer
    permission_classes  = [AllowAny,] # should be changed to IsAuthenticated


@api_view(['POST'])
def get_tasks_status(request):
    task_ids    = request.data.get('task_ids')
    statuses    = {
        task_id: AsyncResult(task_id).status for task_id in task_ids
    }
    return JsonResponse({'statuses': statuses})


class Test(APIView):
    def get(self, request):
        test_task.delay(2, 5)
        return Response("Celery Task Running")