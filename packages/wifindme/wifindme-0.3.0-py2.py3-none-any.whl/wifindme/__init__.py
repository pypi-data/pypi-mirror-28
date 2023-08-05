#!/usr/bin/env python3

"""
Locates the current wifi-enabled computer using nearby access points and
https://radiocells.org/geolocation or 
https://wiki.mozilla.org/CloudServices/Location/FAQ 
or both.
"""

import requests # for web request
import socket # For timeout exception
from wifi import Cell, Scheme # for wifi scanning

system_version = '0.3'
system_name = 'wifindme.py'

apiradiocells = 'https://radiocells.org/backend/geolocate'
apimozilla = 'https://location.services.mozilla.com/v1/geolocate?key=test'

verbose = False
start = None
timeout = 10 # api timeout in seconds

if verbose:
    import json     # only used in debugging
    import sys      # only used in debugging
    import time     # for timing

def locate(device='wlan0', min_aps=1, max_aps=0, hiddenaps=True, service='r'):
    """
    device = which wifi device to use. Must be root on linux to scan.
    Min_aps = minimum visible Access Points before a location is looked up. 0 = no limit.
    Max_aps = only send the first x APs to api. 0 = no limit.
    hiddenaps = Use wifi APs with hidden SSID, true or false
    service = Valid choices: 'r', 'm'
    """

    num = 0
    j = '{"wifiAccessPoints":['

    if verbose:
        print ("scan result of", device)
        start = time.time()

    # Loop APs
    for cell in Cell.all(device): 
        ssid=cell.ssid
        if verbose: print(ssid, cell.signal, cell.address)

        if not hiddenaps and 0 == len(ssid): # skip hidden APs
            continue
        num += 1

        if 1 < num: # Build json for AP
            j += ','
        j += '{"macAddress":"%s","signalStrength":%s}' \
            % (cell.address.replace(':', '-'), cell.signal)
        if 0 != max_aps and num >= max_aps:
            break

    j += ']}'

    if verbose:
        print (json.dumps(j, indent=4))
        print ("Scan done in: %s seconds" % (time.time()-start))

    # Ask API (if we've got enough APs to send)
    if (0 < num and num >= min_aps): 
        if verbose: start=time.time()
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        try:
            if 'r' == service:
                response = requests.post(apiradiocells, headers=headers, timeout=timeout, data=(j))
            elif 'm' == service:
                response = requests.post(apimozilla, headers=headers, timeout=timeout, data=(j))
        except requests.exceptions.ReadTimeout as e: # socket.timeout as e:
            if verbose: print ("API timeout." + e)
            return False, (False, False)

        if verbose:
            print(response)
            print(response.json())
            print ("API lookup done in: %s seconds" % (time.time()-start))


        # Decode result: {'source': 'wifis', 'measurements': 504, 'location': {'lat': 59.12345, 'lng': 10.12345}, 'accuracy': 30}
        result = response.json()

        try:
          if result['location']:
            pass
        except KeyError:
            if verbose: "Empty result returned."
            return False, (False, False)

        return result['accuracy'], \
            (result['location']['lat'], result['location']['lng'])
    else:
        return False, (False, False)

if __name__ == "__main__":
    print("This is a library and can't be used directly. Check examples folder, or https://github.com/ways/wifindme/.")
