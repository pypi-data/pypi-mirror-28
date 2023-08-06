# OKTA plugin for cloudtoken.
#
# You will need to add the key 'okta_url' with the value being the URL for your OKTA IdP, for example:
#
# okta_url: !!str 'https://{{example}}.okta.com
#
# Author: Andy Loughran (andy@lockran.com)

import xml.etree.ElementTree as Et
import re
import requests
import argparse
import json
from botocore.compat import urlsplit
from bs4 import BeautifulSoup


class Plugin(object):
    def __init__(self, config):
        self._config = config
        self._name = 'okta'
        self._description = 'Authenticate against OKTA.'

    def __str__(self):
        return __file__

    @staticmethod
    def unset(args):
        pass

    @staticmethod
    def arguments(defaults):
        parser = argparse.ArgumentParser()
        return parser

    def execute(self, data, args, flags):
        url, host = (None, None)

        try:
            url = self._config['okta_url']
        except KeyError:
            print("Configuration key 'okta_url' not found. Exiting.")
            exit(1)

        try:
            host = re.search(r'(https?://[\w\-.]+)/', url).group(1)
        except AttributeError:
            print("Configuration key 'okta_url' value does not seem to be a http(s) URL. Exiting.")
            exit(1)

        requests.packages.urllib3.disable_warnings()  # Disable warning for self signed certs.
        session = requests.session()

        username = args.username
        password = args.password
        authurl = "api/v1/authn"

        content = {}
        content['username'] = username
        content['password'] = password
        headers = {
            'Accept': 'application/json', 
            'Content-Type': 'application/json'
            }
        content['options'] = {
            'multiOptionalFactorEnroll': 'true',
            'warnBeforePasswordExpired': 'true'
            }

        endpoint = url
        short_url = "https://" + urlsplit(endpoint).netloc + "/"
        fullurl = short_url + authurl;

        r = session.post(fullurl, headers=headers, data=json.dumps(content))
        response = json.loads(r.text)
        token = response['stateToken']
        id = response['_embedded']['factors'][0]['id']

        verifyurl = short_url + authurl + "/factors/" + id + "/verify"
        vcontent = {}
        vcontent['stateToken'] = token
        selection = input("Please enter your MFA code: ")
        vcontent['passCode'] = selection
        v = session.post(verifyurl, headers=headers, data=json.dumps(vcontent)) 
        sToken = json.loads(v.text)['sessionToken']
        saml_url = endpoint + '?sessionToken=%s' % sToken
        response = session.get(saml_url)
        soup = BeautifulSoup(response.text, "html.parser")
        saml = soup.find("input", attrs={"name": "SAMLResponse"})
        r = saml['value']
        data.append({'plugin': self._name, 'data': r})
        return data
