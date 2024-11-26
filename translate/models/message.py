from . import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = 'message'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    session_id = db.Column(db.Integer, nullable=False)
    thread_id = db.Column(db.String(255), nullable=False)
    user_content = db.Column(db.Text, nullable=False)
    ai_result = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'thread_id': self.thread_id,
            'user_content': self.user_content,
            'ai_result': self.ai_result,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        } 