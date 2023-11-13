from celery import shared_task
from pathfinder_server.celery import app


# test 용 함수
@shared_task
def test_task(a: int, b: int):
    print("test Celery task : ", a + b)
    return a + b