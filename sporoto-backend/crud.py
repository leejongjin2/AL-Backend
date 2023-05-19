from sqlalchemy.orm import Session
import models, schemas
# from src import get_metric
import time
from fastapi import APIRouter
from datetime import datetime
import hashlib
from database import get_db
from fastapi import Depends, UploadFile, File

from worker import get_metric

router = APIRouter()

@router.get("/challenges/", tags=['Buzzni AI Backend'], response_model=list[schemas.Challenges])
async def get_challenges(db: Session = Depends(get_db)):
    return db.query(models.Challenges).all()


@router.get('/challenges/{challenge_id}', tags=['Buzzni AI Backend'], response_model=schemas.Challenge)
async def get_challenge(challenge_id: str, db: Session = Depends(get_db)):
    query = db.query(models.Challenges).filter(models.Challenges.challange_id==challenge_id).first()
    query.metrics = query.metrics.split()
    return query


@router.post("/challenges/{challenge_id}/submissions", tags=['Buzzni AI Backend'], response_model=schemas.Submission)
async def submission(challenge_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    code = file.file.read()
    submission_id = hashlib.shake_256(code).hexdigest(6)
    query = db.query(models.Challenges).filter(models.Challenges.challange_id==challenge_id).first()
    metrics = query.metrics.split()
    now = datetime.now().replace(microsecond=0)
    submission_time = now.strftime('%Y-%m-%d %H:%M:%S')
    submission_status = models.Submissions(submission_id=submission_id, submission_time=submission_time, status='processing', c_id=challenge_id)
    response = {"submission_time" : submission_time, "submission_id": submission_id, "challenge_id" : challenge_id}
    # result = get_metric(code=submission_id, metrics=metrics)
    db.add(submission_status)
    db.commit()
    db.refresh(submission_status)

    get_metric.apply_async([submission_id, metrics], task_id=submission_id)
    
    return response


@router.get("/challenges/{challenge_id}/submissions", tags=['Buzzni AI Backend'])
async def get_submissions(challenge_id: str, db: Session = Depends(get_db)):
    query = db.query(models.Submissions).filter(models.Submissions.c_id==challenge_id).all()
    result_dict =dict()
    for q in query:
        if 'Complete' in q.status:
            result_dict[q.submission_id] = {'result' : q.result, 'submission_time': q.submission_time.strftime('%Y-%m-%d %H:%M:%S')}
        else:
            result_dict[q.submission_id] = {'status' : 'processing', 'submission_time': q.submission_time.strftime('%Y-%m-%d %H:%M:%S')}
    return result_dict


@router.get("/challenges/{challenge_id}/submissions/{submission_id}", tags=['Buzzni AI Backend'])
async def get_submission(challenge_id: str, submission_id: str,db: Session = Depends(get_db)):
    result = get_metric.AsyncResult(submission_id)
    query = db.query(models.Submissions).filter(models.Submissions.c_id==challenge_id, models.Submissions.submission_id==submission_id).first()
    print(result.info)
    if result.info == None:
        result_dict = {'status' : 'processing', 'submission_time' : query.submission_time.strftime('%Y-%m-%d %H:%M:%S')}
    else:
        result_dict = {'result' : result.info, 'submission_time' : query.submission_time.strftime('%Y-%m-%d %H:%M:%S')}
    return result_dict