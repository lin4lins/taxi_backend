from random import choice, randint, sample

from faker import Faker
from faker_vehicle import VehicleProvider

from main import app, db
from models import Address, Car, Driver, Order, Rider

RIDERS_COUNT = 284
DRIVERS_COUNT = 21
ADDRESS_COUNT = 300
ORDERS_COUNT = 1024
BUILDINGS_ON_STREET_COUNT = 10

faker = Faker(['pl_PL'])
faker.add_provider(VehicleProvider)


def fill_db():
    db.drop_all()
    db.create_all()
    create_riders()
    create_drivers()
    create_cars()
    create_address()
    create_orders()


def create_riders():
    for _ in range(RIDERS_COUNT):
        Rider.create(name=faker.name(), phone_number=faker.phone_number())


def create_drivers():
    for _ in range(DRIVERS_COUNT):
        Driver.create(name=faker.name(), phone_number=faker.phone_number())


def create_cars():
    drivers = Driver.query.all()
    for driver in drivers:
        Car.create(driver_id=driver.id,
                   license_plate=faker.license_plate(),
                   model=faker.vehicle_make_model(),
                   color=faker.safe_color_name())


def create_address():
    for _ in range(ADDRESS_COUNT):
        Address.create(city=faker.city(),
                       street=faker.street_name(),
                       building=randint(1, BUILDINGS_ON_STREET_COUNT))


def create_orders():
    drivers = Driver.query.all()
    riders = Rider.query.all()
    address = Address.query.all()
    for _ in range(ORDERS_COUNT):
        point_a, point_b = sample(address, 2)
        driver, rider = choice(drivers), choice(riders)
        Order.create(created_at=faker.date_time(),
                     point_a_id=point_a.id,
                     point_b_id=point_b.id,
                     driver_id=driver.id,
                     rider_id=rider.id,
                     status=faker.boolean(),
                     amount=randint(50, 500))


if __name__ == '__main__':
    with app.app_context():
        fill_db()
