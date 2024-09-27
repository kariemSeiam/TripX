from app.models import User
from app.extensions import db

def get_user_by_id(user_id):
    return User.query.get(user_id)

def create_user(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user
