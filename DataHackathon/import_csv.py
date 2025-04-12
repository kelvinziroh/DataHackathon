# import_script.py
import csv
import os
import django
from django.utils import timezone
from django.db import transaction

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataHackathon.settings')
django.setup()

from hackathon.models import Team, Participant

def bulk_import_participants(csv_file_path='DataHackathon.csv'):
    """Import all participant data from CSV into myprojectdb"""
    try:
        participants = []
        teams_created = set()  # To track teams already created
        
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Skip empty rows
                if not any(row.values()) or all(not v.strip() for v in row.values()):
                    continue

                email = row['Email address'].strip()
                if not email or Participant.objects.filter(email=email).exists():
                    continue

                first_name = row['First name'].strip()
                last_name = row['Last Name'].strip()
                gender = row['Gender'].strip()
                course = row['Course'].strip()
                cohort = row.get('Cohort', '').strip() or None
                confidence_score = int(row.get('Confidence Score', '0').strip()) if row.get('Confidence Score', '0').strip().isdigit() else 0

                # Create or get team
                team_name = f"{course} Team"
                if team_name not in teams_created:
                    team, created = Team.objects.get_or_create(
                        teamName=team_name,
                        defaults={
                            'league': 'Default League',
                            'accumulatedPoint': 0,
                            'affiliation': 'Unknown',
                            'lateSubmissionDateTime': timezone.now(),
                            'currentPhase': 'Active'
                        }
                    )
                    if created:
                        teams_created.add(team_name)
                else:
                    team = Team.objects.get(teamName=team_name)

                try:
                    date_joined = timezone.make_aware(
                        timezone.datetime.strptime(row['Timestamp'].strip(), '%d/%m/%Y %H:%M:%S')
                    )
                except ValueError:
                    continue

                participants.append(Participant(
                    name=f"{first_name} {last_name}",
                    team=team,
                    email=email,
                    userName=email.split('@')[0],
                    firstName=first_name,
                    lastName=last_name,
                    gender=gender,
                    course=course,
                    cohort=cohort,
                    dateJoined=date_joined,
                    role='Participant',
                    status='Active',
                    confidenceScore=confidence_score
                ))

            # Bulk create with transaction
            with transaction.atomic():
                Participant.objects.bulk_create(participants, batch_size=1000)
                print(f"Successfully imported {len(participants)} participants into myprojectdb")
                print(f"Created {len(teams_created)} teams")

    except FileNotFoundError:
        print(f"CSV file not found: {csv_file_path}")
    except Exception as e:
        print(f"Import failed: {e}")

if __name__ == "__main__":
    # Ensure the CSV file path is correct
    csv_path = 'DataHackathon.csv'  # Update this path
    bulk_import_participants(csv_path)
