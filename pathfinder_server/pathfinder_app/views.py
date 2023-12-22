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
    ExpertSerializer,
    ExpertCreateSerializer,
    ExpertDefectSerializer,
    ExpertDefectCreateSerializer,
    WelderSerializer,
)
from .tasks import computer_vision_process_task
from .filters import RtImageFilter

class RtImageViewSet(
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
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            instance_id = response.data['pk']
            self.get_queryset().filter(pk=instance_id).update(
                uploader=self.request.user
            )
            result = computer_vision_process_task.delay(instance_id)

            return Response({
                'message'           : 'Processing started',
                'rt_image_id'       : instance_id,
                'ai_model_task_id'  : result.id,
            })
        return response

    def get_serializer_class(self):
        if self.action == 'create':
            return RtImageCreateSerializer
        return RtImageListSerializer


class ExpertViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):
    queryset = Expert.objects.all()

    def perform_create(self, serializer):
        expert = serializer.save()
        expert.rt_image.welder.number += 1
        expert.rt_image.welder.success_count += 1
        expert.rt_image.welder.save()

    def get_serializer_class(self):
        if self.action == 'create':
            return ExpertCreateSerializer
        return ExpertSerializer


class ExpertDefectViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin
):
    queryset = ExpertDefect.objects.all()

    defect_type_to_field = {
        'slag'      : 'slag_number',
        'porosity'  : 'porosity_number',
        'others'    : 'others_number'
    }

    def create(self, request, *args, **kwargs):
        rt_image = get_object_or_404(RtImage, pk=request.data['rt_image_id'])
        expert, created = Expert.objects.get_or_create(rt_image=rt_image)
        serializer = self.get_serializer(data=request.data['defect_list'], many=True)

        if serializer.is_valid():
            serializer.save(expert=expert, modifier=self.request.user)
            if rt_image.welder is not None:
                if created:
                    rt_image.welder.number += 1
                elif rt_image.expert.expert_defect_set.exists():
                    rt_image.welder.success_count -= 1
                for defect_data in serializer.data:
                    field_name = self.defect_type_to_field.get(defect_data['defect_type'])
                    if field_name:
                        setattr(rt_image.welder, field_name,
                                getattr(rt_image.welder, field_name) + 1)
                rt_image.welder.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=False)
    def bulk_delete(self, request):
        pk_list = request.data.get('pk_list', None)
        if pk_list is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        defect_once = self.get_queryset().filter(pk=pk_list[0]).get()
        expert = defect_once.expert
        if defect_once.expert.rt_image.welder is not None:
            for defect in self.get_queryset().filter(pk__in=pk_list):
                field_name = self.defect_type_to_field.get(defect.defect_type)
                if field_name:
                    setattr(defect_once.expert.rt_image.welder, field_name,
                            getattr(defect_once.expert.rt_image.welder, field_name) - 1)
            defect_once.expert.rt_image.welder.save()
        self.get_queryset().filter(pk__in=pk_list).delete()
        if not expert.expert_defect_set.exists():
            expert.rt_image.welder.success_count += 1
            expert.rt_image.welder.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

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

    @action(methods=['GET'], detail=False, url_path='(?P<welder_name>.+)')
    def get_welder_detail(self, request, welder_name=None):
        welder = get_object_or_404(Welder, name=welder_name)
        serializer = self.get_serializer(welder)
        return Response(serializer.data)
