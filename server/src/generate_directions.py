from .services import geocode_location, generate_directions, overpass_query

def generate(source: str, destination: str):
    src_coord = geocode_location(source)
    des_coord = geocode_location(destination)

    coordinates = generate_directions(src_coord, des_coord)

    points_of_interest = []

    crd_len = len(coordinates)

    for i in range(0, crd_len, (crd_len // 15)):
        lon, lat = coordinates[i]
        result = overpass_query(lat, lon)

        points_of_interest.extend(result)

    return points_of_interest
