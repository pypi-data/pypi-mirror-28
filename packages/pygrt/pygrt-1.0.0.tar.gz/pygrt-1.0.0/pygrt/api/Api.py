from requests import request
from time import time
import math

class Api(object):
	def __init__(self):
		return

	def request(self, endpoint, method='GET', *args, **kwargs):
		url = 'http://realtimemap.grt.ca/{endpoint}'.format(endpoint=endpoint)

		params = {k: v for k, v in kwargs.items() if v is not None}
		params['unique'] = math.floor(time())
		headers = {'Referer': 'http://realtimemap.grt.ca/'}

		response = request(method, url, params=params, headers=headers)

		return response.json()