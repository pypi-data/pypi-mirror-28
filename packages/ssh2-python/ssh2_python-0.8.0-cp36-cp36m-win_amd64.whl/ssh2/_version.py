
import json

version_json = '''
{"date": "2018-01-08T13:21:11.525399", "dirty": false, "error": null, "full-revisionid": "99dcd6fe192746a84ec5dbd8944b84251f26f152", "version": "0.8.0"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

