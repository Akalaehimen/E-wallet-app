from datetime import datetime
from utils import db


class ElectModel(db.Model):
    __tablename__ = "elect"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(10), nullable=False, unique=True)
    amount = db.Column(db.Float, nullable=False)
    meter_number = db.Column(db.Integer, nullable=False)
    payment_mode = db.Column(db.String(20), nullable=False)
    provider = db.Column(db.String(20), nullable=False)
    service_charge = db.Column(db.Integer, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow)

    def to_json(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'amount': self.amount,
            'meter_number': self.meter_number,
            'payment_mode': self.payment_mode,
            'provider': self.provider,
            'service_charge': self.service_charge,
            'order_date': self.created_at.isoformat()
        }

    def __repr__(self):
        return f"<AirtimePurchase(amount={self.amount}, phone_number='{self.phone_number}', created_at='{self.created_at}')>"
