# encoding=utf8
"""
Created on 2016年7月7日

@author: jyang
"""

import requests

requests.packages.urllib3.disable_warnings()


def post_json(url, json):
    response = requests.post(url, verify=False, json=json, timeout=5)
    if response.status_code != 200:
        raise Exception('Http request error, status code: {}'.format(response.status_code))
    return response.json()
