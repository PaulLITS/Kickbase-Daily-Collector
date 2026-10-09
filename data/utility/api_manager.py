import time
from datetime import datetime, timedelta
import requests
import json
import pytz
import sys
from typing import Union

sys.stdout.reconfigure(encoding="utf-8")

TIMEZONE_DE = pytz.timezone('Europe/Berlin')
def parse_date(date: str) -> datetime:
    return datetime.fromisoformat(date.replace("Z", "+00:00"))

login_url = "https://api.kickbase.com/v4/user/login"
start = '01.07.2023'
class ApiManager:
    def __init__(self):
        self.base_url: str = "https://api.kickbase.com/v4"
        self.users = None
        self.throttle = None
        self.cache = None
        self.league = None
        self.api = None
        self.start = None
        self.leagueid = None
        
        
    def init(self, options):
        # Kickbase login
        login_payload = {
        "em": options.mail,
        "loy": "false",
        "pass": options.pw,
        "rep": {}
        }
        
        session = requests.Session()
        response = session.post(login_url, json=login_payload)
        if response.status_code == 200:
            j = response.json()
            self.token = j["tkn"]
            self.token_expire = parse_date(j["tknex"])

            self._username = options.mail
            self._password = options.pw

           
            leagues = j["srvl"]

        elif response.status_code == 401:
            raise Exception()
        else:
            raise Exception()

        # Setup league
        if options.league:
            self.league = None
            for league in leagues:
                if league.name == options.league:
                    self.league = league

            if self.league is None:
                raise Exception(f'League "{options.league}" not found.')
        else:
            self.league = leagues[0]
            self.leagueid = leagues[0]["id"]

        self.cache = {}
        self.throttle = 0.01
        
        url = f"https://api.kickbase.com/v4/leagues/{self.leagueid}/settings/managers"

        payload = {}
        headers = {
           'Accept': 'application/json',
           'Authorization': f'Bearer {self.token}',
           'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        # Setup user list
        data = response.json()

        self.users = [user for user in data["us"] 
                      if user["n"] not in options.ignore ]
        self.start = TIMEZONE_DE.localize(datetime.strptime(start, '%d.%m.%Y'))
    
    def get_bonus(self):
        self.get("/bonus/collect")
    
    def _auth_cookie(self):
        return "kkstrauth={}".format(self.token)

    def _is_token_valid(self):
        if self.token is None or self.token_expire is None:
            return False
        return self.token_expire > datetime.now() - timedelta(days=1)
    
    def _url_for_endpoint(self, endpoint: str):
        return self.base_url + endpoint
    
    def get(self, endpoint: str):
        if endpoint not in self.cache:
            time.sleep(self.throttle)

            # Make sure the login token is still valid
            if not self._is_token_valid:
                self.login(self._username, self._password)

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            # Add authentication
            headers["Cookie"] = self._auth_cookie()

            # Measure request time
            start = time.time()

            response = requests.get(
                self._url_for_endpoint(endpoint),
                headers=headers
            )

            delay = time.time() - start

            # Update throttle
            self.throttle = (self.throttle + delay) / 2

            if self.throttle > 1:
                self.throttle = 1

            # Store parsed JSON in cache
            self.cache[endpoint] = response.json()

        return self.cache[endpoint]
    
    
    
manager = ApiManager()
