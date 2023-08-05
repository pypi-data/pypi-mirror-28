from .Api import Api

class Route(Api):
	def __init__(self):
		super().__init__()

	def stops(self, route_id, stop_id=False):
		if stop_id is False:
			return self.request('Stop/GetByRouteId', 'GET', routeId=route_id)
		else:
			return self.request('Stop/GetStopInfo', 'GET', routeId=route_id, stopId=stop_id)

	def shape(self, route_id):
		return self.request('Shape/GetByrouteId', 'GET', routeId=route_id)


# This is the jQuery function used to draw the polylines on the map
# $.get('/Shape/GetByrouteId', { routeId: routeId }, function (data) {
#     if (data) {
#         $.each(data, function (index, object) {
#             if ($(this.Shapes).length > 0) {
#                 var _coordinates = [];
#                 var _bounds = new google.maps.LatLngBounds();
#                 $.each(this.Shapes, function (i, e) {
#                     var _coordinate = new google.maps.LatLng(e.Latitude, e.Longitude);
#                     _coordinates.push(_coordinate);
#                     _bounds.extend(_coordinate);
#                 });
#                 var _shape = new google.maps.Polyline({
#                     path: _coordinates,
#                     strokeColor: color ? "#" + color : "#E94BA0",
#                     strokeOpacity: 0.5,
#                     strokeWeight: 5
#                 });
#                 _shape.setMap(map);
#                 map.fitBounds(_bounds);
#                 shapeList.push({ routeId: routeId, shape: _shape, bounds: _bounds });
#             }
#         });
#     }
# });

