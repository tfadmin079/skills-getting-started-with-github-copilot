from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Users (superheroes)
        users = [
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "Marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "Marvel"},
            {"name": "Spider-Man", "email": "spiderman@marvel.com", "team": "Marvel"},
            {"name": "Batman", "email": "batman@dc.com", "team": "DC"},
            {"name": "Superman", "email": "superman@dc.com", "team": "DC"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "DC"},
        ]
        db.users.insert_many(users)
        db.users.create_index([("email", 1)], unique=True)

        # Teams
        teams = [
            {"name": "Marvel", "members": [u["email"] for u in users if u["team"] == "Marvel"]},
            {"name": "DC", "members": [u["email"] for u in users if u["team"] == "DC"]},
        ]
        db.teams.insert_many(teams)

        # Activities
        activities = [
            {"user_email": "ironman@marvel.com", "activity": "Running", "duration": 30},
            {"user_email": "cap@marvel.com", "activity": "Cycling", "duration": 45},
            {"user_email": "spiderman@marvel.com", "activity": "Swimming", "duration": 25},
            {"user_email": "batman@dc.com", "activity": "Running", "duration": 40},
            {"user_email": "superman@dc.com", "activity": "Cycling", "duration": 50},
            {"user_email": "wonderwoman@dc.com", "activity": "Swimming", "duration": 35},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {"team": "Marvel", "points": 100},
            {"team": "DC", "points": 120},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {"name": "Morning Cardio", "suggested_for": "Marvel"},
            {"name": "Strength Training", "suggested_for": "DC"},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
