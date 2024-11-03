import psycopg2
from dynaconf import Dynaconf

# Initialize settings
settings = Dynaconf(
    settings_files=["settings.yaml", ".secrets.yaml"],
    environments=True,
    merge_enabled=True,
    default_env="default",
)


def test_connection():
    try:
        # Replace these parameters with your own
        conn = psycopg2.connect(
            dbname=settings.postgres_db.database,
            user=settings.postgres_db.user,
            password=settings.postgres_db.password,
            host=settings.postgres_db.host,
            port=settings.postgres_db.port
        )
        
        # If connection is successful
        print("Connection to PostgreSQL database was successful!")
        conn.close()
        
    except psycopg2.OperationalError as e:
        print("Failed to connect to the database")
        print("Error:", e)

if __name__ == "__main__":
    test_connection()