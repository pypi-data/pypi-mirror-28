# yac variables are stored as:
# 
#{
#    "variable-name": {
#        "comment": "variable explanation",
#        "value":   "variable value"
#    }   
#}
# 

def get_variable(params, variable_name, default_value="", value_key='value'):

    if variable_name in params and value_key in params[variable_name]:
        return params[variable_name][value_key]
    else:
        return default_value

def get_variable_comment(params, variable_name):

    if variable_name in params and 'comment' in params[variable_name]:
        return params[variable_name]['comment']
    else:
        return ""

def set_variable(params, variable_name, value, comment="", value_key='value'):

    params[variable_name] = {value_key : value, 'comment': comment}

# yac maps are stored as:
# 
#{
#    "my-map": {
#        "comment":      "map explanation",
#        "lookup":       "my-lookup-param",
#        "value": {
#            "param_val1":   "value for the val1 setpoint of another param",
#            "param_val2":   "value for the val2 setpoint of another param"
#        }
#    }
#}
#
# where, the param used in the map lookup could look like
#{
#    "my-lookup-param": {
#        "comment": "variable explanation",
#        "value":   "param_val1"
#    }   
#}
#
#
# this map could be referenced in a servicefiles as:
# ...
#    "SomeJsonKey" : { "yac-map" : ["my-map", "my-lookup-param"] }
# ...

def get_map_variable(params, map_name, param_key, default_value="", value_key='value'):

    # the param value associated with the param key is used
    # in the map lookup
    param_val = get_variable(params,param_key,"")

    if ( param_val and 
         (map_name in params) and 
         (value_key in params[map_name]) and
         param_val in params[map_name][value_key]):
        return params[map_name][value_key][param_val]
    else:
        return default_value    

def set_map_variable(params, map_name, map_key, value, value_key='value'):


    if ( map_name in params and 
         value_key in params[map_name] and
         map_key in params[map_name][value_key]):

        params[map_name][value_key][map_key] = value
