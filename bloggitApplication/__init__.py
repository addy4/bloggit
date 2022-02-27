from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 
from flask_mail import Mail
import bloggitApplication.keys as keyfile

#SQLAlchemy is an object relational mapper allowing us to access data in an object oriented manner.

app = Flask(__name__, template_folder='view') 

app.config['SECRET_KEY'] = '43f8cdbdc26cb3c699ccaf4d78159ee9'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = keyfile.KEYS['email']
app.config['MAIL_PASSWORD'] = keyfile.KEYS['password']
mail = Mail(app)
db = SQLAlchemy(app)  
bcrypt = Bcrypt(app) 
login_init = LoginManager(app) 
login_init.login_view = 'login_me'
login_init.login_message_category = 'info'

#How is LoginManager useful ? 
#We add some functionality to the database models and this will handle all the sessions in the background for us. 

from bloggitApplication import routes
