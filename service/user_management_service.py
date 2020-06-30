from webApp.model.user import User, session_user_app
from flask import Flask, current_app

candidate_app = Flask(__name__)

with candidate_app.app_context():
    @candidate_app.teardown_appcontext
    def shutdown_session(exception=None):
        session_user_app.remove()


def validate_user(email, password_hash):
    user = session_user_app.query(User).filter_by(email=email, password_hash=password_hash, is_active=1).first()
    session_user_app.commit()
    return user


def validate_user_email(email):
    user = session_user_app.query(User).filter_by(email=email, is_active=1).first()
    session_user_app.commit()
    return user


def activate_user(activation_link):
    user = session_user_app.query(User).filter_by(activation_link=activation_link).update(
        {'is_active': 1})
    session_user_app.commit()
    return user


def reset_user_password(email, password, activation_link):
    user = session_user_app.query(User).filter_by(email=email).update(
        {'password_hash': password, 'activation_link': activation_link, 'is_active': 0})
    session_user_app.commit()
    return user


def validate_user_email_all_status(email):
    user = session_user_app.query(User).filter_by(email=email).first()
    session_user_app.commit()
    return user


def create_user(user):
    session_user_app.add(user)
    session_user_app.commit()
    return user
