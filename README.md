## GitHub ETL Project 🚀
A mini ETL (Extract, Transform, Load) project using Python, Docker, and PostgreSQL to extract a user's GitHub repositories, transform them, and load them into a database.
## Architecture Diagram
![mini_etl](https://github.com/user-attachments/assets/9ce0c249-ba1d-47b2-b5e7-d285bcca6877)
GitHub API --> Python Script (ETL) --> PostgreSQL (Docker)
# 📝 Description
This project runs a complete ETL pipeline:

Extract: Fetches public repositories from a GitHub user using the GitHub API.

Transform: Selects and reformats relevant fields (name, description, language, stars, creation date, etc.).

Load: Inserts the cleaned data into a PostgreSQL table.

Everything runs inside Docker containers, making the setup easy and reproducible.


#✅ Prerequisites
Docker

A GitHub token (for API authentication)

Python 3 (already included in the container)

A GitHub account

#📁 Project Structure
.
├── docker-compose.yml
├── Dockerfile
├── main.py              # ETL script
├── .env                 # Environment variables
└── requirements.txt     # Python dependencies

Configure the .env file

GITHUB_USERNAME=your_github_username
GITHUB_TOKEN=your_github_token

DB_NAME=github_etl

DB_USER=postgres

DB_PASSWORD=yourpassword

DB_HOST=postgres_db

DB_PORT=5432

#🚀 Run the Pipeline
Start the pipeline with:


docker-compose up --build

The python_etl container will run once, load the data, and then stop automatically.

The postgres_db container will remain active and keep the PostgreSQL database running.

#🔎 Verify the Data
To check if the data was successfully loaded, connect to the PostgreSQL container:

docker exec -it postgres_db psql -U postgres -d github_etl

Then run:

SELECT * FROM github_repos LIMIT 5;
