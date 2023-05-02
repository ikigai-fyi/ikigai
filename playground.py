import os

from stravalib import Client

MY_ACCESS_TOKEN = os.getenv("MY_ACCESS_TOKEN")
client = Client(access_token=MY_ACCESS_TOKEN)

athlete = client.get_athlete()
print(athlete)
