# Copyright © 2018 Po Huit
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Fetch EVE systems and stargates using ESI

# Some code based on
# http://docs.python.org/3/howto/urllib2.html

from time import sleep
import urllib.parse as parse
import urllib.request as request
import urllib.error as error
import json
from sys import stderr

esi_base = "http://esi.tech.ccp.is/latest/"
max_retries = 5
retry_timeout = 5.0
request_rate = 30.0

def ccp_request(path, args=None):
    assert args == None
    url = esi_base + path + "/"
    for retries in range(max_retries):
        try:
            with request.urlopen(url) as response:
                sleep(1.0/request_rate)
                return json.loads(response.read())
        except error.HTTPError as e:
            print("http error: ", e.code, file=stderr)
            if retries < max_retries - 1:
                sleep(retry_timeout)
        except error.URLError as e:
            print("bad url", url + ":", e.reason, file=stderr)
            exit(1)
    print("fetch failed for", url, file=stderr)
    exit(1)

by_system_id = dict()
systems = ccp_request('universe/systems')
print(len(systems), "systems")
for system_id in systems:
    system = ccp_request('universe/systems/' + str(system_id))
    print(system['name'])
    by_system_id[system_id] = system

by_stargate_id = dict()
for system_id, system in by_system_id.items():
    stargates = system['stargates']
    for stargate_id in stargates:
        stargate = ccp_request('universe/stargates/' + str(stargate_id))
        print(system['name'], "->", stargate_id)
        by_stargate_id[stargate_id] = stargate

info = {'systems': by_system_id, 'stargates': by_stargate_id}
with open('eve-map.json', 'w') as dumpfile:
    json.dump(info, dumpfile)
