import requests
import os
import json
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, user_url):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = { 
        'Authorization': token
    }
    long_user_url = {
        "long_url": user_url
    }
    response = requests.post(url, headers=headers, json=long_user_url)
    response.raise_for_status()
    resp = response.json()['id']
    return resp


def count_clicks(token, link):
    url = 'https://api-ssl.bitly.com/v4/bitlinks/{0}/clicks/summary'
    headers = { 
        'Authorization': token
    }
    payload = {
        "unit": "day",
        "units": "-1"
    }
    response = requests.get(url.format(link), headers=headers, params=payload)
    response.raise_for_status()
    resp = response.json()["link_clicks"]
    return resp
    

def is_bitlink(token, user_url):
    url = 'https://api-ssl.bitly.com/v4/bitlinks/{0}'
    headers = { 
        'Authorization': token
    }
    response = requests.get(url.format(user_url), headers=headers)
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser(description='Описание программы')
    parser.add_argument('name', type=str, help='Введите url')
    args = parser.parse_args()
    user_parse = urlparse(args.name)
    url_merge = f'{user_parse.scheme}://{user_parse.netloc}/{user_parse.path}'
    user_merge_net_path = '{0}{1}'.format(user_parse.netloc, user_parse.path)
    bitly_token = os.environ['BITLY_TOKEN']
    try:
        if is_bitlink(bitly_token, user_merge_net_path):
            print(count_clicks(bitly_token, user_merge_net_path))
        else:
            print(shorten_link(bitly_token, url_merge))
    except requests.exceptions.HTTPError as error:
        print('Произошла ошибка, необходимо приобрести данную услугу:\n{0}'.format(error))
