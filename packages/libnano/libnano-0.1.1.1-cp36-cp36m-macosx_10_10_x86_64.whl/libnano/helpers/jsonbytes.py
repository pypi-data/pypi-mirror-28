'''
libnano.helpers.jsonbytes
~~~~~~~~~~~~~~~~~~~~~~~~~

Patched json loading to return dictionary with all key and value strings
as bytes objects, rather than unicode.
'''

import json
import sys
from collections import OrderedDict

if sys.version_info[0] > 2:
    STR_T = str
else:
    STR_T = unicode

def base_decode_list(data):
    local_str_t = STR_T
    res = []
    for item in data:
        if isinstance(item, local_str_t):
            item = item.encode('utf-8')
        elif isinstance(item, (tuple, list)):
            item = base_decode_list(item)
        elif isinstance(item, dict):
            item = base_decode_dict(item)
        res.append(item)
    return res
# end def

def base_decode_dict(data):
    local_str_t = STR_T
    res = {}
    for key, value in data.items():
        if isinstance(key, local_str_t):
            key = key.encode('utf-8')
        if isinstance(value, local_str_t):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = base_decode_list(value)
        elif isinstance(value, dict):
            value = base_decode_dict(value)
        res[key] = value
    return res
# end def

class BOrderedDict(OrderedDict):
    """ OrderedDict with byte strings
    """
    def __init__(self, *args, **kwds):
        super(BOrderedDict, self).__init__(*args, **kwds)

    def __setitem__(self, key, value,
                    dict_setitem=dict.__setitem__):
        global STR_T
        local_str_t = STR_T
        if isinstance(key, local_str_t):
            key = key.encode('utf-8')
        if isinstance(value, local_str_t):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            for i in range(len(value)):
                item = value[i]
                if isinstance(item, local_str_t):
                    value[i] = item.encode('utf-8')
        super(BOrderedDict, self).__setitem__(key, value, dict_setitem)
# end class

def load(fp, cls=None, parse_float=None,
          parse_int=None, parse_constant=None, ordered=False, **kw):
    return loads(fp.read(),
        cls=cls,
        parse_float=parse_float, parse_int=parse_int,
        parse_constant=parse_constant, ordered=ordered, **kw)
# end def


def loads(s, encoding=None, cls=None, parse_float=None,
          parse_int=None, parse_constant=None, ordered=False, **kw):
    if ordered:
        return json.loads(s,
            cls=cls,
            parse_float=parse_float, parse_int=parse_int,
            parse_constant=parse_constant, object_pairs_hook=BOrderedDict, **kw)
    else:
        return json.loads(s,
            cls=cls, object_hook=base_decode_dict,
            parse_float=parse_float, parse_int=parse_int,
            parse_constant=parse_constant, **kw)
# end def
