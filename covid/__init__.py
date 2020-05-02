import os
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
###############################################################################################


app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['DEBUG'] = True
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'khushi1872k@gmail.com'
app.config['MAIL_PASSWORD'] = 'ThisisKhushi'
app.config['MAIL_DEFAULT_SENDER'] = 'khushi1872k@gmail.com'
app.config['MAIL_ASCII_ATTACHMENTS'] = False
app.config['MAIL_MAX_EMAILS'] = None

db = SQLAlchemy(app)
Migrate(app,db)
mail = Mail(app)

########################################################################################3333

from covid.requirements.views import requirements
app.register_blueprint(requirements)

###################################################################################################3
@app.route('/')
def home():
    return render_template('home.html')




