from .Api import Api
from time import time
import math

class Bus(Api):
	def __init__(self):
		super().__init__()

	def all(self):
		return self.request('Map/GetVehicles', 'GET')

	def info(self, vehicle_id, trip_id):
		return self.request('Stop/GetBusInfo', 'GET', vehicleId=vehicle_id, tripId=trip_id)

	def route(self, route_id):
		return self.request('Map/GetVehiclesByRouteId', 'GET', routeId=route_id)

