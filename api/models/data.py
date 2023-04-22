from datetime import datetime
from utils import db


class DataModel(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(10), nullable=False, unique=True)
    phone_number = db.Column(db.Integer, nullable=False)
    data_plan = db.Column(db.String(20), nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow)

    def to_json(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'phone_number': self.phone_number,
            'data_plan': self.data_plan,
            'order_date': self.created_at.isoformat()
        }

    def __repr__(self):
        return f"<AirtimePurchase(amount={self.amount}, phone_number='{self.phone_number}', created_at='{self.created_at}')>"
