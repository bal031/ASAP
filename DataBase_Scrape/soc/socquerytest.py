""" simple query module for ScheduleOfClasses API 
note not sure how to store authentication tokens yet...
"""
from requests import get, post
import requests.auth
from requests_oauthlib import OAuth1


access_token = "48f68ee9-6ccd-3f82-94d8-a03b1c84b9c4"

url = "https://api.ucsd.edu:8243/get_schedule_of_classes/v1/"
auth_oauth = OAuth1(client_key='csiONAjbrLrimjZrld1PvF3fooUa', client_secret='bchYJo80tfqb4G25Pr8pFXlEbrka')
headers = {
    "authorization" : "Bearer " + access_token
    }


class BearerAuth(requests.auth.AuthBase):
    """Custom Authentication class
    """
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


if __name__ == "__main__":
    print("attempting to make a request...")
    try:
        response = get(url, headers=headers)
        print(response.json())
    except Exception as e:
        print("something went wrong: " + str(e))
