import json
import requests
from flask import Flask

# API endpoint URL's and access keys
WMATA_API_KEY = "598dbacee36b4054aa40e6b72ee29b3e"
INCIDENTS_URL = "https://jhu-intropython-mod10.replit.app/"
headers = {"api_key": WMATA_API_KEY, 'Accept': '*/*'}

################################################################################

app = Flask(__name__)

# get incidents by machine type (elevators/escalators)
# field is called "unit_type" in WMATA API response
@app.route("/incidents/<unit_type>", methods=["GET"])
def get_incidents(unit_type):
    # create an empty list called 'incidents'
    incidents = []

    # use 'requests' to do a GET request to the WMATA Incidents API
    # retrieve the JSON from the response
    response = requests.get(INCIDENTS_URL, headers=headers)
    response_json = response.json()

    # iterate through the JSON response and retrieve all incidents matching 'unit_type'
    # for each incident, create a dictionary containing the 4 fields from the Module 7 API definition
    #   -StationCode, StationName, UnitType, UnitName
    # add each incident dictionary object to the 'incidents' list
    incident_list = response_json["ElevatorIncidents"]

    for station in incident_list:
        unit_index = station["UnitType"]
        if unit_index.upper() == unit_type.upper():
            s_code = ("StationCode", station["StationCode"])
            s_name = ("StationName", station["StationName"])
            u_name = ("UnitName", station["UnitName"])
            u_type = ("UnitType", station["UnitType"])

            incidents.append(dict([s_code,s_name,u_name,u_type]))

    # return the list of incident dictionaries using json.dumps()
    return json.dumps(incidents)

if __name__ == '__main__':
    app.run(debug=True)
