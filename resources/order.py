from flask import Response
from flask_restful import (Resource, fields, marshal, marshal_with, reqparse,
                           request, abort)

from backend.models import Order

address_fields = {"id": fields.Integer, "city": fields.String, "street": fields.String, "building": fields.Integer}
order_fields = {'id': fields.Integer, 'created_at': fields.DateTime,
                'point_a': fields.Nested(address_fields), 'point_b': fields.Nested(address_fields),
                'driver_id': fields.Integer, 'rider_id': fields.Integer,
                'status': fields.Boolean, 'amount': fields.Integer}


class OrderResource(Resource):
    @marshal_with(order_fields)
    def get(self, id):
        return Order.get_by_id(id)

    def delete(self, id):
        Order.delete(id=id)

        return Response(status=204)


class OrdersResource(Resource):
    @marshal_with(order_fields)
    def get(self):
        return Order.get_all()

    def post(self):
        Order.create(point_a_id=request.json['point_a_id'], point_b_id=request.json['point_b_id'],
                     driver_id=request.json['driver_id'], rider_id=request.json['rider_id'],
                     status=request.json['status'], amount=request.json['amount'])
        return Response(status=201)


class OrdersStatistics(Resource):
    @staticmethod
    def __get_arguments():
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('type', type=str, required=True, location='args',
                            choices=['orders_count', 'percent_of_success', 'top_10_by_amount', 'most_recent',
                                     'earned_amount'])
        return parser.parse_args()

    def get(self):
        args = self.__get_arguments()
        int_choices = {'orders_count': Order.get_orders_count, 'percent_of_success': Order.get_percent_of_success,
                       'earned_amount': Order.get_earned_amount}
        order_choices = {'top_10_by_amount': Order.get_top_10_by_amount, 'most_recent': Order.get_most_recent}
        if int_choices.get(args.get("type")):
            return int_choices.get(args.get("type"))()
        else:
            return marshal(order_choices.get(args.get("type"))(), order_fields)


class OrdersSearch(Resource):
    @staticmethod
    def __get_arguments():
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('driver_id', type=int, required=False, location='args')
        parser.add_argument('rider_id', type=int, required=False, location='args')
        return parser.parse_args()

    @marshal_with(order_fields)
    def get(self):
        args = self.__get_arguments()
        driver_id, rider_id = args.get("driver_id"), args.get("rider_id")
        if driver_id and rider_id or not driver_id and not rider_id:
            return abort(404)

        return Order.get_by_driver_id(driver_id) if driver_id else Order.get_by_rider_id(rider_id)

