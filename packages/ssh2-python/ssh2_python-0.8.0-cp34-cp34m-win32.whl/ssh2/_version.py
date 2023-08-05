
import json

version_json = '''
{"date": "2018-01-08T12:54:30.162504", "error": null, "dirty": false, "version": "0.8.0", "full-revisionid": "99dcd6fe192746a84ec5dbd8944b84251f26f152"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

