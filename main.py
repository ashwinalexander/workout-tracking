# Workout Tracking Google Sheet (stored in an env variable)
# Nutrionix API documentation
# https://developer.syndigo.com/docs/nutritionix-api-guide
# https://developer.syndigo.com/docs/natural-language-for-exercise
# v2/natural/exercise

# SHEETY API documentation
# https://v2.sheety.co/docs/getting-started

import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

APP_ID = os.getenv('APP_ID')
API_KEY = os.getenv('API_KEY')
NUT_DOMAIN = "https://trackapi.nutritionix.com"
NUT_ENDPOINT = "/v2/natural/exercise"
NUT_URL = f"{NUT_DOMAIN}{NUT_ENDPOINT}"
SHEETY_URL = os.getenv('SHEETY_API_URL')
SHEETY_BEARER_TOKEN = os.getenv('SHEETY_BEARER_TOKEN')

now = datetime.now()
# we need to pass the date and time into the Google Sheet
today_date = now.strftime("%Y/%m/%d")
today_time = now.strftime("%H:%M:%S")

nut_headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    'Content-Type': 'application/json'
}


# Get natural language input on exercise accomplished
print('Tell me which exercises you did:')
exercise_input = input()

params = {
    "query": exercise_input
}

# POST # https://developer.syndigo.com/docs/natural-language-for-exercise
response = requests.post(url=NUT_URL,json=params, headers=nut_headers)
exercise_info = response.json()

# Write a for loop and send a post request for each exercise item returned by the Nutritionix API
for item in exercise_info["exercises"]:

    sheety_params = {
        "workout": {
            "date": today_date,
            "time": today_time,
            "exercise": item["user_input"],
            "duration": item["duration_min"],
            "calories": item["nf_calories"],
        }
    }

    # Add the Authorization header
    sheety_headers = {'Authorization': f'Bearer {SHEETY_BEARER_TOKEN}'}
    sheety_response = requests.post(url=SHEETY_URL, json=sheety_params, headers=sheety_headers)



