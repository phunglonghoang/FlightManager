from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Time, Text
from app import db, app
from sqlalchemy.orm import relationship
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2
    STAFF = 3


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class HangMayBay(BaseModel):
    __tablename__ = 'hangmaybay'
    ma_hang = Column(String(5), nullable = False, unique=True)
    ten = Column(String(50), nullable=False, unique=True)
    gioithieu = Column(Text, nullable=False)
    hinhanh = Column(Text, nullable=False)
    chuyenbays = relationship('ChuyenBay', backref='hangmaybay', lazy=False)

    def __str__(self):
        return str(self.ten)

class SanBay(BaseModel):
    __tablename__ = 'sanbay'
    masanbay = Column(String(3), nullable=False, unique=True)
    ten = Column(String(50), nullable=False, unique=True)
    sanbaydungs = relationship('SanBayDung', backref='sanbay', lazy=False)
    vitri = Column(String(50), nullable=False)

    def __str__(self):
        return str(self.ten)

class TuyenBay(BaseModel):
    __tablename__ = 'tuyenbay'

    ten = Column(String(50), nullable=False)
    sanbaydi_ma = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    sanbayden_ma = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    chuyenbays = relationship('ChuyenBay', backref='tuyenbay', lazy=False)
    sanbaydi = relationship("SanBay", foreign_keys=[sanbaydi_ma])
    sanbayden = relationship("SanBay", foreign_keys=[sanbayden_ma])
    def __str__(self):
        return str(self.ten)



class ChuyenBay(BaseModel):
    __tablename__ = 'chuyenbay'
    ten_cb = Column(String(50), nullable = False)
    giodi = Column(DateTime, nullable=False)
    thoigianbay = Column(Integer, nullable=False)
    hangmaybay_ma = Column(Integer, ForeignKey(HangMayBay.id), nullable=False)
    tuyenbay_ma = Column(Integer, ForeignKey(TuyenBay.id), nullable=False)
    sanbaydungs = relationship('SanBayDung', backref='chuyenbay', lazy=False)
    bangdongias = relationship('BangDonGia', backref='chuyenbay', lazy=False)

    def __str__(self):
        return str(self.ten_cb)


class SanBayDung(BaseModel):
    __tablename__ = 'sanbaydung'

    sanbay_ma = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    thoigiandung = Column(Integer, nullable=False)
    chuyenbay_ma = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)


class NguoiDung(BaseModel, UserMixin):
    __tablename__ = 'nguoidung'

    ten = Column(String(50), nullable=False)
    taikhoan = Column(String(50), nullable=False, unique=True)
    matkhau = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=False)
    cccd = Column(String(20), nullable=False)
    passport = Column(String(20), nullable=False)
    hoatdong = Column(Boolean, default=True)
    loainguoidung = Column(Enum(UserRole), default=UserRole.USER)
    anhdaidien = Column(String(100), nullable=False)

    def __str__(self):
        return str(self.ten)


class HangVe(BaseModel):
    __tablename__ = 'hangve'

    ten = Column(String(50), nullable=False, unique=True)
    bangdongias = relationship('BangDonGia', backref='hangve', lazy=True)

    def __str__(self):
        return str(self.ten)


class BangDonGia(BaseModel):
    __tablename__ = 'bangdongia'

    hangve_ma = Column(Integer, ForeignKey(HangVe.id), nullable=False)
    chuyenbay_ma = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    gia = Column('giatien', Float, default=0)
    vechuyenbays = relationship('VeChuyenBay', backref='bangdongia', lazy=True)
    soghe = Column(Integer, nullable=False)


class VeChuyenBay(BaseModel):
    __tablename__ = 'vechuyenbay'

    tennguoidi = Column(String(50), nullable=False)
    cccd = Column(String(20), nullable=False)
    nguoidung_ma = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
    bangdongia_ma = Column(Integer, ForeignKey(BangDonGia.id), nullable=False)
    Ngaydat = Column(DateTime, default=datetime.now())

# class HoaDon(BaseModel):
#     __tablename__ = 'hoadon'
#
#     ngayxuat = Column(DateTime, default=datetime.now(), nullable=False)
#     tongtien = Column(Float, nullable=False)
#     nguoidung_ma = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
#     vechuyenbay_ma = Column(Integer, ForeignKey(VeChuyenBay.id), nullable=False)
#     nguoidung = relationship("NguoiDung", backref="hoadons")
#     vechuyenbay = relationship("VeChuyenBay", backref="hoadons")
#
#     def __str__(self):
#         return f"HoaDon {self.id}"
#
#
# class History(BaseModel):
#     __tablename__ = 'history'
#
#     nguoidung_ma = Column(Integer, ForeignKey(NguoiDung.id), nullable=False)
#     chuyenbay_ma = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
#     ngaydat = Column(DateTime, default=datetime.now(), nullable=False)
#     nguoidung = relationship("NguoiDung", backref="histories")
#     chuyenbay = relationship("ChuyenBay", backref="histories")
#
#     def __str__(self):
#         return f"History {self.id} - User {self.nguoidung_ma}"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # v1 = HangVe(ten='Hạng 1')
        # v2 = HangVe(ten='Hạng 2')
        # db.session.add_all([v1, v2])
        # db.session.commit()

        # import hashlib
        #
        # password = str(hashlib.md5('123'.encode('utf-8')).hexdigest())
        # u1 = NguoiDung(ten='Hoang', taikhoan='admin', matkhau=password,phone='123456', cccd='392139213',passport='222', loainguoidung=UserRole.ADMIN,)
        # u2 = NguoiDung(ten='Hoang', taikhoan='staff', matkhau=password, phone='123456', cccd='321321321',
        #                passport='222', loainguoidung=UserRole.STAFF, )
        #
        # u3 = NguoiDung(ten='ND1', taikhoan='user1', matkhau=password, phone='123256', cccd='3213212321',
        #                passport='22221', loainguoidung=UserRole.USER, )
        # db.session.add_all([u1, u2, u3])
        # db.session.commit()

        #
        # # Hang may bay
        #
        # c1 = HangMayBay(ma_hang='HVN',ten='Vietnam Airlines',
        #                 gioithieu="Là một Hãng hàng không quốc gia có quy mô hoạt động toàn cầu và có tầm cỡ tại khu vực.Vietnam Airlines cam kết sẽ luôn đồng hành cùng các cổ đông, minh bạch công khai thông tin, duy trì và nâng cao các kênh đối thoại mở với cổ đông, tổ chức hoạt động kinh doanh an toàn, chất lượng và có hiệu quả trên cơ sở cân đối hài hòa lợi ích của cổ đông với việc đáp ứng nhu cầu phát triển kinh tế của đất nước.",
        #                 hinhanh="https://res.cloudinary.com/dfzvtpwsd/image/upload/v1669997776/T%C6%B0_v%E1%BA%A5n_ajewn9.jpg")
        # c2 = HangMayBay(ma_hang='BAV', ten='Bamboo Airwayss',
        #                 gioithieu="Là hãng hàng không tư nhân đầu tiên tại Việt Nam xác định theo đuổi mục tiêu cung cấp dịch vụ hàng không định hướng chuẩn quốc tế. Trên hành trình sải cánh vươn xa, chiến lược cốt lõi của Bamboo Airways là kết nối các vùng đất tiềm năng, góp phần quảng bá sâu rộng và hiệu quả giá trị tốt đẹp của văn hoá, con người Việt Nam tới bạn bè thế giới.",
        #                 hinhanh="https://res.cloudinary.com/dfzvtpwsd/image/upload/v1669997776/Bamboo_Airways_khai_th%C3%A1c_an_to%C3%A0n_1_000_chuy%E1%BA%BFn_bay_trong_5_tu%E1%BA%A7n_t%C3%ADnh_t%C4%83ng_l%C3%AAn_100_chuy%E1%BA%BFn_ng%C3%A0y_a0ifja.jpg")
        # c3 = HangMayBay(ma_hang='VJC',ten='Vietjet Air',
        #                 gioithieu="Là hãng hàng không đầu tiên tại Việt Nam vận hành theo mô hình hàng không thế hệ mới, chi phí thấp và cung cấp đa dạng các dịch vụ cho khách hàng lựa chọn. Hãng không chỉ vận chuyển hàng không mà còn cung cấp các nhu cầu tiêu dùng hàng hoá và dịch vụ cho khách hàng thông qua các ứng dụng công nghệ thương mại điện tử tiên tiến.",
        #                 hinhanh="https://res.cloudinary.com/dfzvtpwsd/image/upload/v1669997775/Airbus_A321XLR_pour_VietJet_A350-900_pour_South_African_Airways___Air_Journal_cblehe.jpg")
        # c4 = HangMayBay(ma_hang='PIC',ten='Pacific Airlines',
        #                 gioithieu="Hãng hàng không Pacific Airlines được biết tới là hàng hàng không đi tiên phong trong mảng vé máy bay giá rẻ tại Việt Nam. Mục tiêu hoạt động là đem đến những tấm vé máy bay giá rẻ tới tận tay người tiêu dung hàng ngày. Có thể nói Pacific Airlines Là một bước ngoặc lớn trong ngành hàng không vận chuyển và trong thời đại kinh tế thị trường đầy biến động hiện nay.",
        #                 hinhanh="https://res.cloudinary.com/dfzvtpwsd/image/upload/v1669998060/Web_maybay_zikhqo.jpg")
        # c5 = HangMayBay(ma_hang='JQ', ten='Jetstar',
        #                 gioithieu="Có thể, bạn biết đến chúng tôi như hãng hàng không nổi tiếng về cung cấp giá vé rẻ. Nhưng bạn có biết rằng mỗi tuần chúng tôi thực hiện hơn 5,000 chuyến bay đến hơn 85 điểm đến hay chúng tôi đã giúp quyên góp được hơn 10 triệu đô la Úc. Bạn có thể theo các liên kết tại đây để tìm hiểu triết lý kinh doanh của chúng tôi, về đội bay đầy ấn tượng của chúng tôi và các cơ hội để BẠN có thể đến với Jetstar.",
        #                 hinhanh="https://res.cloudinary.com/dfzvtpwsd/image/upload/v1669998050/a321_neo_ugtnjh.jpg")
        # db.session.add_all([c1, c2, c3, c4, c5])
        # db.session.commit()
        #
        #
        # #sân bay
        # sb1 = SanBay(masanbay="BMV", ten="Sân bay Buôn Ma Thuột", vitri="Đắk Lắk")
        # sb2 = SanBay(masanbay="DAD", ten="Sân bay quốc tế Đà Nẵng", vitri="Đà Nẵng")
        # sb3 = SanBay(masanbay="HAN", ten="Sân bay quốc tế Nội Bài", vitri="Hà Nội")
        # sb4 = SanBay(masanbay="SGN", ten="Sân bay quốc tế Tân Sơn Nhất", vitri="Thành phố Hồ Chí Minh")
        # sb5 = SanBay(masanbay="CXR", ten="Sân bay quốc tế Cam Ranh", vitri="Khánh Hòa")
        # sb6 = SanBay(masanbay="PQC", ten="Sân bay quốc tế Phú Quốc", vitri="Kiên Giang")
        # sb7 = SanBay(masanbay="NGO", ten="Sân bay quốc tế Chubu", vitri="Nagoya")
        # sb8 = SanBay(masanbay="ICN", ten="Sân bay quốc tế Incheon", vitri="Hàn Quốc")
        # sb9 = SanBay(masanbay="LAX", ten="Sân bay quốc tế Los Angeles", vitri="Los Angeles")
        # sb10 = SanBay(masanbay="MVD", ten="Sân bay quốc tế Carrasco", vitri="Montevideo")
        # db.session.add_all([sb1, sb2, sb3, sb4, sb5, sb6, sb7, sb8, sb9, sb10])
        # db.session.commit()
        #
        # t1 = TuyenBay(ten="Buôn Ma Thuột - Đà Nẵng", sanbaydi_ma=1, sanbayden_ma=2)
        # t2 = TuyenBay(ten="Hà Nội - Sài Gòn ", sanbaydi_ma=3, sanbayden_ma=4)
        # t3 = TuyenBay(ten="Sài Gòn - LOS ", sanbaydi_ma=4, sanbayden_ma=9)
        # #
        # db.session.add_all([t1, t2, t3])
        # db.session.commit()
        # #chuyến bay
        # cb1 = ChuyenBay(ten_cb ="BMT- ĐN", giodi=datetime.strptime('01/10/24 02:55:00', '%m/%d/%y %H:%M:%S'), thoigianbay=90,
        #                hangmaybay_ma=1, tuyenbay_ma=1)
        # db.session.add_all([cb1])
        # db.session.commit()
        # #
        #
        #
        b1 = BangDonGia(hangve_ma=1, chuyenbay_ma=1, gia=1000000, soghe=20)
        b2 = BangDonGia(hangve_ma=2, chuyenbay_ma=1, gia=900000, soghe=15)
        # b3 = BangDonGia(hangve_ma=1, chuyenbay_ma=2, gia=800000, soghe=50)
        # b4 = BangDonGia(hangve_ma=1, chuyenbay_ma=3, gia=1300000, soghe=30)
        # b5 = BangDonGia(hangve_ma=2, chuyenbay_ma=3, gia=1000000, soghe=20)
        # b6 = BangDonGia(hangve_ma=1, chuyenbay_ma=4, gia=1000000, soghe=35)
        # b7 = BangDonGia(hangve_ma=2, chuyenbay_ma=4, gia=1500000, soghe=10)
        # b8 = BangDonGia(hangve_ma=1, chuyenbay_ma=5, gia=1000000, soghe=40)
        # b9 = BangDonGia(hangve_ma=1, chuyenbay_ma=6, gia=1300000, soghe=30)
        # b10 = BangDonGia(hangve_ma=2, chuyenbay_ma=7, gia=1000000, soghe=20)
        # b11 = BangDonGia(hangve_ma=1, chuyenbay_ma=8, gia=1000000, soghe=35)
        # b12 = BangDonGia(hangve_ma=2, chuyenbay_ma=9, gia=7500000, soghe=10)
        # b13 = BangDonGia(hangve_ma=1, chuyenbay_ma=10, gia=1000000, soghe=40)
        # db.session.add_all([b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13])
        # db.session.commit()
