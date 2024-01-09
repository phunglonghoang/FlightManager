import hashlib
from flask_login import current_user
from sqlalchemy import func

from app import db
from app.models import HangMayBay, SanBay, ChuyenBay, TuyenBay, NguoiDung, UserRole, BangDonGia, HangVe, SanBayDung, \
    VeChuyenBay


def load_airlines():
    return HangMayBay.query.all()


def get_airline_by_id(airline_id):
    return HangMayBay.query.get(airline_id)


def get_airport_by_name(airport=None):
    return SanBay.query.filter(SanBay.ten == airport.strip()).first()


def get_airport_by_id(a):
    return SanBay.query.filter(SanBay.id == a).first()


def load_sanbays():
    return SanBay.query.all()


def get_flightroute(airport1=None, airport2=None):
    return TuyenBay.query.filter(TuyenBay.sanbaydi_ma == airport1.id,
                                 TuyenBay.sanbayden_ma == airport2.id).first()


def get_flightroute_by_id(a=None):
    return TuyenBay.query.filter(TuyenBay.id == a).first()


def load_flights(flightroute=None, airline=None, d=None):
    query = db.session.query(ChuyenBay, BangDonGia) \
        .join(BangDonGia, ChuyenBay.id == BangDonGia.chuyenbay_ma) \
        .filter(d < ChuyenBay.giodi)

    if flightroute:
        query = query.filter(ChuyenBay.tuyenbay_ma == flightroute.id)
    if airline:
        query = query.filter(ChuyenBay.hangmaybay_ma == airline.id)

    flights = query.all()
    return flights



def get_flight_by_id(a):
    return ChuyenBay.query.get(a)


def auth_user(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return NguoiDung.query.filter(NguoiDung.taikhoan == username.strip(),
                                      NguoiDung.matkhau == password).first()


def get_user_by_id(user_id):
    return NguoiDung.query.get(user_id)


def register(name, username, password, avatar):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    user = NguoiDung(ten=name, taikhoan=username, matkhau=password, anhdaidien=avatar)
    db.session.add(user)
    db.session.commit()


def load_bangdongias(f=None):
    query = BangDonGia.query
    if f:
        query = query.filter(BangDonGia.chuyenbay_ma == f)

    return query.all()


def load_hangves():
    return HangVe.query.all()


def load_sanbaydungs():
    return SanBayDung.query.all()


def add_ticket(tennguoidi=None, cccd=None, bangdongia=None):
    ticket = VeChuyenBay(tennguoidi=tennguoidi, cccd=cccd, nguoidung_ma=current_user.id, bangdongia_ma=bangdongia)
    db.session.add(ticket)
    db.session.commit()


def flightroute_stats(from_date=None, to_date=None):
    query = db.session.query(TuyenBay.id, TuyenBay.ten, func.sum(BangDonGia.gia), func.count(ChuyenBay.id)) \
        .join(ChuyenBay, ChuyenBay.tuyenbay_ma == TuyenBay.id) \
        .join(BangDonGia, BangDonGia.chuyenbay_ma == ChuyenBay.id) \
        .join(VeChuyenBay, VeChuyenBay.bangdongia_ma == BangDonGia.id)
    if from_date:
        query = query.filter(VeChuyenBay.Ngaydat >= from_date)
    if to_date:
        query = query.filter(VeChuyenBay.Ngaydat <= to_date)
    return query.group_by(TuyenBay.ten).order_by(TuyenBay.id).all()
