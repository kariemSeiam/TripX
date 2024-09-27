"""
This module contains the database models for the TripX application.
Each class represents a table in the database.
"""

from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json


class User(db.Model):
    """Model for user accounts."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=False)
    profile_photo_url = db.Column(db.String(255), nullable=True)
    verification_code = db.Column(db.String(6), nullable=True)  # New field for verification code

    vehicles = db.relationship('Vehicle', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'



class Conversation(db.Model):
    """Model for user conversations."""
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    messages = db.relationship('Message', backref='conversation', lazy=True)

    def __repr__(self):
        return f'<Conversation {self.id}>'

class Message(db.Model):
    """Model for messages within a conversation."""
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    sender_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Message {self.id} in Conversation {self.conversation_id}>'


class Document(db.Model):
    """Model for user documents."""
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)
    file_url = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('documents', lazy=True))

    def __repr__(self):
        return f"<Document {self.document_type} for user {self.user_id}>"


class Notification(db.Model):
    """Model for user notifications."""
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    data = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return f'<Notification {self.id} - {self.title}>'



class Payment(db.Model):
    """Model for payments."""
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending', index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    driver = db.relationship('Driver', backref='payments', lazy=True)

    def __repr__(self):
        return f'<Payment {self.id} - {self.amount} {self.currency}>'

class Promotion(db.Model):
    """Model for promotions and discounts."""
    __tablename__ = 'promotions'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=False)
    discount_type = db.Column(db.String(20), nullable=False)  # percent or amount
    discount_value = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    usage_limit = db.Column(db.Integer, nullable=False, default=1)
    times_used = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Promotion {self.code}>'


class Driver(db.Model):
    """Model for drivers."""
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    license_number = db.Column(db.String(50), nullable=False, unique=True, index=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    rating = db.Column(db.Float, default=0.0)  # Average rating of the driver
    trip_count = db.Column(db.Integer, default=0)  # Count of trips completed

    user = db.relationship('User', backref=db.backref('drivers', lazy=True))
    vehicle = db.relationship('Vehicle', backref=db.backref('drivers', lazy=True))

    def __repr__(self):
        return f"<Driver {self.user.username} - {self.license_number}>"


class History(db.Model):
    """Model for user history related to trips."""
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<History {self.id}>'


class Rating(db.Model):
    """Model for ratings given by users."""
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    rider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    feedback = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Rating {self.id}>'




class Referral(db.Model):
    """Model for user referrals."""
    __tablename__ = 'referrals'

    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    referred_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    referral_code = db.Column(db.String(64), unique=True, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Referral {self.referral_code}>'


class Request(db.Model):
    """Model for user requests."""
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    request_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending', index=True)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('requests', lazy='dynamic'))

    def __repr__(self):
        return f'<Request {self.id} - {self.request_type}>'


class SupportTicket(db.Model):
    """Model for support tickets."""
    __tablename__ = 'support_tickets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = db.relationship('SupportMessage', backref='ticket', lazy=True)

    def __repr__(self):
        return f'<SupportTicket {self.id}>'

class SupportMessage(db.Model):
    """Model for messages within support tickets."""
    __tablename__ = 'support_messages'

    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('support_tickets.id'), nullable=False)
    sender_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<SupportMessage {self.id} in Ticket {self.ticket_id}>'


class Trip(db.Model):
    """Model for trips taken by users."""
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    rider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    start_location = db.Column(db.String(255), nullable=False)
    end_location = db.Column(db.String(255), nullable=False)
    fare = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='requested', index=True)
    started_at = db.Column(db.DateTime, nullable=True)
    ended_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    driver = db.relationship('Driver', backref='trips', lazy=True)
    rider = db.relationship('User', backref='trips', lazy=True)
    vehicle = db.relationship('Vehicle', backref='trips', lazy=True)

    def __repr__(self):
        return f'<Trip {self.id} - {self.status}>'



class Vehicle(db.Model):
    """Model for vehicles owned by users."""
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    license_plate = db.Column(db.String(20), unique=True, nullable=False, index=True)
    color = db.Column(db.String(20))
    vehicle_type = db.Column(db.String(20))
    vehicle_photo_urls = db.Column(db.String(255))  # Store as JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def photo_urls_list(self):
        """Return the vehicle photo URLs as a list."""
        return json.loads(self.vehicle_photo_urls) if self.vehicle_photo_urls else []

    @photo_urls_list.setter
    def photo_urls_list(self, urls):
        """Set the vehicle photo URLs from a list."""
        self.vehicle_photo_urls = json.dumps(urls)  # Store as JSON string

    def __repr__(self):
        return f'<Vehicle {self.make} {self.model}>'
class Withdrawal(db.Model):
    """Model for withdrawal requests made by drivers."""
    __tablename__ = 'withdrawals'

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending', index=True)
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)

    driver = db.relationship('Driver', backref='withdrawals', lazy=True)

    def __repr__(self):
        return f'<Withdrawal {self.id} - {self.amount} via {self.method}>'


class TokenBlacklist(db.Model):
    """Model for blacklisted tokens."""
    __tablename__ = 'token_blacklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    user_identity = db.Column(db.String(50), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, jti, token_type, user_identity, revoked, expires):
        self.jti = jti
        self.token_type = token_type
        self.user_identity = user_identity
        self.revoked = revoked
        self.expires = expires

    def __repr__(self):
        return f"<TokenBlacklist {self.jti}>"
