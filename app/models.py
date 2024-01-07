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

    ten = Column(String(50), nullable=False, unique=True)
    gioithieu = Column(Text, nullable=False)
    hinhanh = Column(Text, nullable=False)
    chuyenbays = relationship('ChuyenBay', backref='hangmaybay', lazy=False)

    def __str__(self):
        return self.ten


class SanBay(BaseModel):
    __tablename__ = 'sanbay'

    ten = Column(String(20), nullable=False, unique=True)
    sanbaydungs = relationship('SanBayDung', backref='sanbay', lazy=False)

    # sanbaydis = relationship('TuyenBay', backref='sanbaydi', lazy=False)
    # sanbaydens = relationship('TuyenBay', backref='sanbayden', lazy=False)

    def __str__(self):
        return self.ten


class TuyenBay(BaseModel):
    __tablename__ = 'tuyenbay'

    ten = Column(String(50), nullable=False)
    sanbaydi_ma = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    sanbayden_ma = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    chuyenbays = relationship('ChuyenBay', backref='tuyenbay', lazy=False)
    sanbaydi = relationship("SanBay", foreign_keys=[sanbaydi_ma])
    sanbayden = relationship("SanBay", foreign_keys=[sanbayden_ma])

    def __str__(self):
        return self.ten


class ChuyenBay(BaseModel):
    __tablename__ = 'chuyenbay'

    giodi = Column(DateTime, nullable=False)
    thoigianbay = Column(Integer, nullable=False)
    hangmaybay_ma = Column(Integer, ForeignKey(HangMayBay.id), nullable=False)
    tuyenbay_ma = Column(Integer, ForeignKey(TuyenBay.id), nullable=False)
    sanbaydungs = relationship('SanBayDung', backref='chuyenbay', lazy=False)
    bangdongias = relationship('BangDonGia', backref='chuyenbay', lazy=True)


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
    hoatdong = Column(Boolean, default=True)
    loainguoidung = Column(Enum(UserRole), default=UserRole.USER)
    anhdaidien = Column(String(100), nullable=False)
    vechuyenbays = relationship('VeChuyenBay', backref='nguoidung', lazy=True)

    def __str__(self):
        return self.ten


class HangVe(BaseModel):
    __tablename__ = 'hangve'

    ten = Column(String(50), nullable=False, unique=True)
    bangdongias = relationship('BangDonGia', backref='hangve', lazy=True)

    def __str__(self):
        return self.ten


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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        c1 = HangMayBay(ten='Vietnam Airlines',
                        gioithieu="Là một Hãng hàng không quốc gia có quy mô hoạt động toàn cầu và có tầm cỡ tại khu vực.Vietnam Airlines cam kết sẽ luôn đồng hành cùng các cổ đông, minh bạch công khai thông tin, duy trì và nâng cao các kênh đối thoại mở với cổ đông, tổ chức hoạt động kinh doanh an toàn, chất lượng và có hiệu quả trên cơ sở cân đối hài hòa lợi ích của cổ đông với việc đáp ứng nhu cầu phát triển kinh tế của đất nước.",
                        hinhanh="https://res.cloudinary.com/dfzvtpwsd/image/upload/v1669997776/T%C6%B0_v%E1%BA%A5n_ajewn9.jpg")
        c2 = HangMayBay(ten='Bamboo Airwayss',
                        gioithieu="Là hãng hàng không tư nhân đầu tiên tại Việt Nam xác định theo đuổi mục tiêu cung cấp dịch vụ hàng không định hướng chuẩn quốc tế. Trên hành trình sải cánh vươn xa, chiến lược cốt lõi của Bamboo Airways là kết nối các vùng đất tiềm năng, góp phần quảng bá sâu rộng và hiệu quả giá trị tốt đẹp của văn hoá, con người Việt Nam tới bạn bè thế giới.",
                        hinhanh="https://res.cloudinary.com/dfzvtpwsd/image/upload/v1669997776/Bamboo_Airways_khai_th%C3%A1c_an_to%C3%A0n_1_000_chuy%E1%BA%BFn_bay_trong_5_tu%E1%BA%A7n_t%C3%ADnh_t%C4%83ng_l%C3%AAn_100_chuy%E1%BA%BFn_ng%C3%A0y_a0ifja.jpg")
        c3 = HangMayBay(ten='Vietjet Air',
                        gioithieu="Là hãng hàng không đầu tiên tại Việt Nam vận hành theo mô hình hàng không thế hệ mới, chi phí thấp và cung cấp đa dạng các dịch vụ cho khách hàng lựa chọn. Hãng không chỉ vận chuyển hàng không mà còn cung cấp các nhu cầu tiêu dùng hàng hoá và dịch vụ cho khách hàng thông qua các ứng dụng công nghệ thương mại điện tử tiên tiến.",
                        hinhanh="https://res.cloudinary.com/dfzvtpwsd/image/upload/v1669997775/Airbus_A321XLR_pour_VietJet_A350-900_pour_South_African_Airways___Air_Journal_cblehe.jpg")
        c4 = HangMayBay(ten='Pacific Airlines',
                        gioithieu="Hãng hàng không Pacific Airlines được biết tới là hàng hàng không đi tiên phong trong mảng vé máy bay giá rẻ tại Việt Nam. Mục tiêu hoạt động là đem đến những tấm vé máy bay giá rẻ tới tận tay người tiêu dung hàng ngày. Có thể nói Pacific Airlines Là một bước ngoặc lớn trong ngành hàng không vận chuyển và trong thời đại kinh tế thị trường đầy biến động hiện nay.",
                        hinhanh="https://res.cloudinary.com/dfzvtpwsd/image/upload/v1669998060/Web_maybay_zikhqo.jpg")
        c5 = HangMayBay(ten='Jetstar',
                        gioithieu="Có thể, bạn biết đến chúng tôi như hãng hàng không nổi tiếng về cung cấp giá vé rẻ. Nhưng bạn có biết rằng mỗi tuần chúng tôi thực hiện hơn 5,000 chuyến bay đến hơn 85 điểm đến hay chúng tôi đã giúp quyên góp được hơn 10 triệu đô la Úc. Bạn có thể theo các liên kết tại đây để tìm hiểu triết lý kinh doanh của chúng tôi, về đội bay đầy ấn tượng của chúng tôi và các cơ hội để BẠN có thể đến với Jetstar.",
                        hinhanh="https://res.cloudinary.com/dfzvtpwsd/image/upload/v1669998050/a321_neo_ugtnjh.jpg")
        db.session.add_all([c1, c2, c3, c4, c5])
        db.session.commit()

        v1 = HangVe(ten='Hạng 1')
        v2 = HangVe(ten='Hạng 2')
        db.session.add_all([v1, v2])
        db.session.commit()

        import hashlib

        password = str(hashlib.md5('123'.encode('utf-8')).hexdigest())
        u1 = NguoiDung(ten='Hoang', taikhoan='admin', matkhau=password, loainguoidung=UserRole.ADMIN,
                       anhdaidien='https://res.cloudinary.com/dfzvtpwsd/image/upload/v1670221889/2_pzciij.png')
        u2 = NguoiDung(ten='Duc', taikhoan='staff', matkhau=password, loainguoidung=UserRole.STAFF,
                       anhdaidien='https://res.cloudinary.com/dfzvtpwsd/image/upload/v1670221889/3_gpownw.png')
        u3 = NguoiDung(ten='Du', taikhoan='user', matkhau=password, loainguoidung=UserRole.USER,
                       anhdaidien='https://res.cloudinary.com/dfzvtpwsd/image/upload/v1670221889/1_beeily.png')
        db.session.add_all([u1, u2, u3])
        db.session.commit()

        s1 = SanBay(ten='Buôn Mê Thuật')
        s2 = SanBay(ten='Hồ Chí Minh')
        s3 = SanBay(ten='Hà Nội')
        s4 = SanBay(ten='Vinh')
        s5 = SanBay(ten='Nha Trang')
        s6 = SanBay(ten='Vũng Tàu')
        s7 = SanBay(ten='Huế')
        s8 = SanBay(ten='Hải Phòng')
        s9 = SanBay(ten='Cần Thơ')
        s10 = SanBay(ten='Đà Nẵng')
        db.session.add_all([s1, s2, s3, s4, s5, s6, s7, s8, s9, s10])
        db.session.commit()

        t1 = TuyenBay(ten="Tuyến 1", sanbaydi_ma=1, sanbayden_ma=2)
        t2 = TuyenBay(ten="Tuyến 2", sanbaydi_ma=2, sanbayden_ma=3)
        t3 = TuyenBay(ten="Tuyến 3", sanbaydi_ma=3, sanbayden_ma=4)
        t4 = TuyenBay(ten="Tuyến 4", sanbaydi_ma=4, sanbayden_ma=5)
        t5 = TuyenBay(ten="Tuyến 5", sanbaydi_ma=5, sanbayden_ma=6)
        db.session.add_all([t1, t2, t3, t4, t5])
        db.session.commit()

        c1 = ChuyenBay(giodi=datetime.strptime('12/19/22 13:55:00', '%m/%d/%y %H:%M:%S'), thoigianbay=30,
                       hangmaybay_ma=1, tuyenbay_ma=1)
        c2 = ChuyenBay(giodi=datetime.strptime('12/20/22 7:00:00', '%m/%d/%y %H:%M:%S'), thoigianbay=180,
                       hangmaybay_ma=2, tuyenbay_ma=2)
        c3 = ChuyenBay(giodi=datetime.strptime('12/20/22 9:35:00', '%m/%d/%y %H:%M:%S'), thoigianbay=70,
                       hangmaybay_ma=3, tuyenbay_ma=3)
        c4 = ChuyenBay(giodi=datetime.strptime('12/29/22 6:55:00', '%m/%d/%y %H:%M:%S'), thoigianbay=90,
                       hangmaybay_ma=4, tuyenbay_ma=4)
        c5 = ChuyenBay(giodi=datetime.strptime('12/25/22 19:55:00', '%m/%d/%y %H:%M:%S'), thoigianbay=120,
                       hangmaybay_ma=5, tuyenbay_ma=5)
        c6 = ChuyenBay(giodi=datetime.strptime('1/19/23 13:55:00', '%m/%d/%y %H:%M:%S'), thoigianbay=90,
                       hangmaybay_ma=3, tuyenbay_ma=1)
        c7 = ChuyenBay(giodi=datetime.strptime('12/20/22 7:00:00', '%m/%d/%y %H:%M:%S'), thoigianbay=180,
                       hangmaybay_ma=5, tuyenbay_ma=2)
        c8 = ChuyenBay(giodi=datetime.strptime('12/20/22 9:35:00', '%m/%d/%y %H:%M:%S'), thoigianbay=70,
                       hangmaybay_ma=1, tuyenbay_ma=1)
        c9 = ChuyenBay(giodi=datetime.strptime('12/29/22 6:55:00', '%m/%d/%y %H:%M:%S'), thoigianbay=90,
                       hangmaybay_ma=4, tuyenbay_ma=4)
        c10 = ChuyenBay(giodi=datetime.strptime('12/25/22 19:55:00', '%m/%d/%y %H:%M:%S'), thoigianbay=120,
                        hangmaybay_ma=2, tuyenbay_ma=3)
        db.session.add_all([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10])
        db.session.commit()

        sd1 = SanBayDung(sanbay_ma=3, thoigiandung=22, chuyenbay_ma=1)
        sd2 = SanBayDung(sanbay_ma=1, thoigiandung=22, chuyenbay_ma=2)
        sd3 = SanBayDung(sanbay_ma=7, thoigiandung=26, chuyenbay_ma=2)
        sd4 = SanBayDung(sanbay_ma=9, thoigiandung=20, chuyenbay_ma=3)
        sd5 = SanBayDung(sanbay_ma=8, thoigiandung=30, chuyenbay_ma=4)
        db.session.add_all([sd1, sd2, sd3, sd4, sd5])
        db.session.commit()

        b1 = BangDonGia(hangve_ma=1, chuyenbay_ma=1, gia=1000000, soghe=20)
        b2 = BangDonGia(hangve_ma=2, chuyenbay_ma=1, gia=900000, soghe=15)
        b3 = BangDonGia(hangve_ma=1, chuyenbay_ma=2, gia=800000, soghe=50)
        b4 = BangDonGia(hangve_ma=1, chuyenbay_ma=3, gia=1300000, soghe=30)
        b5 = BangDonGia(hangve_ma=2, chuyenbay_ma=3, gia=1000000, soghe=20)
        b6 = BangDonGia(hangve_ma=1, chuyenbay_ma=4, gia=1000000, soghe=35)
        b7 = BangDonGia(hangve_ma=2, chuyenbay_ma=4, gia=1500000, soghe=10)
        b8 = BangDonGia(hangve_ma=1, chuyenbay_ma=5, gia=1000000, soghe=40)
        b9 = BangDonGia(hangve_ma=1, chuyenbay_ma=6, gia=1300000, soghe=30)
        b10 = BangDonGia(hangve_ma=2, chuyenbay_ma=7, gia=1000000, soghe=20)
        b11 = BangDonGia(hangve_ma=1, chuyenbay_ma=8, gia=1000000, soghe=35)
        b12 = BangDonGia(hangve_ma=2, chuyenbay_ma=9, gia=7500000, soghe=10)
        b13 = BangDonGia(hangve_ma=1, chuyenbay_ma=10, gia=1000000, soghe=40)
        db.session.add_all([b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13])
        db.session.commit()
