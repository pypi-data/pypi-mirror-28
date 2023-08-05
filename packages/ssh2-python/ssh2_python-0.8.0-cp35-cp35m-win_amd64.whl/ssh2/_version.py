
import json

version_json = '''
{"full-revisionid": "99dcd6fe192746a84ec5dbd8944b84251f26f152", "dirty": false, "date": "2018-01-08T13:07:02.786167", "error": null, "version": "0.8.0"}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

