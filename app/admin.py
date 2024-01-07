from flask import redirect, request
from app import admin, db, dao
from app.models import HangMayBay, SanBay, TuyenBay, ChuyenBay, SanBayDung, BangDonGia, NguoiDung, HangVe, VeChuyenBay, \
    UserRole
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.loainguoidung == UserRole.ADMIN


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.loainguoidung == UserRole.ADMIN


class Authenticated2View(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class Authenticated2ModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and (current_user.loainguoidung == UserRole.STAFF
                                                  or current_user.loainguoidung == UserRole.ADMIN)


class LogoutView(Authenticated2View):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        stats = dao.flightroute_stats(from_date=request.args.get('from_date'), to_date=request.args.get('to_date'))
        return self.render('admin/stats.html', stats=stats)


class HangMayBayModelView(AuthenticatedModelView):
    column_filters = ['ten']
    column_searchable_list = ['ten']
    column_exclude_list = ['gioithieu', 'hinhanh']
    can_view_details = True
    can_export = True
    column_labels = {
        'ten': 'Tên hãng máy bay',
        'gioithieu': 'Giới thiệu',
        'hinhanh': 'Hình ảnh'
    }
    page_size = 10


class SanBayModelView(AuthenticatedModelView):
    column_filters = ['ten']
    column_searchable_list = ['ten']
    can_view_details = True
    can_export = True
    column_labels = {
        'ten': 'Tên sân bay',
    }
    page_size = 10


class TuyenBayModelView(AuthenticatedModelView):
    column_filters = ['ten', 'sanbaydi', 'sanbayden']
    column_searchable_list = ['ten']
    can_view_details = True
    can_export = True
    column_labels = {
        'ten': 'Tên tuyến bay',
        'sanbaydi': 'Sân bay đi',
        'sanbayden': 'Sân bay đến',
    }
    page_size = 10


class ChuyenBayModelView(Authenticated2ModelView):
    column_filters = ['tuyenbay']
    can_view_details = True
    can_export = True
    column_labels = {
        'giodi': 'Giờ đi',
        'thoigianbay': 'Thời gian bay',
        'hangmaybay': 'Hãng máy bay',
        'tuyenbay': 'Tuyến bay',
    }
    page_size = 10


class SanBayDungModelView(AuthenticatedModelView):
    column_filters = ['chuyenbay_ma']
    can_view_details = True
    can_export = True
    column_labels = {
        'thoigiandung': 'Thời gian dừng',
        'sanbay': 'Sân bay',
        'chuyenbay': 'Chuyến bay',
    }
    page_size = 10


class ChiTietChuyenBayModelView(AuthenticatedModelView):
    column_filters = ['chuyenbay_ma']
    can_view_details = True
    can_export = True
    column_labels = {
        'gia': 'Giá',
        'soghe': 'Số ghế',
        'chuyenbay': 'Chuyến bay',
        'hangve': 'Hạng vé',

    }
    page_size = 10


class HangVeModelView(AuthenticatedModelView):
    can_export = True
    can_view_details = True
    column_labels = {
        'ten': 'Tên hạng vé'
    }
    page_size = 10


class NguoiDungModelView(AuthenticatedModelView):
    column_filters = ['loainguoidung']
    can_view_details = True
    can_export = True
    column_exclude_list = ['matkhau', 'anhdaidien']
    column_searchable_list = ['ten']
    can_view_details = True
    column_labels = {
        'ten': 'Tên người dùng',
        'taikhoan': 'Tài khoản',
        'matkhau': 'Mật khẩu',
        'anhdaidien': 'Ảnh đại diện',
        'hoatdong': 'Hoạt động',
        'loainguoidung': 'Loại người dùng',
    }
    page_size = 10


class VeChuyenBayModelView(AuthenticatedModelView):
    can_export = True
    can_view_details = True
    column_labels = {
        'tennguoidi': 'Tên người đi',
        'cccd': 'Căn cước công dân',
        'Ngaydat': 'Ngày đặt vé',
        'nguoidung': 'Người dùng',
        'bangdongia': 'Chi tiết chuyến đi',
    }
    page_size = 10


admin.add_view(HangMayBayModelView(HangMayBay, db.session, name='Hãng máy bay'))
admin.add_view(SanBayModelView(SanBay, db.session, name='Sân bay'))
admin.add_view(TuyenBayModelView(TuyenBay,  db.session, name='Tuyến bay'))
admin.add_view(ChuyenBayModelView(ChuyenBay, db.session, name='Chuyến bay'))
admin.add_view(SanBayDungModelView(SanBayDung, db.session, name='Sân bay dừng'))
admin.add_view(ChiTietChuyenBayModelView(BangDonGia, db.session, name='Chi tiết chuyến bay'))
admin.add_view(HangVeModelView(HangVe, db.session, name='Hạng vé'))
admin.add_view(NguoiDungModelView(NguoiDung, db.session, name='Người dùng'))
admin.add_view(VeChuyenBayModelView(VeChuyenBay, db.session, name='Vé'))
admin.add_view(StatsView(name='BC-TK'))
admin.add_view(LogoutView(name='Đăng xuất'))


