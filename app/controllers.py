from flask import render_template, request, redirect
from flask_login import login_user, logout_user
from app import dao
from datetime import timedelta, datetime
# import cloudinary.uploader


def index():
    airlines = dao.load_airlines()
    airports = dao.load_sanbays()
    hangves = dao.load_hangves()
    return render_template('index.html', airlines=airlines, airports=airports, hangves=hangves)


def airline():
    airlines = dao.load_airlines()
    airline_id = request.args.get("airline_id")
    b = dao.get_airline_by_id(airline_id)
    airports = dao.load_sanbays()
    return render_template('airline.html', airlines=airlines, b=b, airports=airports)


def flight():
    airlines = dao.load_airlines()
    airport1 = dao.get_airport_by_name(request.args.get("airport1"))
    airport2 = dao.get_airport_by_name(request.args.get("airport2"))
    if airport1 and airport2:
        a = dao.get_flightroute(airport1, airport2)
        if a:
            al = request.args.get("airline")
            date = request.args.get("departuretime")
            dt = datetime.strptime(date, "%Y-%m-%d") + timedelta(hours=12)
            flights = dao.load_flights(a, al, dt)
            return render_template('flights.html', airlines=airlines, a=a, flights=flights)
        else:
            return render_template('flights.html', airlines=airlines, flights=None)
    else:
        return render_template('flights.html', airlines=airlines, flights=None)


def flight_details():
    airlines = dao.load_airlines()
    flight_id = request.args.get("flight_id")
    fl = dao.get_flight_by_id(flight_id)
    fr = dao.get_flightroute_by_id(fl.tuyenbay_ma)
    a1 = dao.get_airport_by_id(fr.sanbaydi_ma)
    a2 = dao.get_airport_by_id(fr.sanbayden_ma)
    bdgs = dao.load_bangdongias(fl.id)
    hvs = dao.load_hangves()
    sbds = dao.load_sanbaydungs()
    sbs = dao.load_sanbays()
    return render_template('flight-details.html', airlines=airlines, fl=fl, a1=a1, a2=a2, bdgs=bdgs, hvs=hvs,
                           sbds=sbds, sbs=sbs)


def contact():
    airlines = dao.load_airlines()
    return render_template('contact.html', airlines=airlines)


def login_admin():
    username = request.form.get("username")
    password = request.form.get("password")

    user = dao.auth_user(username=username, password=password)

    if user:
        login_user(user=user)

    return redirect('/admin')


def register():
    err_msg = ''
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']

        if password.__eq__(confirm):
            avatar = ''
            # if request.files:
            #     res = cloudinary.uploader.upload(request.files['avatar'])
            #     avatar = res['secure_url']
            try:
                dao.register(name=request.form['name'],
                             username=request.form['username'],
                             password=request.form['password'],
                             avatar=avatar)

                return redirect('/login')

            except:
                err_msg = 'Có lỗi xảy ra! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!'

    return render_template('register.html', err_msg=err_msg)


def login_my_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user)

            u = request.args.get('next')
            return redirect(u if u else '/')

    return render_template('login.html')


def logout_my_user():
    logout_user()
    return redirect('/')


def pay():
    bangdongia = request.args.get("bangdongia")
    tenhanhkhach = request.args.get("tenhanhkhach")
    cccd = request.args.get("cccd")
    dao.add_ticket(tenhanhkhach, cccd, bangdongia)
    return redirect('/')

