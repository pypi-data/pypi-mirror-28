#!/usr/bin/env python

import argparse, jmespath, shutil, os
from yac.lib.naming import get_stack_name, set_namer
from yac.lib.service import get_service, get_service_parmeters, get_service_alias
from yac.lib.stack import get_stack_templates, get_stack_name, get_ec2_ips, deploy_stack_files
from yac.lib.vpc import get_vpc_prefs
from yac.lib.container.api import get_connection_str
from yac.lib.container.build import build_image, get_image_name, get_rendered_dockerpath
from yac.lib.template import apply_templates_in_dir
from yac.lib.container.config import get_aliases, find_image_tag
from yac.lib.params import get_service_params, NULL_PARAMS, INVALID_PARAMS

def main():
    
    parser = argparse.ArgumentParser(description='Build image for a service container unto a stack host.')     

    # required args   
    parser.add_argument('servicefile', help='location of the Servicefile (registry key or abspath)')
    parser.add_argument('name',        help='name of container to build')

    parser.add_argument('buildpath',   help='path to the dockerfile') 
        
    parser.add_argument('-d','--dryrun',  help='dry run the container start by printing rendered template to stdout', 
                                          action='store_true')   
    parser.add_argument('-a',
                        '--alias',  help='service alias for the stack currently supporting this service (deault alias is per Servicefile)')     
    parser.add_argument('-p',
                        '--params',  help='path to a file containing additional, static, service parameters (e.g. vpc params, of service constants)') 
    parser.add_argument('--public',     help='connect using public IP address', 
                                        action='store_true') 
                                            
    # pull out args
    args = parser.parse_args()

    # determine service defintion, complete service name, and service alias based on the args
    service_descriptor, service_name, servicefile_path = get_service(args.servicefile)

    # get vpc preferences in place
    vpc_prefs = get_vpc_prefs()

    # set the resource namer to use with this service
    set_namer(service_descriptor, servicefile_path, vpc_prefs)

    # get the alias to use with this service
    service_alias = get_service_alias(service_descriptor,args.alias)

    # determine service params based on the params arg
    service_params_input, service_params_name = get_service_params(args.params)

    # abort if service params were not loaded successfully
    if args.params and service_params_name == NULL_PARAMS:
        print("The service params specified do not exist locally or in registry. Please try again.")
        exit()
    elif service_params_name == INVALID_PARAMS:
        print("The service params file specified failed validation checks. Please try again.")
        exit()
        
    # get the service parameters for use with yac-ref's in service templates
    service_parmeters = get_service_parmeters(service_alias, service_params_input, 
                                              service_name, service_descriptor,
                                              servicefile_path, vpc_prefs)

    # get cloud formation template for the service requested and apply yac intrinsic 
    # functions (yac-ref, etc.) using  the service_parmeters
    stack_template = get_stack_templates(service_descriptor,
                                         service_parmeters)

    image_tag = find_image_tag(args.name,stack_template)

    # get stack name
    stack_name = get_stack_name(service_parmeters)

    # replace any service parmeters variables in body of any files
    build_path = get_rendered_dockerpath(image_tag) 
    if os.path.exists(build_path):
        shutil.rmtree(build_path)

    apply_templates_in_dir(args.buildpath, service_parmeters, build_path)

    # get the ip address of the target host
    target_host_ips = get_ec2_ips( stack_name , "", args.public)

    if args.dryrun:

        user_msg = "%s(dry-run) Building the %s container image on %s using the rendered dockerfile at %s%s"%('\033[92m',
                                                        image_tag,
                                                        target_host_ips,
                                                        build_path,                                                    
                                                        '\033[0m')
        print user_msg


    else:

        # build the container image on each host ...
        for target_host_ip in target_host_ips:

            user_msg = "%sBuilding the %s container image on %s using the rendered dockerfile at %s%s"%('\033[92m',
                                                        image_tag,
                                                        target_host_ip,
                                                        build_path,                                                    
                                                        '\033[0m')

            raw_input(user_msg + "\nHit <enter> to continue..." )

            # get connection string for the docker remote api on the target host
            docker_api_conn_str = get_connection_str( target_host_ip )

            # build the image
            build_image( image_tag, build_path, docker_api_conn_str )
