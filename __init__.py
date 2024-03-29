from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
from webApp.exam_config_management import exam_setup_api
from webApp.exam_process import exam_process_api
from webApp.user_management import user_management_api
from flask_mail import Mail

#config_obj = os.environ.get("DIAG_CONFIG_MODULE", "config.test")
app = Flask(__name__)
#app.config.from_object(config_obj)
#app.config.from_object('config.ProdConfig')
app.config.from_pyfile('/var/www/html/webApp/webApp/configx/test.py')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
mail = Mail(app)

app.register_blueprint(exam_process_api)
app.register_blueprint(user_management_api)
app.register_blueprint(exam_setup_api)
CORS(app)
#app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!

jwt = JWTManager(app)
jwt._set_error_handler_callbacks(app)
# Create a function that will be called whenever create_access_token
# is used. It will take whatever object is passed into the
# create_access_token method, and lets us define what custom claims
# should be added to the access token.
@jwt.user_claims_loader
def add_claims_to_access_token(user):
    print(user)
    return {'id': user.id, 'roles': user.roles}


# Create a function that will be called whenever create_access_token
# is used. It will take whatever object is passed into the
# create_access_token method, and lets us define what the identity
# of the access token should be.
@jwt.user_identity_loader
def user_identity_lookup(user):
    print(user)
    return user.email

if __name__ == '__main__':
    app.run()
