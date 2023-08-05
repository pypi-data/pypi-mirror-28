from cfoundation import Service
from pydash import _
from os import path
import gdapi
import os
import requests
import json

class StorageService(Service):
    def remount(self, mount_path, projectName=None):
        s = self.app.services
        log = self.app.log
        rancher_url = os.environ['RANCHER_URL']
        rancher_access_key = os.environ['RANCHER_ACCESS_KEY']
        rancher_secret_key = os.environ['RANCHER_SECRET_KEY']
        client = gdapi.Client(
            url=rancher_url,
            access_key=rancher_access_key,
            secret_key=rancher_secret_key
        )
        project = None
        if (projectName):
            project = client.list_project(name=projectName)[0]
        else:
            project = client.list_project()[0]
        for volume in self.get_volumes(mount_path):
            if len(client.list_volume(name=volume).data) <= 0:
                s.rancher_service.add_volume(volume, project['id'])
                log.info('Mounted volume \'' + volume + '\'')

    def get_volumes(self, mount_path):
        volumes = []
        for file_name in os.listdir(mount_path):
            if path.isdir(path.join(mount_path, file_name)):
                volumes.append(file_name)
        return volumes
