from typing import OrderedDict
import requests
import argparse

from rich.console import Console, RenderGroup
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.padding import Padding


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


def messages(cli_args):
    r = requests.get(
        "https://passio3.com/www/goServices.php?getAlertMessages=1&json=%7B%22systemSelected0%22%3A%2276%22%2C%22amount%22%3A1%2C%22routesAmount%22%3A0%7D")
    messages_data = r.json()
    messages_data = messages_data["msgs"]

    messages_data_new = [{"title": m["name"], "html": m["html"],
                          "date_from":m["from"], "date_to":m["to"]} for m in messages_data]

    console = Console()
    console.print(Panel(Text("Messages", justify="center", style="bold")))
    for m in messages_data_new:
        group = RenderGroup(
            Text(m["title"], justify="center", style="bold"),
            Text(m["date_from"] + " to " + m["date_to"], justify="center"),
            Padding(Text(m["html"]), (1,0,0,0))
            )
        console.print(Panel(group, expand=True))

    

def buses(cli_args):
    r = requests.get(
        "https://passio3.com/www/mapGetData.php?getBuses=1&json=%7B%22s0%22%3A%2276%22%2C%22sA%22%3A1%7D")
    buses_data = r.json()
    buses_data = list(buses_data["buses"].values())
    buses_data = [b[0] for b in buses_data]
    pp(buses_data)

    def map_bus_data(bus):
        new_bus = OrderedDict()
        new_bus["bus_name"] = bus["bus"]
        new_bus["bus_id"] = str(bus["busId"])
        new_bus["latitude"] = str(bus["latitude"])
        new_bus["longitude"] = str(bus["longitude"])
        
        new_bus["route"] = bus["route"]
        new_bus["route_id"] = bus["routeId"]
        return new_bus
    buses_data_new = list(map(map_bus_data, buses_data))
    buses_data_new.sort(key=lambda x: (x["route"], x["bus_name"]))

    table = Table(title="Buses", show_header=True)
    for key in buses_data_new[0]:
        table.add_column(key)
    for bus in buses_data_new:
        table.add_row(*bus.values())

    console = Console()
    console.print(table)

def eta(cli_args):
    ...

def app(cli_args):
    if cli_args["cmd_name"] == "routes":
        routes(cli_args)
    elif cli_args["cmd_name"] == "stops":
        stops(cli_args)
    elif cli_args["cmd_name"] == "messages":
        messages(cli_args)
    elif cli_args["cmd_name"] == "buses":
        buses(cli_args)
    elif cli_args["cmd_name"] == "eta":
        eta(cli_args)
    else:
        print("No command selected")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='gtb',
                                     description='A CLI app for real-time Georgia Tech bus infomation')
    subparsers = parser.add_subparsers(help='Commands', dest='cmd_name')

    parser_routes = subparsers.add_parser('routes', help='...')

    parser_stops = subparsers.add_parser('stops', help='...')
    parser_buses = subparsers.add_parser('buses', help='...')
    parser_eta = subparsers.add_parser('eta', help='...')

    parser_messages = subparsers.add_parser('messages', help='...')

    args = parser.parse_args()
    app(vars(args))
