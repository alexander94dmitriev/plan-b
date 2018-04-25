# Copyright © 2018 Po Huit
# [This program is licensed under the "MIT License"]
# Please see the file LICENSE in the source
# distribution of this software for license terms.

from time import sleep
import json
from esipy import EsiApp

from esipy.cache import FileCache
cache = FileCache(path=".cache")

# App.create(url, strict=True)
# with url = the swagger spec URL, leave strict to default
app = EsiApp(
    cache=cache,
    cache_time=None,
    url="http://esi.tech.ccp.is/latest/swagger.json?datasource=tranquility",
)
app = app.get_latest_swagger

from esipy import EsiClient

# basic client, for public endpoints only
client = EsiClient(
    retry_requests=True,  # set to retry on http 5xx error (default False)
    header={'User-Agent': 'eve.edward.teachya@gmail.com'},
    raw_body_only=False,  # default False, set to True to never parse response and only return raw JSON string content.
    cache=cache,
    cache_time=None,
)

class System(object):
    def __init__(self, system_id, name, stargate_ids):
        self.system_id = system_id
        self.name = name
        self.stargate_ids = stargate_ids

    def __repr__(self):
        stargates = ",".join([str(id) for id in self.stargate_ids])
        return 'system_id=' + str(self.system_id) + "," + \
            'name=' + str(self.name) + "," + \
            'stargate_ids=[' + stargates + "]"

by_system_id = dict()

systems_req = app.op['get_universe_systems']()
systems = client.request(systems_req).data
print(len(systems), "systems")
for system_id in systems:
    system_req = app.op['get_universe_systems_system_id'](system_id=system_id)
    system_data = client.request(system_req).data
    if 'stargates' not in system_data:
        print(system_data['name'] + '*')
        continue
    stargates = system_data['stargates']
    system_desc = System(system_id, system_data['name'], stargates)
    print(system_desc)
    by_system_id[system_id] = system_data
    sleep(1.0/30.0)

by_stargate_id = dict()

for system_id, system_data in by_system_id.items():
    for stargate in system_data['stargates']:
        sg_req = app.op['get_universe_stargates_stargate_id'](stargate_id=stargate)
        sg = client.request(sg_req).data
        dst_id = sg['destination']['system_id']
        dst = by_system_id[dst_id]
        print(system_data.name, '->', dst['name'])
        by_stargate_id[sg['stargate_id']] = sg
        sleep(1.0/30.0)

info = {'systems': by_system_id, 'stargates': by_stargate_id}
with open('eve-map.json', 'w') as dumpfile:
    json.dump(info, dumpfile)
