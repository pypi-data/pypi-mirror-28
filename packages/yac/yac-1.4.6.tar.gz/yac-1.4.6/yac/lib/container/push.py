#!/usr/bin/env python

from docker import Client
import docker, os, json
from api import get_docker_client

def push_image(
            image_tag,
            hub_uname,
            hub_pwd,
            hub_email,
            connection_str = "",
            registry_in="https://index.docker.io/v2"):

    print 'Getting docker client for connection_str=%s' % (connection_str)

    docker_client = get_docker_client( connection_str )

    # first login to docker registry
    docker_client.login(hub_uname,
                        password=hub_pwd,
                        email=hub_email,
                        registry=registry_in)

    # push the image
    for line in docker_client.push(image_tag, stream=True):

        line_json = json.loads(line)

        if 'stream' in line_json:
            print line_json['stream']
        else:
            print line_json




