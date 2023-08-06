import os
import sys

sys.path.insert(0, os.getcwd())

import json
import requests
from pact_test import *


def steak(type):
    out = requests.post(
        'http://localhost:9999/steaks/',
        data=json.dumps({'cooking': type}),
        headers={'content-type': 'application/json', 'spam': 'eggs'}
    )
    return out.json() if out.status_code == 201 else out


@service_consumer('SousChef')
@has_pact_with('Grill Chef')
class GrillChefTest(ServiceProviderTest):

    @given('steaks are available')
    @upon_receiving('a request for a steak well-done')
    @with_request({'method': 'POST', 'path': '/steaks/', 'body': {'cooking': 'well-done'}, 'headers': [{'spam': 'eggs'}]})
    @will_respond_with({'status': 422, 'headers': [{'spam': 'eggs'}], 'body': {'reason': 'we do not serve well-done steaks'}})
    def test_steak_well_done(self):
        response = steak('well-done')
        assert response.status_code == 422
