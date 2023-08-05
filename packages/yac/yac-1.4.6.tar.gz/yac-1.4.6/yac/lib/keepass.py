#!/usr/bin/env python

from __future__ import print_function
import libkeepass
import sys
from yac.lib.variables import set_variable, get_variable, set_map_variable
from yac.lib.intrinsic import INSTRINSIC_ERROR_KEY, YAC_REF_ERROR, YAC_MAP_ERROR
from yac.lib.inputs import path_wizard, string_wizard
from yac.lib.cache import get_cache_value, set_cache_value_ms

class KeepassLoader():

    def __init__(self, 
                 vault_path="",
                 vault_pwd=""):

        self.vault_path = vault_path if vault_path else self.load_cached_vault_path()
        self.vault_pwd = vault_pwd if vault_pwd else self.load_cached_vault_pwd()

        self.error = ""
        self.ready = False
        try:
            with libkeepass.open(self.vault_path, password=self.vault_pwd) as kdb_generator:

                self.kdb = kdb_generator.obj_root
                self.ready = True

        except Exception as e:
            self.error = 'Could not load KeePass database %s:\n%s' % (vault_path, str(e))
    
            # if vault were not passed as constructor arg (and were thus pulled from cache)
            # clear cache
            if (not vault_path and 
                not vault_pwd):
                # clear caches
                self.clear_secrets_cache()

    def is_ready(self):
        return self.ready

    def get_load_errors(self):
        return self.error

    def load_secrets(self, secrets, service_params):

        for secret in secrets:

            if ('source' in secrets[secret] and 
                'keepass' in secrets[secret]['source'] and 
                'lookup' not in secrets[secret]):

                secret_value = self.find_secret_value(secrets[secret]['value']['group'],
                                                      secrets[secret]['value']['title'],
                                                      secrets[secret]['value']['field'])

                if secret_value:
                    # load secret as a parameters
                    set_variable(service_params,secret,secret_value,secrets[secret]['comment'])

                else:
                    # lookup failed. add to list of reference errors
                    setpoint = '%s: %s keepass secret lookup miss'%(YAC_REF_ERROR,secret)
                    error_list = get_variable(service_params,INSTRINSIC_ERROR_KEY,[])
                    set_variable(service_params,INSTRINSIC_ERROR_KEY,error_list+[setpoint])

            elif ('source' in secrets[secret] and
                  'keepass' in secrets[secret]['source'] and 
                  'lookup'  in secrets[secret]):

                # add map to params
                service_params.update({secret:secrets[secret]})

                # secrets are part of a map, so get each setpoint
                for setpoint in secrets[secret]['value']:

                    secret_value = self.find_secret_value(secrets[secret]['value'][setpoint]['group'],
                                                          secrets[secret]['value'][setpoint]['title'],
                                                          secrets[secret]['value'][setpoint]['field'])

                    if secret_value:
                        # load secret as a parameters
                        set_map_variable(service_params, secret, setpoint, secret_value)
                    else:
                        # lookup failed. add to list of reference errors
                        setpoint = '%s: %s keepass secret map lookup miss'%(YAC_MAP_ERROR,secret)
                        error_list = get_variable(service_params,INSTRINSIC_ERROR_KEY,[])
                        set_variable(service_params,INSTRINSIC_ERROR_KEY,error_list+[setpoint])
              

    def find_secret_value(self, group_name, secret_title, entry_field):

        secret_value = ""

        for group in self.kdb.findall('.//Group'):
            group_title = group.find('./Name').text
            if group_title == group_name:
                for entry in group.findall('.//Entry'):
                    kv = {string.find('./Key').text : string.find('./Value').text for string in entry.findall('./String')}
                    if kv['Title'] == secret_title:
                        secret_value = kv[entry_field]
                        break

        return secret_value

    def load_cached_vault_path(self):

        vault_path = get_cache_value('keepass-vault-path')

        if not vault_path:
            vault_path = path_wizard("KeePass Vault Path", 
                                    "Path to the KeePass vault file for secrets lookup", 
                                    [], 
                                    True)

            set_cache_value_ms('keepass-vault-path',vault_path)
        
        return vault_path

        
    def load_cached_vault_pwd(self):

        vault_pwd = get_cache_value('keepass-vault-pwd')

        if not vault_pwd:
            vault_pwd = string_wizard("KeePass Vault Password", 
                                      "The master key for the KeePass vault", 
                                      [], 
                                      True)
            set_cache_value_ms('keepass-vault-pwd', vault_pwd)
        
        return vault_pwd

    def clear_secrets_cache(self):
        set_cache_value_ms('keepass-vault-path',"")
        set_cache_value_ms('keepass-vault-pwd', "") 
