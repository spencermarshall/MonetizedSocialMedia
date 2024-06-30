import requests
import os
# Replace with your own credentials obtained from your Twitter developer account
bearer_token = 'AAAAAAAAAAAAAAAAAAAAADGfuAEAAAAAiKXhRiJILcmDv54r2LVG8PpizMU%3DOveJUzcf8xrH2G1uL32SFFG1WAj0s1He8Wf75y4lYUX0jcOj1K'

def create_headers(bearer_token):
    headers = {"Authorization": f"Bearer {bearer_token}"}
    return headers

def get_user_info(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    headers = create_headers(bearer_token)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.json()}")
        return None

if __name__ == "__main__":
    username = 'elonmusk'
    user_info = get_user_info(username)
    if user_info:
        print(user_info)
