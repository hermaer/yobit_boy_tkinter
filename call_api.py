import os 
import json
import requests
import urllib, http.client
import hmac, hashlib

API_KEY = ""
API_SECRET = b""

def nonce():
	with open('nonce', 'r+') as file:
		nonc = file.read()
		nonc = int(nonc)

	with open('nonce', 'w') as file:
		file.write(str(nonc + 1))
	return nonc


def call_api(**kwargs):

    payload = {'nonce': nonce()}

    if kwargs:
        payload.update(kwargs)
    payload =  urllib.parse.urlencode(payload)

    H = hmac.new(key=API_SECRET, digestmod=hashlib.sha512)
    H.update(payload.encode('utf-8'))
    sign = H.hexdigest()
    
    headers = {"Content-type": "application/x-www-form-urlencoded",
           "Key":API_KEY,
           "Sign":sign}
    conn = http.client.HTTPSConnection("yobit.net", timeout=60)
    conn.request("POST", "/tapi/", payload, headers)
    response = conn.getresponse().read()
    
    conn.close()

    try:
        obj = json.loads(response.decode('utf-8'))

        if 'error' in obj and obj['error']:
            raise ValueError
        return obj
    except ValueError:
        raise ValueError('Ошибка анализа возвращаемых данных, получена строка', response)
