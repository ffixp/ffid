import flask
from webapputils import Webapp
import requests
import json
import ipaddress

# Set up an app
app = Webapp(__name__, static_directory="static", google_tracking_code=None)

# Load the peer file
peers = json.load(open("peers.json", "r"))


@app.errorhandler(404)
def page_not_found(e):
    return "Error 404", 404


@app.route('/')
def index():
    """A little landing page in case anyone ever looks at this service for some reason"""
    return "<h1>FFIXP FFID Registry</h1><p>This service exists to keep network peers informed about eachother's routes</p>"


@app.route('/id/<string:id>')
def by_id(id):
    """Allow users to query by FFID (3-byte hex value)"""
    print("Processing query for network with ID: {}".format(id))
    id = id.upper()
    for peer in peers:
        if peer["ffid"] == id:
            return peer
    return "Error 404", 404


@app.route('/network/<string:name>')
def by_network(name):
    """Allow users to query by network name (case-insensitive)"""
    print("Processing query for network with name: {}".format(name))
    name = name.lower()
    for peer in peers:
        if peer["network"].lower() == name:
            return peer
    return "Error 404", 404


@app.route('/whois/<string:ip>')
def whois_short(ip):
    """Allow users to make a whois-style lookup using just a single IP (/32 mask)"""
    return whois(ip, "32")


@app.route('/whois/<string:ip>/<string:mask>')
def whois(ip, mask):
    """Allow users to make a whois-style lookup using a CIDR IP range"""
    print("Processing query for whois of {}/{}".format(ip, mask))
    try:
        ip = ipaddress.ip_network(f"{ip}/{mask}")
    except ValueError:
        return "Malformed Address", 400

    for peer in peers:
        for network in peer["prefixes"]:
            network = ipaddress.ip_network(network)
            if network.version == ip.version:
                print(ip, network)
                if ip.subnet_of(network):
                    return peer
    return "Error 404", 404


@app.route('/routes')
def routes():
    """Allow peers to get a simple list of all routes in FFIXP"""
    print("Processing query for all routes")
    response = flask.make_response(
        '\n'.join(
            ['\n'.join(
                [
                    f"{peer['ffid']} {route}"
                    for route in peer["prefixes"]
                ]
            )
                for peer in peers
            ]
        ), 200)
    response.headers['Content-Type'] = 'text/plain'
    return response


if __name__ == "__main__":
    app.run(debug=True)
