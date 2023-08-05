WiFindme - Network Geolocation Services
=========================================

Locates the current wifi-enabled computer using nearby access points and
https://radiocells.org/geolocation or 
https://wiki.mozilla.org/CloudServices/Location/FAQ 
or both.

Project home: https://github.com/ways/wifindme

Takes over from https://github.com/ways/locate-radiocells with the added benefit of Mozilla Location Services.

----

Installation
------------

.. code:: bash

  $ pip install wifindme

Dependencies (handled by pip)
-----------------------------

* https://github.com/rockymeza/wifi/
* https://pypi.python.org/pypi/requests/

Usage
-----

Must run as root to get access to scanning on Linux.

Example use:

.. code:: python

    import wifindme
    accuracy, latlng = wifindme.locate(device='wlan0')

Example script included in examples/, (prints out accuracy in meters, and coordinates):

.. code:: bash

  $ sudo ./wifindme.py wlan0
  30 (59.12345, 10.12345)

Compatibility
-------------

Python 2 and 3. Only tested on Linux (Ubuntu, Fedora, Arch).

Development info
----------------

example query sent to radiocells.org:

.. code:: json

  curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"wifiAccessPoints":[{"macAddress":"24-DE-C6-A8-C9-64","signalStrength":-57}]}' https://radiocells.org/backend/geolocate

Example response:

.. code:: json

  {"source": "wifis", "measurements": 14, "location": {"lat": 59.12345, "lng": 10.12345}, "accuracy": 30}

or on fail:

.. code:: json

  {'resultType': 'error', 'results': {'source': 'none', 'measurements': 0, 'location': {'lat': 0.0, 'lng': 0.0}, 'accuracy': 9999}, 'error': {'message': 'Empty request', 'code': 400, 'errors': [{'message': None, 'reason': 'parseError', 'domain': 'global'}]}}

TODO
----

* Notify https://wiki.mozilla.org/CloudServices/Location/Software
* Support fetching location from both at the same time.
* Googles API is compatible, so can add that as well.
* Check with Mozilla if this can be packaged with test API key.
* Correct radiocells "accuracy". They always give 30m...

