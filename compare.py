"""Command line tool for comparing both routing profiles. Make sure that the routing engines are running.
"""

import geojsonio
import requests
import argparse
import sys
import geojson
import json
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

PARSER = argparse.ArgumentParser(description='Command line tool for comparing both routing engines.'
                                 + ' For using this tool you have to make sure that'
                                 + 'the routing engines are running!')
PARSER.add_argument('coordinates',
                    type=float,
                    nargs='*',
                    default=[9.158303, 48.783595,
                             9.010439, 48.794466,
                             9.165981, 48.894487,
                             9.224422, 48.897935],
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
                    help='If set to true the TSP problem will be solved'
                    + 'otherwise just the shortest path will be returned')

def main():
    args = PARSER.parse_args()
    print(args.coordinates[0::2])
    print(args.coordinates[1::2])

    action = 'trip' if args.trip else 'route'
    req_car = build_request(args.host,
                            str(args.port_car),
                            '/' + action + '/v1/driving/',
                            args.coordinates,
                            args.simplified)
    # response_car = requests.get(req_car).json()
    response_car = {'code': 'Ok', 'trips': [{'geometry': {'coordinates': [[13.409687, 52.521288], [13.4103, 52.521748], [13.409487, 52.5223], [13.412376, 52.524069], [13.417176, 52.528456], [13.421289, 52.528729], [13.423868, 52.528136], [13.44293, 52.544468], [13.448029, 52.546909], [13.446736, 52.547706], [13.449663, 52.551086], [13.454227, 52.549438],[13.454402, 52.54912], [13.450851, 52.548364], [13.444648, 52.545618], [13.426534, 52.552575], [13.414877, 52.553858], [13.397147, 52.554806], [13.384244, 52.556031], [13.381906, 52.552755], [13.381248, 52.55227], [13.387901, 52.548603], [13.396877, 52.537153], [13.398978, 52.532449], [13.403381, 52.526988], [13.403658, 52.525687], [13.402291, 52.523694], [13.403695, 52.523084], [13.404517, 52.52196], [13.402863, 52.521371], [13.404811, 52.519918], [13.409487, 52.5223], [13.4103, 52.521748], [13.409687, 52.521288]], 'type': 'LineString'}, 'legs': [{'steps': [], 'distance': 5071.9, 'duration': 569.9, 'summary': '', 'weight': 569.9}, {'steps': [], 'distance': 5561.2, 'duration': 566, 'summary': '', 'weight': 566}, {'steps': [], 'distance': 4858.6, 'duration': 582.7, 'summary': '', 'weight': 582.7}], 'distance': 15491.7, 'duration': 1718.6, 'weight_name': 'routability', 'weight': 1718.6}], 'waypoints': [{'waypoint_index': 0, 'location': [13.409687, 52.521288], 'name': 'Panoramastraße', 'hint': 'SbECgKKxAoAAAAAAMwAAAAAAAAAAAAAAAAAAADMAAAAAAAAAAAAAANEAAACXncwASGkhAzudzAAxZSEDAACPAu4js_M=', 'trips_index': 0}, {'waypoint_index': 1, 'location': [13.454227, 52.549438], 'name': 'Parkstraße', 'hint': 'quYCgLLmAoBBAAAAOQAAAAAAAAAAAAAAQQAAADkAAAAAAAAAAAAAANEAAACTS80APtchA5dKzQAL1yEDAAAfCu4js_M=', 'trips_index': 0}, {'waypoint_index': 2, 'location': [13.381906, 52.552755], 'name': 'Prinzenallee', 'hint': 'wEwAgP___38IAAAAHQAAACIAAABWAAAACAAAAB0AAAAiAAAAVgAAANEAAAASMcwAM-QhA6wwzABa5CEDAQBPDe4js_M=', 'trips_index': 0}]}
    logging.info("Result for car profile: " + str(response_car))
    geom = geojson.loads(json.dumps(response_car[action + 's'][0]['geometry']))
    feature_car = geojson.Feature(geometry=geom)

    req_electric = build_request(args.host,
                                 str(args.port_electric),
                                 '/' + action + '/v1/driving/',
                                 args.coordinates,
                                 args.simplified)
    # response_electric = requests.get(req_electric).json()
    response_electric = {'code': 'Ok', 'trips': [{'geometry': {'coordinates': [[13.409687, 52.521288], [13.4103, 52.521748], [13.409487, 52.5223], [13.412376, 52.524069], [13.417176, 52.528456], [13.421289, 52.528729], [13.423868, 52.528136], [13.44293, 52.544468], [13.448029, 52.546909], [13.446736, 52.547706], [13.449663, 52.551086], [13.454227, 52.549438], [13.454402, 52.54912], [13.450851, 52.548364], [13.444648, 52.545618], [13.426534, 52.552575], [13.414877, 52.553858], [13.397147, 52.554806], [13.384244, 52.556031], [13.381906, 52.552755], [13.381248, 52.55227], [13.387901, 52.548603], [13.396877, 52.537153], [13.398978, 52.532449], [13.403381, 52.526988], [13.403658, 52.525687], [13.402291, 52.523694], [13.403695, 52.523084], [13.404517, 52.52196], [13.402863, 52.521371], [13.404811, 52.519918], [13.409487, 52.5223], [13.4103, 52.521748], [13.409687, 52.521288]], 'type': 'LineString'}, 'legs': [{'steps': [], 'distance': 5071.9, 'duration': 578.8, 'summary': '', 'weight': 578.8}, {'steps': [], 'distance': 5561.2, 'duration': 569.9, 'summary': '', 'weight': 569.9}, {'steps': [], 'distance': 4858.6, 'duration': 585.8, 'summary': '', 'weight': 585.8}], 'distance': 15491.7, 'duration': 1734.5, 'weight_name': 'duration', 'weight': 1734.5}], 'waypoints': [{'waypoint_index': 0, 'location': [13.409687, 52.521288], 'name': 'Panoramastraße', 'hint': 'ua8CgBKwAoAAAAAAMwAAAAAAAAAAAAAAAAAAADMAAAAAAAAAAAAAANEAAACXncwASGkhAzudzAAxZSEDAACPAqxs7Q8=', 'trips_index': 0}, {'waypoint_index': 1, 'location': [13.454227, 52.549438], 'name': 'Parkstraße', 'hint': 'O-oCgEPqAoBBAAAAOQAAAAAAAAAAAAAAQQAAADkAAAAAAAAAAAAAANEAAACTS80APtchA5dKzQAL1yEDAAAfCqxs7Q8=', 'trips_index': 0}, {'waypoint_index': 2, 'location': [13.381906, 52.552755], 'name': 'Prinzenallee', 'hint': 's00AgP___38IAAAAHQAAACIAAABWAAAACAAAAB0AAAAiAAAAVgAAANEAAAASMcwAM-QhA6wwzABa5CEDAQBPDaxs7Q8=', 'trips_index': 0}]}
    logging.info("Result for electric car profile: " + str(response_electric))
    geom = geojson.loads(json.dumps(response_electric[action + 's'][0]['geometry']))
    feature_electric = geojson.Feature(geometry=geom)

    feature_collection = geojson.FeatureCollection([feature_car, feature_electric])
    geojsonio.display(geojson.dumps(feature_collection))

def build_request(host: str, port: str, path: str, coordinates: list, simplified: bool) -> str:
    coords = ';'.join(
        [str(lon) + ',' + str(lat) for lon, lat in zip(coordinates[0::2], coordinates[1::2])]
    )
    req = 'http://' \
        + host \
        + ':' \
        + port \
        + path \
        + coords \
        + '?overview=' \
        + ('simplified' if simplified else 'full') \
        + '&geometries=geojson'
    logging.info('Request build: ' + req)
    return req

if __name__ == "__main__":
    main()
