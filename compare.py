"""Command line tool for comparing both routing profiles.
Make sure that the routing engines are running.
"""

import argparse
import json
import requests
from geojson import Point, Feature, FeatureCollection, loads, dumps
import geojsonio


PARSER = argparse.ArgumentParser(description='Command line tool for comparing both routing engines.'
                                 + ' For using this tool you have to make sure that '
                                 + 'the routing engines are running!')
PARSER.add_argument('coordinates',
                    type=float,
                    nargs='*',
                    default=[9.196618, 48.767587,
                             9.173770, 48.762977,
                             9.162890, 48.768612,
                             9.160714, 48.778650,
                             9.166465, 48.782849,
                             9.169263, 48.790632,
                             9.194753, 48.798413,
                             9.218279, 48.805652,
                             9.204883, 48.783791,
                             9.167740, 48.778174,
                             9.185525, 48.777780,
                             9.191544, 48.782462,
                             9.173416, 48.774817,
                             9.159495, 48.790154,
                             9.170066, 48.785639,
                             9.150796, 48.783735,
                             9.151582, 48.790848],
                    help='A sequence of coordinates for which the optimal route '
                    + 'shall be found alternating between longitude and latitude.'
                    + ' Consequently the list must contain an even number of values.')
PARSER.add_argument('--host',
                    type=str,
                    default='localhost',
                    help='Port for the routing engine with car profile')
PARSER.add_argument('--port_car',
                    type=int,
                    default=5000,
                    help='Port for the routing engine with car profile')
PARSER.add_argument('--port_electric',
                    type=int,
                    default=6000,
                    help='Port for the routing engine with electric car profile')
PARSER.add_argument('--simplified',
                    type=bool,
                    default=False,
                    help='If set to true the path will be simplified')
PARSER.add_argument('--trip',
                    type=bool,
                    default=True,
                    help='If set to true the TSP problem will be solved '
                    + 'otherwise just the shortest path will be returned')

COLOR_CAR = "#ebae10"
PROPERTIES_CAR = {"stroke": COLOR_CAR, "stroke-width": 6, "stroke-opacity": 1}
COLOR_ELECTRIC = "#0d17eb"
PROPERTIES_ELECTRIC = {"stroke": COLOR_ELECTRIC, "stroke-width": 2, "stroke-opacity": 1}


def main():
    """The main method of the comparison command line tool.
    It will parse the arguments and send the requests.
    Lastly, the results will be displayed on the standard out and in the browser.
    """

    # Parse arguments
    args = PARSER.parse_args()

    # Query best route for the car profile
    action = 'trip' if args.trip else 'route'
    req_car = _build_request(args.host,
                             str(args.port_car),
                             args.trip,
                             args.coordinates,
                             args.simplified)
    response_car = requests.get(req_car).json()
    print("Result for car profile: " + str(response_car) + '\n')
    geom = loads(json.dumps(response_car[action + 's'][0]['geometry']))
    feature_car = Feature(geometry=geom, properties=PROPERTIES_CAR)
    waypoints_car = [Feature(geometry=Point(v['location']),
                             properties={
                                 "marker-color": COLOR_CAR,
                                 "marker-size": "large",
                                 "marker-symbol": v['waypoint_index'] + 1
                                 }
                            ) for v in response_car['waypoints']]

    # Query best route for the electric car profile
    req_electric = _build_request(args.host,
                                  str(args.port_electric),
                                  args.trip,
                                  args.coordinates,
                                  args.simplified)
    response_electric = requests.get(req_electric).json()
    print("Result for electric car profile: " + str(response_electric) + '\n')
    geom = loads(json.dumps(response_electric[action + 's'][0]['geometry']))
    feature_electric = Feature(geometry=geom, properties=PROPERTIES_ELECTRIC)
    waypoints_electric = [Feature(geometry=Point(v['location']),
                                  properties={
                                      "marker-color": COLOR_ELECTRIC,
                                      "marker-size": "small",
                                      "marker-symbol": v['waypoint_index'] + 1
                                      }
                                 ) for v in response_electric['waypoints']]

    # Show output in browser
    feature_collection = FeatureCollection([feature_car, feature_electric]
                                           + waypoints_car
                                           + waypoints_electric)
    geojsonio.display(dumps(feature_collection))

    print("------------ Comparison of routing profiles ------------")
    print("Power Consumption Car profile:\t\t\t"
          + str("%.2f" % (response_car[action + 's'][0]['distance'] / 1000)) + " kw")
    print("Power Consumption Electric Car profile:\t\t"
          + str("%.2f" % (response_electric[action + 's'][0]['distance'] / 1000)) + " kw")
    print("--------------------------------------------------------")

def _build_request(host: str, port: str, action: bool, coordinates: list, simplified: bool) -> str:
    """Builds the request string for the routing engine.

    Args:
        host (str): host name/ip.
        port (str): open port of the routing engine.
        action (bool): if true the TSP problem will be solved,
            else the shortest route will be returned.
        coordinates (list): list of lat, lon coordinates.
        simplified (bool): if true the engine will return a simplified list of coordinates,
            else all coordinates will be returned.

    Returns:
        str: the request string.
    """
    coords = ';'.join(
        [str(lon) + ',' + str(lat) for lon, lat in zip(coordinates[0::2], coordinates[1::2])]
    )
    req = 'http://' \
        + host \
        + ':' \
        + port \
        + '/' + ('trip' if action else 'route') + '/v1/driving/' \
        + coords \
        + '?overview=' \
        + ('simplified' if simplified else 'full') \
        + '&geometries=geojson'
    print('Request build: ' + req + '\n')
    return req

if __name__ == "__main__":
    main()
