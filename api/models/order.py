from datetime import datetime
from utils import db

class OrderModel(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(10), nullable=False, unique=True)
    amount = db.Column(db.Float, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_json(self):
        return {
            'id': self.id,
            'phone_number': self.phone_number,
            'order_id ': self.order_id ,
            'amount': self.amount,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f"<AirtimePurchase(amount={self.amount}, phone_number='{self.phone_number}', created_at='{self.created_at}')>"
    

