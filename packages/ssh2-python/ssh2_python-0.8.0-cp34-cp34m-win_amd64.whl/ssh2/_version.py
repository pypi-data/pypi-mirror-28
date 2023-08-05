
import json

version_json = '''
{"full-revisionid": "99dcd6fe192746a84ec5dbd8944b84251f26f152", "date": "2018-01-08T12:57:28.461919", "error": null, "version": "0.8.0", "dirty": false}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

