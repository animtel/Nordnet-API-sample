import json
import logging

from Helpers.MappingHelper import to_dynamic


def try_parse_into_json(string):
    """
    Try parsing the string into JSON objects. Return the unparsable
    parts as buffer
    """
    json_strings = string.split('\n')

    for i in range(0, len(json_strings)):
        try:
            json_data = json.loads(json_strings[i])
            logging.info(">> JSON udpates from public feed")
            logging.info(json.dumps(json_data, indent=4, sort_keys=True))
            print(">> JSON udpates from public feed")
            print(json.dumps(json_data, indent=4, sort_keys=True))
        except:
            ## If this part cannot be parsed into JSON, It's probably not
            ## complete. Stop it right here. Merge the rest of list and
            ## return it, parse it next time
            return ''.join(json_strings[i:])

    ## If all JSONs are successfully parsed, we return an empty buffer
    return ''
