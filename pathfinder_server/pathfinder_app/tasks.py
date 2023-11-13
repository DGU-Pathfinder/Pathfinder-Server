from celery import shared_task
from pathfinder_server.celery import app


# test 용 함수
@shared_task
def test_task(a: int, b: int):
    print("test Celery task : ", a + b)
    return a + b

@shared_task
def computer_vision_process_task(rt_image_id: int, model_name: str):
    print("computer_vision_process_task")
    print("rt_image_id : ", rt_image_id)
    print("model_name : ", model_name)
    # AiModel.objects.create(image_id=image_id, ...)
    return 