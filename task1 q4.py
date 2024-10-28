from argparse import ArgumentParser
import json
from requests import get                                                                  # pip3 install requests
from datetime import datetime

def datetime_to_unixtimestamp(date, time):
    datetime = date + ' ' + time
    datetime_obj = datetime.strptime(datetime, '%d/%m/%Y %H:%M:%S')
    timestamp = datetime_obj.timestamp()
    return timestamp
 
satellite = ArgumentParser(
    prog='python3 satellite.py',
    description="A command for getting location, in latitude and longitude or country code and zone, at real-time or "
                "a specific time",
    epilog="Find out more on GitHub: https://github.com/honey-py/ccBackendTask1"
)

satellite.add_argument('id', type=str, help='The ID of the satellite whose location is being requested')
satellite.add_argument('date', default="-1", type=str, nargs="?",
                    help='The date on which you want to find the location (optional, '
                         'if you want to know location on a specific date and time)')
satellite.add_argument('time', default="-1", type=str, nargs="?",
                    help='The time at which you want to find the location (optional, '
                         'if you want to know location on a specific date and time)')
satellite.add_argument('-l', '--location', action='store_true',
                    help='Return the location in longitude and latitude format')
satellite.add_argument('-c', '--country', action='store_true',
                    help='Return the location in country code and time zone format')

args = satellite.parse_args()


if args.date == "-1" or args.time == "-1":
    data = json.loads(get(f"https://api.wheretheiss.at/v1/satellites/{args.id}").text)
    latitude = data["latitude"]
    longitude = data["longitude"]
else:
    data = json.loads(get(
        f"https://api.wheretheiss.at/v1/satellites/{args.id}/positions?timestamps={datetime_to_unixtimestamp(args.date, args.time)}").text)
    latitude = data[0]["latitude"]
    longitude = data[0]["longitude"]

if args.location or (not args.country and not args.location):
    print("Longitude: ", longitude)
    print("Latitude: ", latitude)

if args.country or (not args.country and not args.location):
    data = json.loads(get(
        f"https://api.wheretheiss.at/v1/coordinates/{longitude},{latitude}").text)
    if 'error' in data:
        print("This location most likely doesn't have any timezone and country_code")
    else:
        print("Country Code: ", data["country_code"])
        print("Time Zone: ", data["timezone_id"])
