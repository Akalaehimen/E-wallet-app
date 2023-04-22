from datetime import datetime
from utils import db

class CryptosModel(db.Model):
    __tablename__ = "cryptos"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(22), nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    
    
    def __repr__(self):
        return f"<Student {self.number}>"