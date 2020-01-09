import threading
from gpiozero import Button
from time import sleep

import requests
import hashlib
import json

requests.packages.urllib3.disable_warnings()

BASE_URL = "https://smartapi.vesync.com"

class VesyncApi:
    def __init__(self, username, password):
        payload = json.dumps({"account":username,"devToken":"","password":hashlib.md5(password.encode('utf-8')).hexdigest()})
        account = requests.post(BASE_URL + "/vold/user/login", verify=False, data=payload).json()
        if "error" in account:
            raise RuntimeError("Invalid username or password")
        else:
            self._account = account
        self._devices = []

    def get_devices(self):
        self._devices = requests.get(BASE_URL + '/vold/user/devices', verify=False, headers=self.get_headers()).json()
        return self._devices

    def turn_on(self,id):
        requests.put(BASE_URL + '/v1/wifi-switch-1.3/' + id + '/status/on', verify=False, data={}, headers=self.get_headers())

    def turn_off(self, id):
        requests.put(BASE_URL + '/v1/wifi-switch-1.3/' + id + '/status/off', verify=False, data={}, headers=self.get_headers())

    def get_headers(self):
        return {'tk':self._account["tk"],'accountid':self._account["accountID"]}

api = VesyncApi("email","password")


def top_switch(b,outletid):
    topswitch = Button(b)
    
    for x in api.get_devices():
        if x['cid'] == outletid:
            state = len(x['deviceStatus']) == 2
            break

    while True:
        if topswitch.is_pressed:
            if state:
                api.turn_off(outletid)
                state = False
            else:
                api.turn_on(outletid)
                state = True
            while (topswitch.is_pressed):
                sleep(1)

  
def bottom_switch(b,outletid):
    bottomswitch = Button(b)
    
    for x in api.get_devices():
        if x['cid'] == outletid:
            state = len(x['deviceStatus']) == 2
            break

    while True:
        if bottomswitch.is_pressed:
            if state:
                api.turn_off(outletid)
                state = False
            else:
                api.turn_on(outletid)
                state = True
            while (bottomswitch.is_pressed):
                sleep(1)
  
if __name__ == "__main__": 
    # creating thread 
    t1 = threading.Thread(target=top_switch, args=(17,'0ad5682d-956f-4cf1-99fb-666d87a1aad6'))
    t2 = threading.Thread(target=bottom_switch, args=(27,'1b9dfad4-25c3-4df9-a1ab-5bd79422c224'))

    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()


