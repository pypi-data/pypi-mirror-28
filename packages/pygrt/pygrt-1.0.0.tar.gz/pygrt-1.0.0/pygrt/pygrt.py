from .api import Api, Bus, Route

class GRT(object):
	def __init__(self):
		self._api = Api()
		self._bus = Bus()
		self._route = Route()

	@property
	def api(self):
		return self._api

	@property
	def bus(self):
		return self._bus

	@property
	def route(self):
		return self._route