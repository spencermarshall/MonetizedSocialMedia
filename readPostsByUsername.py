import requests
import os
# Replace with your own credentials obtained from your Twitter developer account
bearer_token = os.getenv('BEARER_TOKEN')

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
    username = 'starwars'
    user_info = get_user_info(username)
    if user_info:
        print(user_info)
