import json
from services import overpass_query
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = '''
Using the provided restaurant name, city, and geolocation, search for the cuisine of the restaurant (mexican, italian, etc) and the cost.
Create a prompt that includes the city, restaurant name, cuisine, geolocation, and a typical meal cost.
Include a one sentence description of the defining feature of the restaurant.
The response should be a total of 2 sentences: general information and the defining feature.

Example:
The Houston, Texas "Hard Rock Cafe" is an American restaurant with a geolocation of (29.7626286, -95.3672993) and a cost of roughly $20 per meal.
This restaurant is known for its iconic guitar-shaped entrance and vibrant rock'n'roll memorabilia collection celebrating music legends.
'''

""" 
Should be a JSON file in this format
[
  {
    "city": "Houston",
    "lat": "29.760427",
    "lon": "-95.369803"
  },
  ...
]
"""
with open('cities.json') as f:
    cities = json.load(f)

# Remove later and fix file
with open('descriptions.json') as f:
    finished_descriptions = json.load(f)

restaurants = []
descriptions = []
count = 1

# Remove later and fix file
desc_counter = 0

for item in cities:
    city = item['city']
    lat = item['lat']
    lon = item['lon']

    print(f'{count}/500: Starting options for {city}...')

    local_restaurants = overpass_query(lat, lon, 3000)
    # formatted_restaurants = [{
    #     "name": name,
    #     "city": city,
    #     "lat": lat,
    #     "lon": lon
    # } for name, lat, lon in local_restaurants if name]

# Remove later and fix file
    formatted_restaurants = []
    for rest in local_restaurants:
        name = rest[0]
        lat = rest[1]
        lon = rest[2]

        if name is None: continue

        formatted_restaurants.append({
            "name": name,
            "city": city,
            "lat": str(lat),
            "lon": str(lon),
            "description": finished_descriptions[desc_counter]
        })

        desc_counter += 1

    restaurants += formatted_restaurants

    # local_count = 1
    # total_count = len(formatted_restaurants)

    # for r in formatted_restaurants:
    #     print(f'{local_count}/{total_count}...Restaurant: {r['name']}')

    #     context = f'Name: ${r['name']}. City: {r['city']}. Geo: {r['lat']}, {r['lon']}.'

    #     messages = [
    #         { 'role': 'system', 'content': SYSTEM_PROMPT },
    #         { 'role': 'user', 'content': context }
    #     ]

    #     client = OpenAI()
    #     response = client.chat.completions.create(
    #         model='gpt-4o-mini',
    #         messages=messages
    #     )

    #     descriptions.append(response.choices[0].message.content)

    #     local_count += 1

    count += 1
    print('')

print('Finished!')

with open('restaurants.json', 'w') as f:
    f.write(json.dumps(restaurants, indent=4))

"""
Writes to a separate Document
Keep hidden unless ready to overwrite
"""
# with open('descriptions.json', 'w') as f:
#     f.write(json.dumps(descriptions, indent=4))

# def display():
#     return descriptions
