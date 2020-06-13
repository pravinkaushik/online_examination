from model.user import User, session_user_app


def validate_user(email, password_hash):
    user = User.query.filter_by(email=email, password_hash=password_hash, is_active=1).first()
    return user


def validate_user_email(email):
    user = User.query.filter_by(email=email, is_active=1).first()
    return user


def create_user(user):
    session_user_app.add(user)
    session_user_app.commit()
    return user
