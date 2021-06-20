from typing import OrderedDict
import requests
import argparse

from rich.console import Console
from rich.table import Table

from pprint import pprint as pp



def routes(cli_args):
    r = requests.get(
        "https://passio3.com/www/mapGetData.php?getRoutes=1&json=%7B%22systemSelected0%22%3A%2276%22%2C%22amount%22%3A1%7D")
    route_data = r.json()

    def map_route_data(route):
        new_route = OrderedDict()
        new_route["name"] = route["name"].strip()
        new_route["color"] = route["color"]
        new_route["id"] = route["id"]
        return new_route
    route_data_new = list(map(map_route_data, route_data))

    table = Table(title="Routes", show_header=True)
    for key in route_data_new[0]:
        table.add_column(key)
    for route in route_data_new:
        table.add_row(*route.values())

    console = Console()
    console.print(table)


def stops(cli_args):
    r = requests.get(
        "https://passio3.com/www/mapGetData.php?getStops=2&json=%7B%22s0%22%3A%2276%22%2C%22sA%22%3A1%7D")
    stop_data = r.json()
    stop_data = list(stop_data["stops"].values())
    
    def map_stop_data(stop):
        new_stop = OrderedDict()
        new_stop["name"] = stop["name"]
        new_stop["latitude"] = str(stop["latitude"])
        new_stop["longitude"] = str(stop["longitude"])
        new_stop["stopId"] = stop["stopId"]
        new_stop["id"] = stop["id"]
        new_stop["routeName"] = stop["routeName"]
        new_stop["routeId"] = stop["routeId"]
        new_stop["position"] = stop["position"]
        return new_stop
    stop_data_new = list(map(map_stop_data, stop_data))
    stop_data_new.sort(key=lambda x: (x["routeName"], int(x["position"])))

    table = Table(title="Stops", show_header=True)
    for key in stop_data_new[0]:
        table.add_column(key)
    for stop in stop_data_new:
        table.add_row(*stop.values())

    console = Console()
    console.print(table)    

def app(cli_args):
    if cli_args["cmd_name"] == "routes":
        routes(cli_args)
    elif cli_args["cmd_name"] == "stops":
        stops(cli_args)
    else:
        print("IDK YET")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='gtb',
                                     description='A CLI app for real-time Georgia Tech bus infomation')
    subparsers = parser.add_subparsers(help='Commands', dest='cmd_name')

    parser_routes = subparsers.add_parser('routes', help='...')

    parser_2 = subparsers.add_parser('stops', help='...')
    parser_3 = subparsers.add_parser('buses', help='...')

    args = parser.parse_args()
    app(vars(args))
