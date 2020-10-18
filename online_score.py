import requests

API_URL = "https://ants-leaderboard.herokuapp.com/api/scores"


def save_score(username, score):
    try:
        data = {'username': username, 'score': score}
        requests.post(API_URL, json=data)
    except requests.exceptions.RequestException:
        print("Unable to save high score")


def get_scores():
    try:
        response = requests.get(API_URL)
        return response.json()
    except requests.exceptions.RequestException:
        print("Unable to fetch high scores")
        return {}
