from gmaps import Geocoding, Elevation, Directions

# api = Geocoding()
api = Directions()
directions =  api.directions((51.9028, 4.4975),(51.9235, 4.4701))
print 'Distance: ' + str(directions[0]['legs'][0]['distance']['value']) + ' meters'
print 'Time: ' + str(directions[0]['legs'][0]['duration']['value']) + ' seconds'

for step in directions[0]['legs'][0]['steps']:
    start = (step['start_location']['lat'], step['start_location']['lng'])
    end = (step['end_location']['lat'], step['end_location']['lng'])
    print start, end
# print 'distance: ' + directions['Directions']['Distance']['meters']
# api.geocode("somwhere")
# api.Elevation(51.123, 21.123)

