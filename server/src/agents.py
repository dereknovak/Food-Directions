import instructor
import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, model_validator
from typing import TypedDict

from langchain.agents import tool, initialize_agent
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType

from services import geocode_location, generate_route
from search import search_restaurants, closest_restaurants

load_dotenv()

class Coordinate(TypedDict):
    lat: float
    lon: float

client = instructor.from_provider(
    'openai/gpt-4.1-mini',
    mode=instructor.Mode.RESPONSES_TOOLS
)

class PriceRange(TypedDict):
    min: int
    max: int

class Query(BaseModel):
    cuisine: str | None = Field(description='Food cuisine requested. If none, return None')
    price_range: PriceRange | None = Field(description='Approximate min/max price of query. Min should be 50 percent less and Max 50 percent more than requested amount.') 

    # @model_validator(mode='after')
    # def validate_price(cls, query):
    #     if not query: return
    #     try:
    #         if query.price_range['min'] <= 0:
    #             raise ValueError('Minimum value cannot be 0 or less. Bring all minimum values less than 5 to 5.')
    #         return query
    #     except ValueError as e:
    #         print('Validation failed:', e)

# query = client.responses.create(
#     model='gpt-4o-mini',
#     input=[
#         { 'role': 'user', 'content': "I'm looking for a mexican restaurant halfway between Dallas and Austin. I don't wanna spend more than $10." }
#     ],
#     response_model=Query
# )

# print(query)

@tool
def get_geolocation(city: str) -> Coordinate:
    """Accepts a city string as an argument and returns a geolocation dict"""
    return geocode_location(city)

@tool
def get_route(source: Coordinate, dest: Coordinate):
    """Returns an object with ordered geolocation waypoints between the provided source and destination object parameters"""
    route = generate_route(source, dest)

    waypoints = []
    length = len(route)

    for i in range(0, length, (length // 15)):
        waypoints.append(route[i])

    return waypoints

# @tool
# def get_restaurants(query: Query, waypoint: list[float], limit: int):
#     """Returns a list containing a specified amount of restaurants relevant to query from restaurant database"""
#     price_range = f'{query.price_range['min']}-{query.price_range['max']}' if query.price_range else ''
#     content = f'{query.cuisine} {price_range} {waypoint}'

#     return search_restaurants(content, limit)

@tool
def get_waypoint(route: list[list[float, float]], index: int, length: int):
    """Returns the geolocation waypoint reversed on a route ordered from source to destination. Use length of routes list to determine which index is used"""
    waypoint = route[index]
    waypoint.reverse()

    return waypoint

@tool
def get_closest_restaurants(query: str, coord: Coordinate, limit=5):
    """Returns a sorted list of closest restaurants, including name, description, and distance in meters. Convert the distance to miles."""
    return closest_restaurants(query, coord)


tools = [get_geolocation, get_route, get_closest_restaurants, get_waypoint]

llm = ChatOpenAI(model='gpt-4o', temperature=0)
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# agent.run('Give me 5 resaurants between Copperas Cove and Killeen')
# agent.run('Give me a list of 5 mexican restaurants at the halfway point between Copperas Cove and Dallas')

def ask_agent(route, context):
    return agent.run(f'{route} {context}')