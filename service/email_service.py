from flask_mail import Mail, Message
from flask import Flask, current_app
import os

script_dir = os.path.dirname(__file__)

# examination_name_placeholder activation_placeholder http://localhost:4200 exam_id_placeholder email_placeholder
# password_placeholder
user_app = Flask(__name__)
with user_app.app_context():
    # config_obj = os.environ.get("DIAG_CONFIG_MODULE", "configx.test")
    current_app.config.from_pyfile('/var/www/html/webApp/webApp/configx/test.py')
    # current_app.config.from_object('webApp.config.ProdConfig')
    # current_app.config.from_object(config_obj)
    mail = Mail(current_app)

    email_confirmation = None
    email_confirmation_path = "html/email_confirmation.html"
    ec_abs_file_path = os.path.join(script_dir, email_confirmation_path)
    with open(ec_abs_file_path, 'r') as file:
        email_confirmation = file.read().replace('\n', '')

    email_invitation = None
    email_invitation_path = "html/exam_invitation.html"
    ei_abs_file_path = os.path.join(script_dir, email_invitation_path)
    with open(ei_abs_file_path, 'r') as file:
        email_invitation = file.read().replace('\n', '')

    welcome = None
    welcome_path = "html/welcome.html"
    wc_abs_file_path = os.path.join(script_dir, welcome_path)
    with open(wc_abs_file_path, 'r') as file:
        welcome = file.read().replace('\n', '')

    result = None
    result_path = "html/result.html"
    ei_abs_file_path = os.path.join(script_dir, result_path)
    with open(ei_abs_file_path, 'r') as file:
        result = file.read().replace('\n', '')


    def send_activation_email(recipient, random_str):
        html_data = email_confirmation.replace("activation_placeholder", random_str)
        msg = Message("Email confirmation", sender=current_app.config["MAIL_USERNAME"], recipients=[recipient])
        msg.html = html_data
        mail.send(msg)
        return "Sent"


    def send_email_invitation(recipient, exam_id, exam_name, password, exam_title):
        html_data = email_invitation.replace("exam_name_placeholder", exam_name)
        html_data = html_data.replace("exam_title_placeholder", exam_title)
        html_data = html_data.replace("exam_id_placeholder", str(exam_id))
        html_data = html_data.replace("email_placeholder", recipient)
        html_data = html_data.replace("password_placeholder", password)

        msg = Message("Invitation Take Test", sender=current_app.config["MAIL_USERNAME"], recipients=[recipient])
        msg.html = html_data
        mail.send(msg)
        return "Sent"


    def send_welcome(recipient):
        html_data = welcome.replace("email_placeholder", recipient)
        msg = Message("Welcome Email", sender=current_app.config["MAIL_USERNAME"], recipients=[recipient])
        msg.html = html_data
        mail.send(msg)
        return "Sent"


    def send_enquiry(name, email, message):
        print("Sending email ===========================")
        msg = Message("Email enquiry" + name, sender=current_app.config["MAIL_USERNAME"],
                      recipients=["pravinkaushik.bsp@gmail.com"])
        msg.body = "email-" + email + " message-" + message

        print("Sending email1 ===========================" + current_app.config["MAIL_USERNAME"])
        mail.send(msg)
        return "Sent"


    def publish_result(recipient, exam_id, exam_name, marks, exam_title):
        html_data = result.replace("exam_name_placeholder", exam_name)
        html_data = html_data.replace("exam_title_placeholder", exam_title)
        html_data = html_data.replace("exam_id_placeholder", str(exam_id))
        html_data = html_data.replace("email_placeholder", recipient)
        html_data = html_data.replace("marks_placeholder", str(marks))

        msg = Message("Result has been published", sender=current_app.config["MAIL_USERNAME"], recipients=[recipient])
        msg.html = html_data
        mail.send(msg)
        return "Sent"