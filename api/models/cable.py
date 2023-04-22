from datetime import datetime
from utils import db

class CableModel(db.Model):
    __tablename__ = "cable"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(10), nullable=False, unique=True)
    subscriber_number = db.Column(db.Integer, nullable=False)
    package_name = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_json(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'subscriber_number': self.subscriber_number,
            'package_name': self.package_name,
            'order_date': self.created_at.isoformat()
        }

    def __repr__(self):
        return f"<AirtimePurchase(amount={self.amount}, phone_number='{self.phone_number}', created_at='{self.created_at}')>"
    