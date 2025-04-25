import os
import requests
import psycopg2
from dotenv import load_dotenv


load_dotenv()


GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


def extract_repos(user):
    url = f"https://api.github.com/users/{user}/repos"
    response = requests.get(url, auth=(GITHUB_USERNAME, GITHUB_TOKEN))

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    
    
def transform_repos(repos):
    transformed_repos = []
    for repo in repos:
        transformed_repo = {
            "id": repo["id"],
            "name": repo["name"],
            "full_name": repo["full_name"],
            "description": repo["description"],
            "created_at": repo["created_at"],
            "language": repo["language"],
            "stars": repo["stargazers_count"]

        }
        transformed_repos.append(transformed_repo)
    return transformed_repos


def load_to_postgres(repos):
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
        host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()
        
    

    cur.execute("""
        CREATE TABLE IF NOT EXISTS github_repos (
            id BIGINT PRIMARY KEY,
            name TEXT,
            full_name TEXT,
            description TEXT,
            stars INTEGER,
            language TEXT,
            created_at TIMESTAMP
        );
    """)

    for repo in repos:
        cur.execute("""
            INSERT INTO github_repos (id, name, full_name, description, stars, language, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, (
            repo["id"], repo["name"], repo["full_name"],
            repo["description"], repo["stars"],
            repo["language"], repo["created_at"]
        ))

        
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Data loaded successfully.")

# --- Run ETL ---
if __name__ == "__main__":
    raw_data = extract_repos(GITHUB_USERNAME)
    cleaned_data = transform_repos(raw_data)
    load_to_postgres(cleaned_data)