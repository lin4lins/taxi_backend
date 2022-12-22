from flask_restful import Api

from main import app
from backend.resources.address import AddressResource
from backend.resources.driver import DriverResource, DriversResource, DriversStatistics
from backend.resources.order import OrderResource, OrdersResource, OrdersStatistics, OrdersSearch
from backend.resources.rider import RiderResource, RidersResource, RidersStatistics


api = Api(app)
api.add_resource(RidersResource, '/riders/')
api.add_resource(RidersStatistics, '/riders/statistics')
api.add_resource(RiderResource, '/riders/<int:id>')

api.add_resource(DriversResource, '/drivers/')
api.add_resource(DriversStatistics, '/drivers/statistics')
api.add_resource(DriverResource, '/drivers/<int:id>')

api.add_resource(OrdersResource, '/orders/')
api.add_resource(OrdersStatistics, '/orders/statistics')
api.add_resource(OrderResource, '/orders/<int:id>')
api.add_resource(OrdersSearch, '/orders/search')

api.add_resource(AddressResource, '/address/')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
