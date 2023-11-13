from rest_framework import serializers
from accounts.models import User
from .models import (
    RtImage,
    AiModel,
    Defect,
)


class AiModelCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AiModel
        fields = [
            'rt_image',
            'ai_model_name',
            'score',
            'expert_check',
        ]

    def validate_ai_model_name(self, value):
        valid_ai_model_names = [
            'EfficientDet',
            'RetinaNet',
            'Faster_R-CNN',
            'Cascade_R-CNN',
        ]
        if value not in valid_ai_model_names:
            raise serializers.ValidationError("This is not a valid AI model name.")
        return value
 

class RtImageCreateSerializer(serializers.ModelSerializer):
    uploader    = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = RtImage
        fields = [
            'pk',
            'uploader',
            'upload_date',
            'image',
        ]


class DefectListSerializer(serializers.ModelSerializer):
    modifier    = serializers.ReadOnlyField(source='modifier.username')
    
    class Meta:
        model = Defect
        fields = [
            'pk',
            'ai_model',
            'modifier',
            'defect_type',
            'xmin',
            'ymin',
            'xmax',
            'ymax',
        ]


class AiModelListSerializer(serializers.ModelSerializer):
    defect_set = DefectListSerializer(many=True)
    
    class Meta:
        model = AiModel
        fields = [
            'pk',
            'rt_image',
            'ai_model_name',
            'score',
            'expert_check',
            'defect_set'
        ]

    def to_representation(self, instance):
        """Custom representation to handle no AiModel case."""
        representation = super().to_representation(instance)
        if not instance.defect_set.exists():
            representation['defect_set'] = []
        return representation


class RtImageListSerializer(serializers.ModelSerializer):
    ai_model_set = AiModelListSerializer(many=True)
    
    class Meta:
        model = RtImage
        fields = [
            'pk',
            'image',
            'uploader',
            'upload_date',
            'ai_model_set',
        ]

    def to_representation(self, instance):
        """Custom representation to handle no AiModel case."""
        representation = super().to_representation(instance)
        if not instance.ai_model_set.exists():
            representation['ai_model_set'] = []
        return representation


class DefectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Defect
        fields = [
            'pk',
            'ai_model',
            # 'modifier_pk',
            'modifier',
            'defect_type',
            'xmin',
            'ymin',
            'xmax',
            'ymax',
        ]

    def validate_defect_type(self, value):
        valid_defect_types = [
            'slag',
            'porosity',
            'others',
        ]
        if value not in valid_defect_types:
            raise serializers.ValidationError("This is not a valid defect type name.")
        return value


class AiModelUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AiModel
        fields = [
            'pk',
            'expert_check',
        ]


# class AiModelDetailSerializer(serializers.ModelSerializer):
#     defect_set  = DefectDetailSerializer(many=True)

#     class Meta:
#         model = AiModel
#         fields = [
#             'pk',
#             'rt_image',
#             'ai_model_name',
#             'score',
#             'expert_check',
#             'defect_set',
#         ]

#     def to_representation(self, instance):
#         """Custom representation to handle no AiModel case."""
#         representation = super().to_representation(instance)
#         if not instance.defect_set.exists():
#             representation['defect_set'] = []
#         return representation


# class RtImageDetailSerializer(serializers.ModelSerializer):
#     uploader    = serializers.ReadOnlyField(source='uploader.username')
#     ai_model_set    = AiModelDetailSerializer(many=True, read_only=True)

#     class Meta:
#         model = RtImage
#         fields = [
#             'pk',
#             'image',
#             'uploader',
#             'upload_date',
#             'ai_model_set'
#         ]
    
#     def to_representation(self, instance):
#         """Custom representation to handle no AiModel case."""
#         representation = super().to_representation(instance)
#         if not instance.ai_model_set.exists():
#             representation['ai_model_set'] = []
#         return representation