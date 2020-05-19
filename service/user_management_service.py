
from model.user import User

def validate_user(email, password):
    user = User.query.filter_by(email=email).first()
    return user
