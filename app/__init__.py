from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote

from flask_login import LoginManager


app = Flask(__name__)

app.secret_key = '$#&*&%$(*&^(*^*&%^%$#^%&^%*&56547648764%$#^%$&12312^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/baitaplon?charset=utf8mb4' % quote(
    '17Hoang08@')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)


login = LoginManager(app=app)

import cloudinary

cloudinary.config(
    cloud_name="dtcjtwznh",
    api_key="137131721752293",
    api_secret="2piWuAlUnTFlpWCaDI8BKiObYoo"
)