from PyQt4.QtCore import QVariant
import googlemaps

api_key = 'AIzaSyC-S6dnnYaiephplIQcDjILnkdZHELUD34'
# proxy = "185.108.219.123:8080"
# origin = (51.9028, 4.4975)
# destination = (51.9235, 4.4701)
mode = ['driving', 'walking', 'bicycling', 'transit']
departure_time = None
arrival_time = None
waypoints = []
addresses = iface.activeLayer()
destination = (50.901221, 4.400378)

def getTravelTime(origin, destination, mode, api_key, proxy=None):
    # Create API CLient with or without proxy
    if proxy:
        gmaps = googlemaps.Client(key=api_key, requests_kwargs={'proxies':"%s" % proxy})
    else:
        gmaps = googlemaps.Client(key=api_key)

    directions = gmaps.directions(origin, destination, mode=mode)

    distance = directions[0]['legs'][0]['distance']['value']
    travel_time = directions[0]['legs'][0]['duration']['value']

    return distance, travel_time


def getTravelSteps(origin, destination, mode, api_key, proxy=None):
    if proxy:
        gmaps = googlemaps.Client(key=api_key, requests_kwargs={'proxies':"%s" % proxy})
    else:
        gmaps = googlemaps.Client(key=api_key)

    directions = gmaps.directions(origin, destination, mode=mode)

    for step in directions[0]['legs'][0]['steps']:
        start = (step['start_location']['lat'], step['start_location']['lng'])
        end = (step['end_location']['lat'], step['end_location']['lng'])

    return start, end


def writeTravelTime(addresses, destination):
    # Create network layer
    vl = QgsVectorLayer("Point", "points with travel time", "memory")
    pr = vl.dataProvider()

    # Add id field
    vl.startEditing()
    pr.addAttributes([QgsField('id', QVariant.String), QgsField('address_id', QVariant.String), QgsField('travel_time', QVariant.Int)])
    vl.updateFields()

    # Add features
    for index, fet in enumerate(addresses.getFeatures()):
        geom = fet.geometry().asPoint()
        address_id = fet['Employee']
        origin = (geom.y(), geom.x())
        print origin
        distance, time = getTravelTime(origin, destination, 'driving', api_key)
        print time
        fet = QgsFeature(vl.pendingFields())
        fet.setAttribute('address_id', address_id)
        fet.setAttribute('travel_time', time)
        fet.setAttribute('id', index)
        fet.setGeometry(QgsGeometry.fromPoint(geom))
        pr.addFeatures([fet])

    # Save and add to the canvas
    vl.commitChanges()
    vl.updateExtents()
    QgsMapLayerRegistry.instance().addMapLayer(vl)


writeTravelTime(addresses, destination)

# print getTravelTime((50.9011, 4.400378), destination, 'driving', api_key)[1]/60   #

# Create network layer
# vl = QgsVectorLayer("Point", "points with travel time", "memory")
# pr = vl.dataProvider()
#
# # Add id field
# vl.startEditing()
# pr.addAttributes(
#     [QgsField('id', QVariant.String), ])
# vl.updateFields()
# fet = QgsFeature(vl.pendingFields())
# fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(4.400378, 50.901221)))
# pr.addFeatures([fet])
# vl.commitChanges()
# vl.updateExtents()
# QgsMapLayerRegistry.instance().addMapLayer(vl)