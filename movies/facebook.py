"""Module for managing requests to facebook api"""
import requests
from MovieDatabase.settings import FACEBOOK_CLIENT_ID, FACEBOOK_CLIENT_SECRET
from typing import List, Dict, Optional, Any
from .models import FacebookProfile

FACEBOOK_API_VERSION = 'v6.0'


def manage_facebook_login(token: str) -> FacebookProfile:
    """
    Manages login in facebook users

    Function creates facebook user in database or if that user already exists,
    only updates its profile.

    Args:
        token: access token from facebook
    """

    def get_facebook_user_from_database(facebook_id: int) -> Optional[FacebookProfile]:
        """Gets user with given facebook id from database or creates one if not exist"""
        user = FacebookProfile.objects.get(facebook_id=facebook_id)
        return user

    def gather_user_profile() -> int:
        """Retrieves user profile info from facebook"""
        facebook_data = FacebookData(token)
        facebook_id = facebook_data.get_user_id()
        return facebook_id

    facebook_id = gather_user_profile()
    try:
        user = get_facebook_user_from_database(facebook_id)
    except FacebookProfile.DoesNotExist:
        user = FacebookProfile.objects.create(facebook_id=facebook_id)

    return user


def make_request_and_get_json(url: str) -> Optional[Dict[str, str]]:
    """
    Makes HTTP GET request to specified url and returns response body.

    Args:
        url: the url to make a request

    Returns:
        Body of the response in json format.
    """
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        return None


class FacebookLogin:
    """A class responsible for LogIn with Facebook operations"""

    @staticmethod
    def get_url_for_facebook_login(redirect_uri: str) -> str:
        """
        Returns url for facebook login.
        Args:
            redirect_uri: the url facebook should redirect after authentication

        Returns:
            url for facebook authentication
        """
        base_url = f'https://www.facebook.com/{FACEBOOK_API_VERSION}/dialog/oauth'
        return (f'{base_url}' +
                f'?client_id={FACEBOOK_CLIENT_ID}&redirect_uri={redirect_uri}')

    @staticmethod
    def exchange_code_for_token(code: str, redirect_uri: str) -> str:
        """
        Sends request to facebook in order to receive user access token.
        Args:
            code: The code received from facebook after successful user authentication
            redirect_uri: the url passed as redirect_uri for login request

        Returns:
            User access token.
        """
        base_url = f'https://graph.facebook.com/{FACEBOOK_API_VERSION}/oauth/access_token'
        url = (f'{base_url}' +
               f'?client_id={FACEBOOK_CLIENT_ID}&redirect_uri={redirect_uri}' +
               f'&client_secret={FACEBOOK_CLIENT_SECRET}&code={code}')
        response = make_request_and_get_json(url)
        return response['access_token']


class FacebookData:
    """
    Class for getting user informations from facebook
    Args:
        access_token: facebook token for accessing user data
    """

    def __init__(self, access_token: str) -> None:
        self.token = access_token

    def get_user_data(self, fields: List[str]) -> Dict[str, Any]:
        """
        Retrieves specified user data from facebook
        Args:
            fields: data to retrieve

        Returns:
            Dictionary with retrieved data
        """
        base_url = f'https://graph.facebook.com/{FACEBOOK_API_VERSION}/me'
        fields_str = ','.join(fields)
        url = f'{base_url}?fields={fields_str}&access_token={self.token}'
        return make_request_and_get_json(url)

    def get_user_id(self) -> int:
        """
        Retrieves user id from facebook
        Returns:
            Facebook id of the user
        """
        return int(self.get_user_data(['id'])['id'])
