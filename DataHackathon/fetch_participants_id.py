# fetch_participant_ids.py
import psycopg2
from psycopg2 import Error

def fetch_participant_data_with_ids():
    try:
        # Database connection parameters
        connection = psycopg2.connect(
            database="myprojectdb",
            user="myuser",      # Replace with your PostgreSQL username
            password='mypassword', # Replace with your PostgreSQL password
            host="localhost",
            port="5432"
        )

        # Create a cursor to execute queries
        cursor = connection.cursor()

        # SQL query to fetch IDs, names, and emails
        query = "SELECT id, name, email FROM hackathon_participant;"
        cursor.execute(query)

        # Fetch all rows
        participants = cursor.fetchall()

        # Print the results
        for participant in participants:
            participant_id, name, email = participant
            print(f"ID: {participant_id}, Name: {name}, Email: {email}")

        # Print total count
        print(f"Total participants: {len(participants)}")

        # Optional: Save to a file
        with open('participants_with_ids.txt', 'w') as f:
            for participant in participants:
                participant_id, name, email = participant
                f.write(f"ID: {participant_id}, Name: {name}, Email: {email}\n")

    except (Exception, Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")
    
    finally:
        # Close database connection
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
            print("PostgreSQL connection closed.")

if __name__ == "__main__":
    fetch_participant_data_with_ids()