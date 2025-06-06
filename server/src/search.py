import os
import psycopg2
from psycopg2.extras import RealDictCursor
import openai
from dotenv import load_dotenv

load_dotenv()

DB_PARAMS = {
    "host": os.getenv('DATABASE_HOST'),
    "port": os.getenv('DATABASE_PORT'),
    "user": os.getenv('DATABASE_USER'),
    "database": os.getenv('DATABASE_NAME'),
}

def generate_embedding(text):
    """Generate an embedding vector for the given text using OpenAI API."""
    client = openai.OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding

def search_restaurants(query, limit=5):
    try:
        embedding = generate_embedding(query)

        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute(
            """
            SELECT
                description,
                1 - (embedding <=> %s::vector) as similarity
            FROM restaurant
            WHERE 1 - (embedding <=> %s::vector) > 0.4
            ORDER BY similarity DESC
            LIMIT %s
            """,
            (embedding, embedding, limit)
        )

        results = cursor.fetchall()
        conn.close()

        return results
    
    except Exception as e:
        print(f'Effor searching activities: {e}')
        raise e