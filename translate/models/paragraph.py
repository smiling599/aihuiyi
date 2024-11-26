from . import db
import json

class Paragraph(db.Model):
    __tablename__ = 'paragraph'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    word_map = db.Column(db.Text)
    sentence_map = db.Column(db.Text)
    
    def get_maps(self):
        return {
            'content': self.content,
            'word_map': json.loads(self.word_map) if self.word_map else {},
            'sentence_map': json.loads(self.sentence_map) if self.sentence_map else {}
        } 