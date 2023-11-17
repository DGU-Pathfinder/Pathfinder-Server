from celery import shared_task
from pathfinder_server.celery import app
from .models import (
    AiModel,
    AiDefect,
)
from .serializers import (
    AiModelCreateSerializer,
    AiDefectSerializer,
)
from .ai.ai_process import (
    ai_model_efficientdet,
    ai_model_retinanet,
    ai_model_faster_rcnn,
    ai_model_cascade_rcnn,
)


# test 용 함수
@shared_task
def test_task(a: int, b: int):
    print("test Celery task : ", a + b)
    return a + b


@shared_task
def computer_vision_process_task(rt_image_id: int, model_name: str):
    """Get result from ai model and save to db"""

    dict_ai_model_func = {
        'EfficientDet'  : ai_model_efficientdet,
        'RetinaNet'     : ai_model_retinanet,
        'Faster_R-CNN'  : ai_model_faster_rcnn,
        'Cascade_R-CNN' : ai_model_cascade_rcnn,
    }

    # ai단 함수 호출
    ai_score, defect_data_set = dict_ai_model_func[model_name](rt_image_id)

    # 결함이 없어도 반드시 추가할 것
    ai_model_serializer = AiModelCreateSerializer(
        data={
            'rt_image'      : rt_image_id,
            'ai_model_name' : model_name,
            'score'         : ai_score,
        })
    if ai_model_serializer.is_valid():
        ai_model_serializer.save()
    else:
        print(ai_model_serializer.errors)
        return

    # 결함이 있을 경우에만 사용할 것
    for element in defect_data_set:
        defect_serializer = AiDefectSerializer(
            data={
                'ai_model'      : ai_model_serializer.data['pk'],
                'defect_type'   : element['defect_type'],
                'xmin'          : element['xmin'],
                'ymin'          : element['ymin'],
                'xmax'          : element['xmax'],
                'ymax'          : element['ymax'],
            })
        if defect_serializer.is_valid():
            defect_serializer.save()
        else:
            print(defect_serializer.errors)
            return

    print("Finished AI model task : ", model_name)
    return 