from flask import redirect, request
from app import db, dao, app
from app.models import HangMayBay, SanBay, TuyenBay, ChuyenBay, SanBayDung, BangDonGia, NguoiDung, HangVe, VeChuyenBay, \
    UserRole
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, Admin, AdminIndexView
from flask_login import logout_user, current_user
from wtforms import ValidationError
from wtforms.fields import PasswordField



# class MyAdmin(AdminIndexView):
#     @expose('/')
#     def index(self):
#         return self.render('admin/index.html', stats=dao.flightroute_stats() )
admin = Admin(app=app, name='QUẢN TRỊ', template_mode='bootstrap4')
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
        'ma_hang': 'Mã hãng bay',
        'ten': 'Tên hãng máy bay',
        'gioithieu': 'Giới thiệu',
        'hinhanh': 'Hình ảnh'
    }
    page_size = 10
    form_columns =('ma_hang','ten','gioithieu','hinhanh')


class SanBayModelView(AuthenticatedModelView):
    column_filters = ['ten']
    column_searchable_list = ['ten']
    can_view_details = True
    can_export = True
    column_labels = {
        'ten': 'Tên sân bay',

        'masanbay': 'Mã Sân Bay',
        'vitri': 'Vị Trí'
    }
    page_size = 10
    form_columns = ('ten', 'masanbay', 'vitri')


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
    form_columns = ('ten', 'sanbaydi', 'sanbayden')
    #hàm kiểm tra thay đổi trong form và gọi hàm check_same_airport
    def on_model_change(self, form, model, is_created):

        self.check_same_airport(model.sanbaydi, model.sanbayden)
    #hàm check trùng sân bay
    def check_same_airport(self, sanbaydi, sanbayden):
        if sanbaydi == sanbayden:
            raise ValidationError('trùng sân bay vui lòng chọn lại')



class ChuyenBayModelView(Authenticated2ModelView):
    column_filters = ['tuyenbay']
    can_view_details = True
    can_export = True
    column_labels = {
        'ten_cb': 'Tên chuyến bay',
        'giodi': 'Giờ đi',
        'thoigianbay': 'Thời gian bay',
        'hangmaybay': 'Hãng máy bay',
        'tuyenbay': 'Tuyến bay',

    }
    page_size = 10
    form_columns = ('ten_cb','giodi', 'thoigianbay', 'hangmaybay', 'tuyenbay')
    def on_model_change(self, form, model, is_created):
        if model.thoigianbay < 30:
            raise ValidationError('Thời gian bay tối thiểu là 30 phút')
        return super(ChuyenBayModelView, self).on_model_change(form, model, is_created)


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

    def on_model_change(self, form, model, is_created):
        if (model.thoigiandung < 20) or model.thoigiandung >30:
            raise ValidationError('Thời gian bay dừng phải trong khoảng từ 20 đến 30 phút')
        return super(SanBayDungModelView, self).on_model_change(form, model, is_created)


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
    form_columns = ('gia', 'soghe', 'chuyenbay', 'hangve')
    def on_model_change(self, form, model, is_created):
        if model.soghe < 0:
            raise ValidationError('số ghế phải lớn hơn 0')

        return super(ChiTietChuyenBayModelView, self).on_model_change(form, model, is_created)


class HangVeModelView(AuthenticatedModelView):
    can_export = True
    can_view_details = True
    column_labels = {
        'ten': 'Tên hạng vé'
    }

    page_size = 10
    form_columns = ['ten']



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
    # column_list = ['nguoidung_ma']
    # dấu kí tự password
    form_overrides = {
        'matkhau': PasswordField
    }
    form_excluded_columns = ['ves']
    # column_list = ('tennguoidi', 'nguoidung_ma')
    #kiểm tra hàm nhập phone xem đã có trong db chưa
    def on_model_change(self, form, model):

        phone_form = form.phone.data
        cccd_form = form.cccd.data
        passport_form = form.passport.data


        if NguoiDung.query.filter_by(phone=phone_form).first():
            raise ValidationError('SĐT đã được đăng kí trước đó')

        if NguoiDung.query.filter_by(cccd=cccd_form).first():
            raise ValidationError('Số CCCD đã được đăng kí trước đó')
        if NguoiDung.query.filter_by(passport= passport_form).first():
            raise ValidationError('Passport đã được  đăng kí trước đó')

        return super(NguoiDungModelView, self).on_model_change(form, model)

class VeChuyenBayModelView(Authenticated2ModelView):
    can_export = True
    can_view_details = True
    column_labels = {
        'tennguoidi': 'Tên người đi',
        'cccd': 'Căn cước công dân',
        'Ngaydat': 'Ngày đặt vé',
        'nguoidung_ma': 'Mã Người dùng',
        'bangdongia': 'Gia'
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


