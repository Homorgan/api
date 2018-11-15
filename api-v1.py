import flask
from flask import request, jsonify
import os
import napalm

app = flask.Flask(__name__)
app.config['DEBUG'] = True

# Create some test data for our catalog in the form of a list of dictionaries.

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Testing for Napalm APIs</h1>
<p>A prototype API for Napalm fuctions.</p>'''


@app.route('/api/v1/resources/ping', methods=['GET'])
def api_all():

    if 'host' in request.args:
        hostname = request.args['host']
    else:
        return 'Error: No Hostname provided'
    #hostname = host #example
    response = os.system("ping -c 1 " + hostname)

    if response == 0:
        var = 'Host is up'
    else:
        var = 'Host is down'

    return var

@app.route('/api/v1/resources/napalm/get-facts', methods=['GET'])
def api_facts():

    if 'host' in request.args:
        hostname = request.args['host']
    else:
        return 'Error: No Hostname provided'

    results = []

    driver = napalm.get_network_driver('eos')

    device = driver(hostname=hostname, username='vagrant',
                    password='vagrant', optional_args={'port': 12443})

    device.open()

    results = device.get_facts()

    device.close()

    return jsonify(results)

@app.route('/api/v1/resources/napalm/get-config', methods=['GET'])
def api_config():

    if 'host' in request.args:
        hostname = request.args['host']
    else:
        return 'Error: No Hostname provided'

    results = []

    driver = napalm.get_network_driver('eos')

    device = driver(hostname=hostname, username='vagrant',
                    password='vagrant', optional_args={'port': 12443})

    device.open()

    results = device.get_config()

    device.close()

    return jsonify(results)

app.run()
