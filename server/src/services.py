import requests
import overpy
from typing import TypedDict

api = overpy.Overpass()

class Coordinate(TypedDict):
    lat: float
    lon: float

def geocode_location(location: str):
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': location,
        'format': 'json',
        'limit': 1
    }
    headers = { 'User-Agent': 'food-directions/1.0' }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    lat = float(data[0]['lat'])
    lon = float(data[0]['lon'])

    return { 'lat': lat, 'lon': lon }

def coord_to_str(coord: Coordinate):
    return ','.join([str(coord['lon']), str(coord['lat'])])

def generate_route(source: Coordinate, destination: Coordinate):
    src = coord_to_str(source)
    des = coord_to_str(destination)

    response = requests.get(f'https://router.project-osrm.org/route/v1/driving/{src};{des}?overview=full&geometries=geojson')
    data = response.json()

    return data['routes'][0]['geometry']['coordinates']

def overpass_query(lat, lon, radius=3000):
    query = f"""
    node["amenity"~"restaurant|cafe"](around:{radius},{lat},{lon});
    out;
    """

    response = api.query(query)

    food_options = [[node.tags.get('name'), node.lat, node.lon] for node in response.nodes]

    return food_options
