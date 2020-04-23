#!/usr/local/bin/python3

from whiptail import Whiptail
import requests
import json

endpoint = "http://YOURIP/api/"
hass = {
        "Authorization": "Bearer YOURTOKEN",
        "Content-Type": "application/json"
}

devices = {
    'NAME1': ['DEVICEID','light',3],
    'NAME2': ['DEVICEID','light',3],
    'NAME3': ['DEVICEID','light',3]
}

def setStatus(device):
    d = "services/"+device[1]+"/"
    if w.confirm('SWITCH ON ?'):
        d += "turn_on"
    else:
        d += "turn_off"
    print(requests.post(endpoint+d, headers=hass, data=json.dumps({'entity_id':device[0]})).text)

def setBrightness(device):
    d = "services/"+device[1]+"/turn_on"
    br = round(int(w.menu('SET BRIGHTNESS', ('0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100')).decode())/100*255)
    print(requests.post(endpoint+d, headers=hass, data=json.dumps({'entity_id':device[0], 'brightness': br})).text)

def setColor(device):
    d = "services/"+device[1]+"/turn_on"
    c = w.menu('SET COLOR', ('WHITE', 'RED', 'ORANGE', 'YELLOW', 'GREEN', 'LIME', 'CYAN', 'BLUE', 'MAGENTA', 'PURPLE')).decode()
    if c == 'WHITE':
        print(requests.post(endpoint+d, headers=hass, data=json.dumps({'entity_id':device[0], 'white_value': 255, 'color_temp': 288})).text)
    else:
        print(requests.post(endpoint+d, headers=hass, data=json.dumps({'entity_id':device[0], 'color_name':c})).text)
    
def chooseAction(device):
    if device[2] == 2:
        menu = ('STATUS', 'BRIGHTNESS')
    elif device[2] == 3:
        menu = ('STATUS', 'BRIGHTNESS', 'COLOR')

    ret = w.menu('CHOOSE ACTION', menu).decode()

    if ret == 'STATUS':
        setStatus(device)
    elif ret == 'BRIGHTNESS':
        setBrightness(device)
    elif ret == 'COLOR':
        setColor(device)

w = Whiptail()
dat = []
for d in devices.keys():
    dat.append(d)
dat.append("EXIT")

dat = tuple(dat)
ret = ''

while True:
    ret = w.menu('LIGHTS', dat).decode()
    if ret == 'EXIT':
        break
    dev = devices[ret]
    if dev[2] == 1:
        setStatus(dev)
    elif dev[2] > 1:
        chooseAction(dev)
