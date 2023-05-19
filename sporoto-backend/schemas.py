from typing import Union
from typing import List, Optional, Dict
from pydantic import BaseModel, Json
from datetime import datetime

class Challenges(BaseModel):
    create_time : datetime
    title : str
    challange_id: str = None

    class Config:
        orm_mode = True

class Challenge(BaseModel):
    create_time : datetime
    title : str
    challange_id: str = None
    metrics : List[str]
    content : Optional[str] = None

    class Config:
        orm_mode = True

class Submission_id(BaseModel):
    result : Dict[str, int]
    status : str
    submission_time : datetime

class Submission(BaseModel):
    submission_time : datetime
    submission_id : str
    challenge_id : str