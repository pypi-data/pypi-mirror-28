import os, urlparse, json
from yac.lib.registry import set_remote_string_w_challenge, get_remote_value, get_registry_keys
from yac.lib.registry import clear_entry_w_challenge
from yac.lib.registry import set_local_value, get_local_value, delete_local_value, get_local_keys
from yac.lib.paths import get_yac_path,get_lib_path
from yac.lib.variables import get_variable

YAC_FILE_PREFIX="yac://"

class FileError():
    def __init__(self, msg):
        self.msg = msg

def get_all_file_keys():

    file_keys = []

    # get all registry keys
    registry_keys = get_registry_keys()

    # find all keys with _naming suffix
    for key in registry_keys:

        if file_in_registry(key):
            # remove the naming part
            file_keys = file_keys + [key.replace(YAC_FILE_PREFIX,'')]

    return file_keys    

def get_file_from_registry(file_key):

    file_contents = ""

    reg_key = get_file_reg_key(file_key)

    # get file from registry
    file_contents = get_remote_value(reg_key)

    return file_contents

def clear_file_from_registry(file_path, challenge):

    # if file is in fact registered
    if get_file_from_registry(file_path):

        # clear file entry
        reg_key = get_file_reg_key(file_path)

        clear_entry_w_challenge(reg_key, challenge)      
    
    else:
        raise FileError("file with key %s doesn't exist"%file_path)

# register file into yac registry
def register_file(file_key, file_path, challenge):

    if os.path.exists(file_path):

        with open(file_path) as file_path_fp:

            file_contents = file_path_fp.read()

            reg_key = get_file_reg_key(file_key)

            # set the file in the registry
            set_remote_string_w_challenge(reg_key, file_contents, challenge)

    else:
        raise FileError("file at %s doesn't exist"%file_path)

def get_file_reg_key(file_with_path, file_namespace=""):

    file_key = file_with_path
    if file_namespace:
        file_key = os.path.join(file_namespace,file_with_path)

    # add prefix to make it easy to identify files in the registry 
    return YAC_FILE_PREFIX + file_key

def get_file_contents(file_key_or_path, servicefile_path=""):
    
    file_contents = ""

    # if file is in registry
    if file_in_registry(file_key_or_path):
        file_contents = get_remote_value(file_key_or_path)

    # if file exists locally
    elif os.path.exists(file_key_or_path):
        with open(file_key_or_path) as file_arg_fp:
            file_contents = file_arg_fp.read()

    # if file exists relative to the service descriptor
    elif os.path.exists(os.path.join(servicefile_path,file_key_or_path)):
        with open(os.path.join(servicefile_path,file_key_or_path)) as file_arg_fp:
            file_contents = file_arg_fp.read()

    return file_contents

def get_file_abs_path(file_key_or_path, servicefile_path):
    
    abs_path = ""

    # if file exists locally
    if os.path.exists(file_key_or_path):
        abs_path = os.path.dirname(os.path.abspath(file_key_or_path))

    # if file exists relative to the service descriptor
    elif os.path.exists(os.path.join(servicefile_path,file_key_or_path)):
        abs_path = os.path.dirname(os.path.join(servicefile_path,file_key_or_path))

    return abs_path    

def localize_file(file_key_or_path, servicefile_path=""):

    localized_file = ""

    # if file is in registry
    if file_in_registry(file_key_or_path):
        # convert the file to a local version
        file_contents = get_remote_value(file_key_or_path)
        localized_file = create_customization_file(file_key_or_path, file_contents)

    # if file exists locally
    elif os.path.exists(file_key_or_path):
        localized_file = file_key_or_path

    # if file exists relative to the service descriptor
    elif os.path.exists(os.path.join(servicefile_path,file_key_or_path)):
       localized_file = os.path.join(servicefile_path,file_key_or_path)

    return localized_file    

# a file is in the registry if the key includes the yac file prefix
def file_in_registry(file_key):

    to_ret = False

    if file_key and YAC_FILE_PREFIX in file_key:
        to_ret = True

    return to_ret

# a file is in yac sources if it exists in yac sources
def file_in_yac_sources(file_key):

    sources_root = get_yac_path()

    source_path = os.path.join(sources_root,file_key) 

    return os.path.exists(source_path)       

def create_customization_file(file_yac_url, file_contents=""):

    if not file_contents:
        file_contents = get_file_contents(file_yac_url)

    # yac file url's are like: yac://<netloc>/<path>
    file_parts = urlparse.urlparse(file_yac_url)

    # Write the script contents to a local file under yac/lib/customizations
    # Include the netloc path to prevent collisions with other custom scripts
    script_file_rel_path = file_parts.netloc + file_parts.path

    script_file_path = os.path.join( get_lib_path(),
                                     'customizations', 
                                     script_file_rel_path)

    # make the directory if it does not alread exist
    script_file_dir = os.path.dirname(script_file_path)
    if not os.path.exists(script_file_dir):
        os.makedirs(script_file_dir)

    # write the file
    with open(script_file_path,'w') as script_file_path_fp:
       script_file_path_fp.write(file_contents)

    return script_file_path 

def dump_dictionary(dictionary, service_name, file_name):  

    # write the dictionary to the dump path
    file_contents = json.dumps(dictionary, indent=2)

    file_path = dump_file_contents(file_contents, service_name, file_name)

    return file_path 

def dump_file_contents(file_contents, service_name, file_name):  

    dump_path = get_dump_path(service_name)

    file_path = os.path.join(dump_path,file_name)

    with open(file_path, 'w') as the_file:
        the_file.write(file_contents)

    return file_path

def get_dump_path(service_name):

    home = os.path.expanduser("~") 

    # if servicename includes a version, replace the colon separator 
    # with a slash
    service_name_cleaned = service_name.replace(":", os.sep)

    dump_path = os.path.join(home,'.yac','tmp', service_name_cleaned)

    # create the directory if it does not alread exist
    if not os.path.exists(dump_path):
        os.makedirs(dump_path)

    return dump_path   

def get_localized_script_path(script_path_arg, params):

    # if the path input is an yac url, download from the registry to a local
    # file
    if file_in_registry(script_path_arg):

        script_file_path = create_customization_file(script_path_arg)
    
    elif file_in_yac_sources(script_path_arg):
        
        script_file_path = os.path.join(get_yac_path(),script_path_arg)

    else:
        # assume the script path is local, and that path is relative to the location
        # of the service file (just like Dockerfile!)
        servicefile_path = get_variable(params,"servicefile-path")
        script_file_path = os.path.join(servicefile_path,script_path_arg)

    return script_file_path    
