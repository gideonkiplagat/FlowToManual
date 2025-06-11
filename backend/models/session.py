from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, DateTime
from . import db
from datetime import datetime

# class SessionRecording(db.Model):
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('user.id'))
#     name = Column(String(100))
#     timestamp = Column(DateTime, default=datetime.utcnow)
#     events = Column(LargeBinary)  # rrweb event JSON blob
#     screenshots = Column(LargeBinary)  # Optional screenshots blob
    
# models/session.py

class SessionRecording(db.Model):
    __tablename__ = 'session_recordings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    events = db.Column(db.LargeBinary, nullable=False)
    
    # Add this foreign key!
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
