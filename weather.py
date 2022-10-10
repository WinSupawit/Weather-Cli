import os
import argparse
import json
import sys
from dotenv import load_dotenv
from urllib import parse, request, error

load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def user_args():

    parser = argparse.ArgumentParser(
        description = "Gets weather information for city"
    )

    parser.add_argument(
        'city',
        nargs = '+',
        type = str,
        help = "Enter city name"
    )

    parser.add_argument(
        '-i',
        '--imperial',
        action = 'store_true',
        help = "Display temperature in imperial units"
    )

    return parser.parse_args()

def create_weather_url(city_input, imperial=False):

    city_name = " ".join(city_input)
    city_name_url = parse.quote_plus(city_name)
    if imperial:
        units = 'imperial'
    else:
        units = 'metric'

    url = (
        f"{BASE_URL}?q={city_name_url}"
        f"&units={units}&appid={API_KEY}"
    )

    return url

def get_weather_data(weather_url):

    try:
        response = request.urlopen(weather_url)
    except error.HTTPError as http_error:
        if http_error.code == 404:
            sys.exit("City data not found.")
        elif http_error.code == 401:
            sys.exit("Check your API key.")
        else:
            sys.exit("Something went wrong...({http_error.code})")

    data = response.read()

    try:
        return json.loads(data)
    except json.JSONDecodeError:
        sys.exit("Couldn't read server response.")

def display_weather_data(weather_data, imperial=False):
    city = weather_data['name']
    description = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']
    if imperial:
        imp = 'F'
    else:
        imp = 'C'

    print(f"{city}", end="")
    print(f"\t{description.capitalize()}", end=" ")
    print(f"({temperature}°{imp})")

if __name__ == "__main__":
    args = user_args()
    weather_url = create_weather_url(args.city, args.imperial)
    weather_data = get_weather_data(weather_url)
    display_weather_data(weather_data, args.imperial)
