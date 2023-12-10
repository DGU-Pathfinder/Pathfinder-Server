from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from celery.result import AsyncResult
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
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
    Welder,
    Expert,
    ExpertDefect,
)
from .serializers import (
    RtImageCreateSerializer,
    RtImageListSerializer,
    ExpertDefectSerializer,
    ExpertDefectCreateSerializer,
    WelderSerializer,
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
    mixins.DestroyModelMixin
):
    queryset            = ExpertDefect.objects.all()
    serializer_class    = ExpertDefectSerializer

    defect_type_to_field = {
        'slag': 'slag_number',
        'porosity': 'porosity_number',
        'others': 'others_number'
    }

    def create(self, request, *args, **kwargs):
        rt_image = get_object_or_404(RtImage, pk=request.data['rt_image_id'])
        expert, created = Expert.objects.get_or_create(rt_image=rt_image)
        # copied_data = request.data.copy()
        # self.request.data['expert'] = expert.pk
        # copied_data['expert'] = expert.pk
        serializer = self.get_serializer(
            data    = request.data['defect_list'],
            # context = {'expert_pk' : expert},
            many    = True
        )

        if serializer.is_valid():
            serializer.save(expert=expert, modifier=self.request.user)
            if rt_image.welder is not None:
                for defect_data in serializer.data:
                    field_name = self.defect_type_to_field.get(defect_data['defect_type'])
                    if field_name:
                        setattr(rt_image.welder, field_name,
                                getattr(rt_image.welder, field_name) + 1)
                rt_image.welder.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def perform_destroy(self, instance):
        if instance.expert.rt_image.welder is not None:
            field_name = self.defect_type_to_field.get(instance.defect_type)
            if field_name:
                setattr(instance.expert.rt_image.welder, field_name,
                        getattr(instance.expert.rt_image.welder, field_name) - 1)
            instance.expert.rt_image.welder.save()
        instance.delete()

    def get_serializer_class(self):
        if self.action == 'create':
            return ExpertDefectCreateSerializer
        return ExpertDefectSerializer


class WelderViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset            = Welder.objects.all()
    serializer_class    = WelderSerializer

    # def get_queryset(self):
    #     return self.queryset.filter(expert_defect_set__isnull=False).distinct()


@api_view(['POST'])
def get_tasks_status(request):
    task_ids    = request.data.get('task_ids')
    statuses    = {
        task_id: AsyncResult(task_id).status for task_id in task_ids
    }
    return JsonResponse({'statuses': statuses})