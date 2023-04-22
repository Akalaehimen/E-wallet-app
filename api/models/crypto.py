from datetime import datetime
from utils import db

class CryptoModel(db.Model):
    __tablename__ = "crypto"
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(25), nullable=False, unique=True)
    date_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    
    
    def __repr__(self):
        return f"<Student {self.address}>"