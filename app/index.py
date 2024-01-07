from flask import request, redirect
from flask_login import login_user
from app import app, dao, controllers, login
from app.admin import *


app.add_url_rule('/', 'index', controllers.index)

app.add_url_rule('/airline', 'airline', controllers.airline)

app.add_url_rule('/flights', 'flights', controllers.flight)

app.add_url_rule('/flight-details', 'flight-details', controllers.flight_details)

app.add_url_rule('/contact', 'contact', controllers.contact)

app.add_url_rule('/login-admin', 'login-admin', controllers.login_admin, methods=['GET', 'POST'])

app.add_url_rule('/register', 'register', controllers.register, methods=['get', 'post'])

app.add_url_rule('/login', 'login-user', controllers.login_my_user, methods=['get', 'post'])

app.add_url_rule('/logout', 'logout', controllers.logout_my_user)

app.add_url_rule('/pay', 'pay', controllers.pay)


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(debug=True)
