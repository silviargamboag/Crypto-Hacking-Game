from flask import Flask
from .Alertmail import checkalert 
from flask_mail import Mail, Message

app = Flask(__name__)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'soniaperezgarnica@gmail.com',
	MAIL_PASSWORD = 'Twiga2017'
	)
mail = Mail(app)
checkalert()

if __name__ =='__main__':
    app.run(debug = True)

from . import Usercontroller
app.register_blueprint(Usercontroller.bp)

from . import Authcontroller
app.register_blueprint(Authcontroller.bp)

from . import Alertcontroller
app.register_blueprint(Alertcontroller.bp)