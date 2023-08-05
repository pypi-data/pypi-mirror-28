# python-ogn-client

[![Build Status](https://travis-ci.org/glidernet/python-ogn-client.svg?branch=master)](https://travis-ci.org/glidernet/python-ogn-client)
[![PyPi Version](https://img.shields.io/pypi/v/ogn-client.svg)](https://pypi.python.org/pypi/ogn-client)
[![Coverage Status](https://coveralls.io/repos/github/glidernet/python-ogn-client/badge.svg?branch=master)](https://coveralls.io/github/glidernet/python-ogn-client?branch=master)

A python3 module for the [Open Glider Network](http://wiki.glidernet.org/).
It can be used to connect to the OGN-APRS-Servers and to parse APRS-/OGN-Messages.

A full featured gateway with build-in database is provided by [ogn-python](https://github.com/glidernet/ogn-python).


## Installation

python-ogn-client is available at PyPI. So for installation simply use pip:

```
pip install ogn-client
```

## Example Usage

Parse APRS/OGN packet.

```
from ogn.parser import parse
from datetime import date, time

beacon = parse("FLRDDDEAD>APRS,qAS,EDER:/114500h5029.86N/00956.98E'342/049/A=005524 id0ADDDEAD -454fpm -1.1rot 8.8dB 0e +51.2kHz gps4x5",
               reference_date=date(2016,1,1), reference_time=time(11,46))
```

Connect to OGN and display all incoming beacons.

```
from ogn.client import AprsClient
from ogn.parser import parse, ParseError

def process_beacon(raw_message):
    if raw_message[0] == '#':
        print('Server Status: {}'.format(raw_message))
        return
    try:
        beacon = parse(raw_message)
        print('Received {beacon_type} from {name}'.format(**beacon))
    except ParseError as e:
        print('Error, {}'.format(e.message))

client = AprsClient(aprs_user='N0CALL')
client.connect()

try:
    client.run(callback=process_beacon, autoreconnect=True)
except KeyboardInterrupt:
    print('\nStop ogn gateway')
    client.disconnect()
```

## License
Licensed under the [AGPLv3](LICENSE).
