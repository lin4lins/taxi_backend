from flask import Response
from flask_restful import Resource, fields, marshal_with, reqparse, request

from backend.models import Car, Driver

order_fields = {'id': fields.Integer}
car_fields = {'id': fields.Integer, 'license_plate': fields.String, 'model': fields.String, 'color': fields.String}
driver_fields = {'id': fields.Integer, 'name': fields.String, 'phone_number': fields.String,
                 'car': fields.Nested(car_fields), 'orders': fields.Nested(order_fields)}


class DriverResource(Resource):
    @marshal_with(driver_fields)
    def get(self, id):
        return Driver.get_by_id(id)

    def delete(self, id):
        Driver.delete(id=id)
        return Response(status=204)


class DriversResource(Resource):
    @marshal_with(driver_fields)
    def get(self):
        return Driver.get_all()

    def post(self):
        driver = Driver.create(name=request.json['name'], phone_number=request.json['phone_number'])
        Car.create(driver_id=driver.id, license_plate=request.json['license_plate'],
                   model=request.json['model'], color=request.json['color'])
        return Response(status=201)


class DriversStatistics(Resource):
    @staticmethod
    def __get_arguments():
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('type', type=str, choices=['top'], required=True, location='args')
        return parser.parse_args()

    @marshal_with(driver_fields)
    def get(self):
        args = self.__get_arguments()
        choices = {'top': Driver.get_top_by_completed_orders}
        return choices.get(args.get("type"))()
