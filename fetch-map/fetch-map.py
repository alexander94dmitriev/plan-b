# Copyright © 2018 Po Huit
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

# Fetch EVE systems and stargates using ESI

from time import sleep
import http.client as client
import json
from sys import stdout, stderr
import threading

esi_endpoint = "esi.tech.ccp.is"
esi_version = "latest"
max_retries = 5
retry_timeout = 5.0
reopen_timeout = 5.0
request_rate = 20.0
nthreads = 20

# https://stackoverflow.com/a/312464
def chunks(l, n):
    """Yield n equal-sized chunks from l."""
    nl = len(l)
    nchunk = nl // n
    for i in range(0, nl, nchunk):
        yield l[i:i + nchunk]

def log(*args):
    print(*args)
    stdout.flush()

tls = threading.local()

def ccp_request(path):
    url = "/" + esi_version + "/" + path + "/"
    for retries in range(max_retries):
        try:
            if retries == 1:
                sleep(reopen_timeout)
                tls.connection.close()
                tls.connection = client.HTTPSConnection(esi_endpoint)
            else:
                sleep(1.0/request_rate)
            tls.connection.request('GET', url)
            response = tls.connection.getresponse()
            if response.status == 200:
                try:
                    return json.load(response)
                except json.decoder.JSONDecodeError as e:
                    print("json error: ", e, file=stderr)
            else:
                print("bad response status: ", response.status, file=stderr)
        except client.HTTPException as e:
            print("http error: ", e.code, file=stderr)
        if retries < max_retries - 1:
            sleep(retry_timeout)
    print("fetch failed for", url, file=stderr)
    exit(1)


by_system_id = dict()
by_stargate_id = dict()
sources_destinations = list()


def worker(systems):
    global by_system_id, by_stargate_id
    tls.connection = client.HTTPSConnection(esi_endpoint)
    tls.by_system_id = dict()
    tls.by_stargate_id = dict()
    tls.sources_destinations = dict()

    for system_id in systems:
        system = ccp_request('universe/systems/' + str(system_id))
        log(system['name'])
        tls.by_system_id[system_id] = system

    for system_id, system in tls.by_system_id.items():
        destinations = list()
        if 'stargates' not in system:
            continue
        stargates = system['stargates']
        for stargate_id in stargates:
            stargate = ccp_request('universe/stargates/' + str(stargate_id))
            log(system['name'], "->", stargate_id)
            tls.by_stargate_id[stargate_id] = stargate
            destination_id = stargate['destination']['system_id']

            dest_name_req = ccp_request('universe/systems/' + str(destination_id))
            destination_name = dest_name_req['name']
            destinations.append([destination_id,destination_name])
            print(destination_id, destination_name)
        sources_destinations.append(([system_id,system['name']],destinations))

    for system_id, system in tls.by_system_id.items():
        by_system_id[system_id] = system

    for stargate_id, stargate in tls.by_stargate_id.items():
        by_stargate_id[stargate_id] = stargate

tls.connection = client.HTTPSConnection(esi_endpoint)
systems = ccp_request('universe/systems')
nsystems = len(systems)
log(nsystems, "systems")
threads = [threading.Thread(target=worker, args=(chunk,))
           for chunk in chunks(systems, nthreads)]
for t in threads:
    t.start()
for t in threads:
    t.join()

info = {'systems': by_system_id, 'stargates': by_stargate_id}
with open('eve-map.json', 'w') as dumpfile:
    json.dump(info, dumpfile)

with open('eve-sources-destinations.json', 'w') as dumpfile:
    json.dump(sources_destinations, dumpfile)
