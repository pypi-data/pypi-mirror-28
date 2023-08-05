# -*- coding: utf-8 -*-

"""Market Maker abstract module."""

import os, string, json, re
import requests
import click

class MarketMaker:
    """
    MarketMaker cli
    """
    _url = 'http://127.0.0.1:7783/'
    _userpass_file = 'SuperNET/iguana/dexscripts/userpass'

    allowed_methods = [
        'orderbook' 
    ]

    def __init__(self, home, method, *args, **kwargs):
        self.method = getattr(self, method, None)
        self._userpass = self._get_userpass(home) 
        self.response = self.method(*args, **kwargs) 
        click.echo(self.response)   

    def _get_userpass(self, home):
        file = open(os.path.join(home,self._userpass_file), 'r')
        for line in file:
            userpass = re.search('export userpass="(.*?)"', line).group(1)
            return userpass
    
    def _call(self, *args, **kwargs):
        self._userpass = "62e2722a87f7fd32c043950d60b64b0846601607d0c9baf14248989f352cea4c"

    def orderbook(self, *args, **kwargs):
        self._userpass = "62e2722a87f7fd32c043950d60b64b0846601607d0c9baf14248989f352cea4c"
        payload = {"userpass": self._userpass, "method": "orderbook", "base": "MNZ", "rel": "KMD"}
        r = requests.post(self._url, data=json.dumps(payload))
        return r.text