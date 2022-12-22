from flask_restful import Resource, marshal_with, fields

from backend.models import Address

address_fields = {"id": fields.Integer, "city": fields.String, "street": fields.String, "building": fields.Integer}


class AddressResource(Resource):
    @marshal_with(address_fields)
    def get(self):
        return Address.get_all()
