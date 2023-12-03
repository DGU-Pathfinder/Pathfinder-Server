from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from celery.result import AsyncResult
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
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
    Expert,
    ExpertDefect,
)
from .serializers import (
    RtImageCreateSerializer,
    RtImageListSerializer,
    ExpertDefectSerializer,
)
from .tasks import computer_vision_process_task
from .filters import RtImageFilter

class RtImageVIewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = RtImage.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_class = RtImageFilter

    def create(self, request, *args, **kwargs):
        response            = super().create(request, *args, **kwargs)
        instance_id         = response.data['pk']

        result = computer_vision_process_task.delay(instance_id)
        
        return Response({
            'message'           : 'Processing started',
            'rt_image_id'       : instance_id,
            'ai_model_task_id'  : result.id,
        })

    def get_serializer_class(self):
        if self.action == 'create':
            return RtImageCreateSerializer
        return RtImageListSerializer


class ExpertDefectViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    queryset            = ExpertDefect.objects.all()
    serializer_class    = ExpertDefectSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        rt_image = get_object_or_404(RtImage, pk=request.data['rt_image_id'])
        data = request.data.copy()
        try:
            print(rt_image.expert)
            data['expert'] = rt_image.expert.pk
        except RtImage.expert.RelatedObjectDoesNotExist:
            expert = Expert.objects.create(rt_image=rt_image)
            data['expert'] = expert.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(modifier=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # if not rt_image.expert:
        #     expert = Expert.objects.create(rt_image=rt_image.pk)
        #     data = request.data.copy()
        #     data['expert'] = expert.pk
        #     serializer = self.get_serializer(data=data)
        # else:
        # serializer.is_valid(raise_exception=True)
        # serializer.save(modifier=self.request.user)


@api_view(['POST'])
def get_tasks_status(request):
    task_ids    = request.data.get('task_ids')
    statuses    = {
        task_id: AsyncResult(task_id).status for task_id in task_ids
    }
    return JsonResponse({'statuses': statuses})