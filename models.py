from backend.main import db
from backend.mixins import RepositoryMixin


class Order(db.Model, RepositoryMixin):
    __tablename__ = 'order_'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    point_a_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    point_a = db.relationship('Address', uselist=False, foreign_keys='Order.point_a_id')

    point_b_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    point_b = db.relationship('Address', uselist=False, foreign_keys='Order.point_b_id')

    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    rider_id = db.Column(db.Integer, db.ForeignKey('rider.id'))
    status = db.Column(db.Boolean, nullable=False, default=False)
    amount = db.Column(db.Integer, nullable=False)

    @classmethod
    def get_orders_count(cls):
        return cls.query.filter_by().count()

    @classmethod
    def get_percent_of_success(cls):
        successful_orders = cls.query.filter_by(status=True).count()
        unsuccessful_orders = cls.query.filter_by(status=False).count()
        return round(successful_orders / (successful_orders + unsuccessful_orders) * 100, 2)

    @classmethod
    def get_top_10_by_amount(cls):
        return cls.query.order_by(cls.amount.desc()).limit(10).all()

    @classmethod
    def get_most_recent(cls):
        return cls.query.order_by(cls.created_at.desc()).first()

    @classmethod
    def get_earned_amount(cls):
        return db.session.query(db.func.sum(cls.amount)).filter_by(status=True).scalar()

    @classmethod
    def get_all(cls):
        return cls.query.join(Rider, Driver).all()

    @classmethod
    def get_by_driver_id(cls, driver_id: int):
        return cls.query.filter_by(driver_id=driver_id).all()

    @classmethod
    def get_by_rider_id(cls, rider_id: int):
        return cls.query.filter_by(rider_id=rider_id).all()


class Rider(db.Model, RepositoryMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(120), unique=True, nullable=False)
    orders = db.relationship('Order', backref='rider', cascade="all,delete")

    @classmethod
    def get_top_by_completed_orders(cls):
        return db.session.query(cls). \
            join(Order). \
            group_by(cls.id).order_by(db.func.count(cls.orders).label('order_total').desc()). \
            filter(Order.status == True). \
            first()


class Driver(db.Model, RepositoryMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.String(120), unique=True, nullable=False)
    car = db.relationship('Car', backref='driver', uselist=False, cascade="all,delete")
    orders = db.relationship('Order', backref='driver', cascade="all,delete")

    @classmethod
    def get_top_by_completed_orders(cls):
        return db.session.query(cls). \
            join(Order). \
            group_by(cls.id).order_by(db.func.count(cls.orders).label('order_total').desc()). \
            filter(Order.status == True). \
            first()


class Car(db.Model, RepositoryMixin):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    license_plate = db.Column(db.String(8), unique=True, nullable=False)
    model = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), nullable=False)


class Address(db.Model, RepositoryMixin):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(50), nullable=False)
    building = db.Column(db.Integer(), nullable=False)
