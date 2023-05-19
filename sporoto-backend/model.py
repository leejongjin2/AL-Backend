from sqlalchemy import Column, String, JSON, ForeignKey, Text
from database import Base

class Challenges(Base):
    __tablename__ = 'challenges'
    challange_id = Column(String, primary_key=True)
    title = Column(String)
    create_time = Column(String)
    metrics = Column(String)
    content = Column(Text)

class Submissions(Base):
    __tablename__ = 'submissions'
    submission_id = Column(String, primary_key=True)
    result = Column(JSON)
    submission_time = Column(String)
    c_id = Column(String, ForeignKey("challenges.challange_id"))
    status = Column(String)