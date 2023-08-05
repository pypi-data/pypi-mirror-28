################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

from .wml_client_error import ApiRequestFailure, WMLClientError
from .href_definitions import is_uid, is_url, HrefDefinitions


def get_ml_token(watson_ml_creds):
    import requests
    import json

    if 'ml_token' not in watson_ml_creds:
        response = requests.get(HrefDefinitions(watson_ml_creds).get_token_endpoint_href(), auth=(watson_ml_creds['username'], watson_ml_creds['password']))
        if response.status_code == 200:
            watson_ml_creds['ml_token'] = json.loads(response.text).get('token')
        else:
            raise ApiRequestFailure("Error during getting ML Token.", response)
    return watson_ml_creds['ml_token']


def get_headers(wml_token):
    return {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + wml_token}


def artifact_url_to_uid(artifact_url):
    uid = artifact_url.split("/")[-1]
    if is_uid(uid):
        return uid
    else:
        raise WMLClientError('Failure during getting uid from url, invalid uid: \'{}\''.format(uid))


def get_artifact_uid(artifact_uid, artifact_url, mandatory=True):
    if artifact_uid is not None and is_uid(artifact_uid):
        return artifact_uid
    elif artifact_uid is not None:
        raise WMLClientError('Invalid uid: \'{}\'.'.format(artifact_uid))

    if artifact_url is not None and is_url(artifact_url):
        return artifact_url_to_uid(artifact_url)
    elif artifact_url is not None:
        raise WMLClientError('Passed url is not valid: \'{}\'.'.format(artifact_url))

    if mandatory:
        raise WMLClientError('Both uid and url are empty.')
    else:
        return None
