import os
from openai import OpenAI
import psycopg2
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

with open('restaurants.json') as f:
    restaurants = json.load(f)

def generate_embeddings():
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        user=os.getenv('DATABASE_USER'),
        database='restaurants'
    )
    cursor = conn.cursor()

    counter = 1
    length = len(restaurants)

    try:
        for item in restaurants:
            text = item['description']
            
            response = client.embeddings.create(
                model='text-embedding-3-small',
                input=text
            )
            embedding = response.data[0].embedding

            cursor.execute(
                'INSERT INTO restaurant (name, city, lat, lon, description, embedding) VALUES (%s, %s, %s, %s, %s, %s)',
                (item['name'], item['city'], float(item['lat']), float(item['lon']), text, embedding)
            )
            print(f'{counter}/{length} Stored embedding for: {item['name']}...')

            counter += 1

        conn.commit()
        print('All embeddings stored successfully!')

    except Exception as e:
        print('Error generating embeddings: ', e)

generate_embeddings()

# if __name__ == '__main__':
#     generate_embeddings()

