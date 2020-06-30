from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
from exam_config_management import exam_setup_api
from exam_process import exam_process_api
from user_management import user_management_api
from flask_mail import Mail

config_obj = os.environ.get("DIAG_CONFIG_MODULE", "config")
app = Flask(__name__)
app.config.from_object(config_obj)
app.config['PROPAGATE_EXCEPTIONS'] = True
db = SQLAlchemy(app)
mail = Mail(app)

app.register_blueprint(exam_process_api)
app.register_blueprint(user_management_api)
app.register_blueprint(exam_setup_api)
CORS(app)
#app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!

jwt = JWTManager(app)
# Create a function that will be called whenever create_access_token
# is used. It will take whatever object is passed into the
# create_access_token method, and lets us define what custom claims
# should be added to the access token.
@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'id': user.id, 'roles': user.roles}


# Create a function that will be called whenever create_access_token
# is used. It will take whatever object is passed into the
# create_access_token method, and lets us define what the identity
# of the access token should be.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.email

if __name__ == '__main__':
    app.run()