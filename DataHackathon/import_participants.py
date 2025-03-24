import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from hackathon.models import Participant, Team

class Command(BaseCommand):
    help = 'Import participants from a CSV file into PostgreSQL'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        # Get or create a default team (adjust as needed)
        team, _ = Team.objects.get_or_create(name='Default Team')

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Parse timestamp
                    date_joined = datetime.strptime(row['Timestamp'], '%d/%m/%Y %H:%M:%S')

                    # Create participant
                    participant = Participant(
                        team=team,
                        email=row['Email address'],
                        userName=row['Email address'].split('@')[0],  # Generate username from email
                        firstName=row['First name'],
                        lastName=row['Last Name'],
                        gender=row['Gender'],
                        course=row['Course'],
                        cohort=row['Cohort'] if row['Cohort'] != 'None student' else None,
                        dateJoined=date_joined,
                        role='participant',  # Default value
                        status='active',     # Default value
                        confidenceScore=int(row['Confidence Score'])
                    )
                    participant.full_clean()  # Validate the model
                    participant.save()
                    self.stdout.write(self.style.SUCCESS(f"Added: {participant}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error processing row {row}: {e}"))
