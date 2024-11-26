from . import db
from datetime import datetime

class UserAction(db.Model):
    __tablename__ = 'user_action'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    session_id = db.Column(db.Integer, nullable=False)
    action_type = db.Column(db.String(50), nullable=False)
    target = db.Column(db.String(255), nullable=False)
    count = db.Column(db.Integer, default=1)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'action_type': self.action_type,
            'target': self.target,
            'count': self.count,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        } 