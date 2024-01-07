from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_admin import Admin
from flask_login import LoginManager
# import cloudinary

app = Flask(__name__)

app.secret_key = '$#&*&%$(*&^(*^*&%^%$#^%&^%*&56547648764%$#^%$&12312^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/baitaplon?charset=utf8mb4' % quote(
    '17Hoang08@')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)

admin = Admin(app=app, name='QUẢN TRỊ', template_mode='bootstrap4')

login = LoginManager(app=app)

# cloudinary.config(cloud_name='dfzvtpwsd', api_key='717947668599675', api_secret='8txPYPx5A5YPpCCfJlTZBANubJg')
