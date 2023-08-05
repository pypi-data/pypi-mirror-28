#!/usr/bin/env python

import jmespath

from yac.lib.keepass import KeepassLoader

REQUIRED_FIELDS = ["service-secrets.secrets",
                   "service-secrets.*.value"]

# load secrets from secrets sources into service params
def load_secrets(service_parmeters, service_secrets):

    sources = jmespath.search("secrets.*.source",service_secrets)

    if 'keepass' in sources:

        # load secrets from keepass into the service params
        print "loading secrets from KeePass vault"

        loader = KeepassLoader()
        loader.load_secrets(service_secrets['secrets'],
                            service_parmeters)

# TODO: integrate this into service validation so users get helful 
# validation errors during pre-processing of their servicefile
def validate_secrets(service_secrets):

    validation_errors = ""

    service_secrets_copy = service_secrets.deepcopy()

    for required_field in REQUIRED_FIELDS:
        field = jmespath(required_field,service_secrets)

        if not field:
            validation_errors = (validation_errors +
                                 "%s is a required service-secrets field.")
