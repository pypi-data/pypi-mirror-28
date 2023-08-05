from cfoundation import Service
import requests
import json
import os
from pydash import _

class RancherService(Service):
    def add_volume(self, name, projectId):
        rancher_url = os.environ['RANCHER_URL']
        rancher_access_key = os.environ['RANCHER_ACCESS_KEY']
        rancher_secret_key = os.environ['RANCHER_SECRET_KEY']
        r = requests.post(
            rancher_url + '/v2-beta/projects/' + projectId + '/volume',
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            data=json.dumps({
                'driver': 'rancher-nfs',
                'driverOpts': {},
                'name': name,
                'type': 'volume'
            }),
            auth=(rancher_access_key, rancher_secret_key)
        )
        if str(r.status_code)[0] != '2':
            raise Exception('Failed to create volume')
        return json.loads(r.text)
