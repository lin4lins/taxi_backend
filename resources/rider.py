from flask import Response
from flask_restful import Resource, fields, marshal_with, reqparse, request

from backend.models import Rider

order_fields = {'id': fields.Integer}
rider_fields = {'id': fields.Integer, 'name': fields.String, 'phone_number': fields.String,
                'orders': fields.Nested(order_fields)}


class RiderResource(Resource):
    @marshal_with(rider_fields)
    def get(self, id):
        return Rider.get_by_id(id)

    def delete(self, id):
        Rider.delete(id=id)
        return Response(status=204)


class RidersResource(Resource):
    @marshal_with(rider_fields)
    def get(self):
        return Rider.get_all()

    def post(self):
        Rider.create(name=request.json['name'], phone_number=request.json['phone_number'])
        return Response(status=201)


class RidersStatistics(Resource):
    @staticmethod
    def __get_arguments():
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('type', type=str, choices=['top'], required=True, location='args')
        return parser.parse_args()

    @marshal_with(rider_fields)
    def get(self):
        args = self.__get_arguments()
        choices = {'top': Rider.get_top_by_completed_orders}
        return choices.get(args.get("type"))()

