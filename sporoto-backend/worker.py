import os
import time
from celery import Celery
# from sqlalchemy.orm import Session
# from database import get_db
# from fastapi import Depends
# import models
celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

@celery.task(name='metrics')
def get_metric(code, metrics):
    import random
    import time
    """
    {code}에 따라 deterministic하게 metric을 반환해주는 함수
    실제 채점과 유사하도록 {code}에 따라 1~6초의 딜레이가 걸립니다.

    Args:
        code(str): 코드 / 실제로 eval되지는 않음
        metrics(List[str]): 반환해야 할 metric 목록

    Returns(Dict[str, int]): 각 metric별로 0~100사이의 난수를 가지는 dict
    """
    random.seed(code)

    time.sleep(random.random() * 15 + 1)
    result = {k: random.randint(0, 100) for k in metrics}
    # db_submission = db.query(models.Submissions).filter_by(submission_id=code).first()
    # db_submission.result = result
    # db_submission.status = 'Complete'
    # db.add(db_submission)
    # db.commit()
    # db.refresh(db_submission)


    return result