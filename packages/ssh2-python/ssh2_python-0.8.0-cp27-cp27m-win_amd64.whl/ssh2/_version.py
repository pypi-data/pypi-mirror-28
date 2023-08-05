
import json

version_json = '''
{"date": "2018-01-08T12:52:35.062000", "full-revisionid": "99dcd6fe192746a84ec5dbd8944b84251f26f152", "dirty": false, "version": "0.8.0", "error": null}'''  # END VERSION_JSON


def get_versions():
    return json.loads(version_json)

