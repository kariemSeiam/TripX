from app.models import Driver

def get_driver_by_user_id(user_id):
    return Driver.query.filter_by(user_id=user_id).first()

def get_driver_by_id(driver_id):
    return Driver.query.get(driver_id)
