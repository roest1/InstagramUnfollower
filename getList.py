import os
import sys
import time
import requests
import pickle
import json
import re
from datetime import datetime
from settings import *

CACHE_DIRECTORY = 'Cache'
SESSION_CACHE = f'{CACHE_DIRECTORY}/session.txt'
FOLLOWERS_CACHE = f'{CACHE_DIRECTORY}/followers.json'
FOLLOWING_CACHE = f'{CACHE_DIRECTORY}/following.json'

INSTAGRAM_URL = 'https://www.instagram.com'
LOGIN_ENDPOINT = f'{INSTAGRAM_URL}/accounts/login/ajax/'
PROFILE_ENDPOINT = f'{INSTAGRAM_URL}/api/v1/users/web_profile_info/'
# Need to use string formatting to dynamically choose user's endpoints
FOLLOWERS_ENDPOINT = f'{INSTAGRAM_URL}/api/v1/friendships/{{}}/followers/' 
FOLLOWING_ENDPOINT = f'{INSTAGRAM_URL}/api/v1/friendships/{{}}/following/'

def get_headers_and_cookies(session):
    # Set up a custom User-Agent and other headers to mimic a real web browser
    headers = {
        'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')
    }
    # get cookies
    res1 = session.get(INSTAGRAM_URL, headers=headers)
    ig_app_id = re.findall(r'X-IG-App-ID":"(.*?)"', res1.text)[0]

    res2 = session.get('https://www.instagram.com/data/shared_data/',
                       headers=headers, cookies=res1.cookies)
    csrf = res2.json()['config']['csrf_token']
    if csrf:
        headers['x-csrftoken'] = csrf
        # extra needed headers
        headers['accept-language'] = "en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7,es;q=0.6,es-MX;q=0.5,es-ES;q=0.4"
        headers['x-requested-with'] = "XMLHttpRequest"
        headers['accept'] = "*/*"
        headers['referer'] = "https://www.instagram.com/"
        headers['x-ig-app-id'] = ig_app_id
        cookies = res1.cookies.get_dict()
        cookies['csrftoken'] = csrf
    else:
        print("No csrf token found in code or empty, maybe you are temp ban? Wait 1 hour and retry")
        return False

    time.sleep(5)

    return headers, cookies

def login(session, headers, cookies):
    # Prepares username and password for POST request to log in
    # Encryption format for password is specified by Instagram for browser logins
    post_data = {
        'username': USERNAME,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:{PASSWORD}'
    }

    response = session.post(LOGIN_ENDPOINT, headers=headers,
                            data=post_data, cookies=cookies, allow_redirects=True)
    
    response_data = json.loads(response.text)

    if 'two_factor_required' in response_data:
        print('Please disable 2-factor authentication to login.')
        sys.exit(1)

    if 'message' in response_data and response_data['message'] == 'checkpoint_required':
        print('Please check Instagram app for a security confirmation that it is you trying to login.')
        sys.exit(1)

    return response_data['authenticated'], response.cookies.get_dict()


def get_social_list(session, headers, route):
    social_list = []

    # Initial request to get the first batch of users
    response = session.get(route, headers=headers).json()
    while response['status'] != 'ok':
        time.sleep(600)  # If querying too much, wait before retrying
        response = session.get(route, headers=headers).json()

    print('.', end='', flush=True)
    social_list.extend(response['users'])

    # Continue fetching users if a 'next_max_id' is present, indicating more data to fetch
    while 'next_max_id' in response:
        time.sleep(2)  # Short delay to avoid hitting the rate limit
        next_max_id = response['next_max_id']
        response = session.get(f"{route}?max_id={next_max_id}", headers=headers).json()
        while response['status'] != 'ok':
            time.sleep(600)  # If querying too much, wait before retrying
            response = session.get(f"{route}?max_id={next_max_id}", headers=headers).json()

        print('.', end='', flush=True)
        social_list.extend(response['users'])

    return social_list


def update_social_list(session, list_type, user_account, headers):
    '''
    session: requests.Session() object
    list_type: "following" or "followers"
    user_account: user account object
    headers: request headers
    '''  
    if list_type == 'following':
        cache = FOLLOWING_CACHE
        route = FOLLOWING_ENDPOINT.format(user_account['id'])
        edge_name = 'edge_follow'
    elif list_type == 'followers':
        cache = FOLLOWERS_CACHE
        route = FOLLOWERS_ENDPOINT.format(user_account['id'])
        edge_name = 'edge_followed_by'
    else:
        raise ValueError('update_social_list() must take "following" or "followers" as the list_type argument.')

    try:
        # Attempt to load the list from cache if it exists
        if os.path.isfile(cache):
            with open(cache, 'r') as f:
                social_list = json.load(f)
            print(f'{list_type.capitalize()} list loaded from cache file.')
        else:
            social_list = []
        
        needs_update = len(social_list) != user_account[edge_name]['count']
        action = 'Rebuilding' if social_list else 'Building'
        if needs_update:
            print(f"{action} {list_type} list...")
            social_list = get_social_list(session, headers, route)
            print("Done")
        
            # Update the cache with the new social list
            with open(cache, 'w') as f:
                json.dump(social_list, f)
        elif not social_list:
            print(f"No {list_type} list to load, and no data to fetch.")

        return social_list
    
    except Exception as e:
        print(f"Error handling {list_type} list: {e}")
        sys.exit(1)


def main():

    session = requests.Session()

    # Check if we have saved cache for logging in
    # If we do, we can avoid logging in multiple times (risking temporary ban)
    if not os.path.isdir(CACHE_DIRECTORY):
        os.makedirs(CACHE_DIRECTORY)
    
    headers, cookies = get_headers_and_cookies(session)

    if os.path.isfile(SESSION_CACHE):
        with open(SESSION_CACHE, 'rb') as f:
            session.cookies.update(pickle.load(f))
    else:
        is_logged, cookies = login(session, headers, cookies)
        if is_logged == False:
            sys.exit('login failed, verify user/password combination')

        with open(SESSION_CACHE, 'wb') as f:
            pickle.dump(session.cookies, f)

        time.sleep(5)
    
    # Get user profile
    response = session.get(PROFILE_ENDPOINT, params={'username': USERNAME}, headers=headers).json()
    user_account = response['data']['user']
    print(f"You're now logged as {user_account['username']} ({user_account['edge_followed_by']['count']} followers, {user_account['edge_follow']['count']} following)")
    time.sleep(5)

    # Get "following" list
    following = update_social_list(session, "following", user_account, headers)
    
    # Get "followers" list
    followers = update_social_list(session, "followers", user_account, headers)

    followers_usernames = {user['username'] for user in followers}
    unfollow_users_list = [
        user for user in following if user['username'] not in followers_usernames]

    print(f'you are following {len(unfollow_users_list)} user(s) who aren\'t following you:')
    with open('people_to_unfollow.txt', 'w') as file:
        for user in unfollow_users_list:
            file.write(f"{user['username']}\n")
    print("See list of people to unfollow in people_to_unfollow.txt\nYou might want to read through this list and take out any accounts you want to keep following before moving onto the unfollowing program.")

if __name__ == '__main__':
    main()