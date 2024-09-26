from app.extensions import db
from datetime import datetime

class Earning(db.Model):
    __tablename__ = 'earnings'

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default='pending')

    driver = db.relationship('Driver', backref='earnings', lazy=True)
    trip = db.relationship('Trip', backref='earnings', lazy=True)

    def __repr__(self):
        return f'<Earning {self.id} - {self.amount} {self.currency}>'
