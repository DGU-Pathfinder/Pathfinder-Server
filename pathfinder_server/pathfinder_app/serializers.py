from rest_framework import serializers
from .models import (
    RtImage,
    AiModel,
    Defect,
)


class DefectListCreateSerializer(serializers.ModelSerializer):
    modifier    = serializers.ReadOnlyField(source='modifier.username')

    class Meta:
        model = Defect
        fields = [
            'ai_model',
            'modifier',
            'defect_type',
            'xmin',
            'ymin',
            'xmax',
            'ymax',
        ]


class AiModelListCreateSerializer(serializers.ModelSerializer):
    defect_set  = DefectListCreateSerializer(many=True)

    class Meta:
        model = AiModel
        fields = [
            'rt_image',
            'ai_model_name',
            'score',
            'expert_check',
        ]
 

# View에서 보여주고, 생성할 수 있도록 하는 serializer
class RtImageListCreateSerializer(serializers.ModelSerializer):
    ai_model_set = AiModelListCreateSerializer(many=True)
    uploader    = serializers.ReadOnlyField(source='uploader.username')

    class Meta:
        model = RtImage
        fields = [
            'ai_model_set',
            'uploader',
            'upload_date',
            'image',
        ]

       
        
# class RtImageDetailSerializer(serializers.ModelSerializer):
#     uploader    = serializers.ReadOnlyField(source='uploader.username')
#     ai_model    = AiModelReadSerializer(many=True, read_only=True)

#     class Meta:
#         model = RtImage
#         fields = [
#             'image',
#             'ai_model'
#         ]


class DefectDetailSerializer(serializers.ModelSerializer):
    modifier    = serializers.ReadOnlyField(source='modifier.username')

    class Meta:
        model = Defect
        fields = [
            'modifier',
            'defect_type',
            'xmin',
            'ymin',
            'xmax',
            'ymax',
        ]

class AiModelDetailSerializer(serializers.ModelSerializer):
    defect_set  = DefectDetailSerializer(many=True)

    class Meta:
        model = AiModel
        fields = [
            'rt_image',
            'ai_model_name',
            'score',
            'expert_check',
        ]
