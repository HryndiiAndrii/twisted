import requests


URL = 'https://api.twitch.tv/helix/streams?user_login=alessiasanteramo'
authURL = 'https://id.twitch.tv/oauth2/token'
Client_ID = '50vngdkhl7a1e7hndy4jde5vn86jil'
Secret = '1f3od2iruizc6opve05afluo4qni7m'

AutParams = {'client_id': Client_ID,
             'client_secret': Secret,
             'grant_type': 'client_credentials'}


def get_authorization_token():
    AutCall = requests.post(url=authURL, params=AutParams)
    access_token = AutCall.json()['access_token']
    return access_token


def check_channel():
    access_token = get_authorization_token()

    head = {'Client-ID': Client_ID,
            'Authorization': "Bearer " + access_token}

    r = requests.get(URL, headers=head).json()['data']

    return r

if __name__ == '__main__':
    # outfile = open('key.txt', 'w')
    # outfile.write(get_authorization_token())
    # outfile.close()
    print(check_channel())
