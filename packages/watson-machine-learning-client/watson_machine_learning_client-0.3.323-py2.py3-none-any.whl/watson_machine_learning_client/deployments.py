################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

import requests
import json
from .utils import get_headers, get_artifact_uid
from .wml_client_error import WMLClientError, MissingValue, ApiRequestFailure, NotUrlNorUID
from .href_definitions import is_uid, is_url
from .wml_resource import WMLResource


class Deployments(WMLResource):
    """
        Deploy and score published models.
    """
    def __init__(self, client, wml_credentials, wml_token, instance_details):
        WMLResource.__init__(self, __name__, client, wml_credentials, wml_token, instance_details)

    def _get_url_for_uid(self, deployment_uid):
        response_get = requests.get(
            self._href_definitions.get_deployments_href(),
            headers=get_headers(self._wml_token))

        try:
            if response_get.status_code == 200:
                for el in json.loads(response_get.text).get('resources'):
                    if el.get('metadata').get('guid') == deployment_uid:
                        return el.get('metadata').get('url')
            else:
                raise ApiRequestFailure('Couldn\'t generate url from uid: \'{}\'.'.format(deployment_uid), response_get)
        except Exception as e:
            raise WMLClientError('Failed during getting url for uid: \'{}\'.'.format(deployment_uid), e)

        raise WMLClientError('No matching url for uid: \'{}\'.'.format(deployment_uid))

    def get_details(self, deployment_uid=None, deployment_url=None):
        """
           Get information about your deployment(s).

           Args:
               deployment_uid (str):  Deployment UID (optional).
               deployment_url (str):  Deployment URL (optional).

           Returns:
               deployment_details (dict) - metadata of deployment(s).

           A way you might use me is

            >>> deployment_details = client.deployments.get_details(deployment_url=deployment_url)
            >>> deployment_details = client.deployments.get_details(deployment_uid)
            >>> deployment_details = client.deployments.get_details(deployment_uid=deployment_uid)
            >>> deployments_details = client.deployments.get_details()
        """
        Deployments._validate_type(deployment_uid, 'deployment_uid', str, False)
        Deployments._validate_type(deployment_url, 'deployment_url', str, False)

        if deployment_url is not None and not is_url(deployment_url):
            raise WMLClientError('\'deployment_url\' is not an url: \'{}\''.format(deployment_url))

        if deployment_uid is not None and not is_uid(deployment_uid):
            raise WMLClientError('\'deployment_uid\' is not an uid: \'{}\''.format(deployment_uid))
        elif deployment_uid is not None:
            deployment_url = self._get_url_for_uid(deployment_uid)

        if deployment_url is None and deployment_uid is None:
            deployment_url = self._instance_details.get('entity').get('deployments').get('url')

        response_get = requests.get(
            deployment_url,
            headers=get_headers(self._wml_token))

        return self._handle_response(200, 'getting deployment(s) details', response_get)

    def create(self, name, description='Model deployment', model_uid=None, model_url=None):
        """
            Create model deployment (online). Either model_uid or model_url must be specified.

            Args:
                model_uid (string):  Published model UID (optional).

                model_url (string):  Published model URL (optional).

                name (string): Deployment name.

                description (string): Deployment description.

            Returns:
                deployment (dict) - details of created deployment.

            A way you might use me is

             >>> deployment = client.deployments.create("Deployment X", "Online deployment of XYZ model.", model_uid)
             >>> deployment = client.deployments.create("Deployment X", "Online deployment of XYZ model.", model_uid=model_uid)
             >>> deployment = client.deployments.create("Deployment X", "Online deployment of XYZ model.", model_url=model_url)
         """
        Deployments._validate_type(name, 'name', str, True)
        Deployments._validate_type(description, 'description', str, True)
        Deployments._validate_type(model_uid, 'model_uid', str, False)
        Deployments._validate_type(model_url, 'model_url', str, False)

        model_uid = get_artifact_uid(model_uid, model_url)

        response_online = requests.post(
            self._instance_details.
            get('entity').
            get('published_models').
            get('url') + "/" + model_uid + "/" + "deployments",
            json={'name': name, 'description': description, 'type': 'online'},
            headers=get_headers(self._wml_token))

        return self._handle_response(201, 'deployment creation', response_online)

    @staticmethod
    def get_scoring_url(deployment):
        """
            Get scoring_url from deployment details.

            Args:
                deployment (dict):  Created deployment details.

            Returns:
                scoring_url (string) - scoring endpoint URL that is used for making scoring requests.

            A way you might use me is

             >>> scoring_endpoint = client.deployments.get_scoring_url(deployment)
        """
        Deployments._validate_type(deployment, 'deployment', dict, True)

        try:
            url = deployment.get('entity').get('scoring_url')
        except Exception as e:
            raise WMLClientError('Getting scoring url for deployment failed.', e)

        if url is None:
            raise MissingValue('entity.scoring_url')

        return url

    @staticmethod
    def get_deployment_uid(deployment_details):
        """
            Get deployment_uid from deployment details.

            Args:
               deployment_details (dict):  Created deployment details.

            Returns:
               deployment_uid (str) - deployment UID that is used to manage the deployment

               A way you might use me is

            >>> scoring_endpoint = client.deployments.get_deployment_uid(deployment)
        """
        Deployments._validate_type(deployment_details, 'deployment_details', dict, True)

        try:
            uid = deployment_details.get('metadata').get('guid')
        except Exception as e:
            raise WMLClientError('Getting deployment uid from deployment details failed.', e)

        if uid is None:
            raise MissingValue('deployment_details.metadata.guid')

        return uid

    @staticmethod
    def get_deployment_url(deployment_details):
        """
            Get deployment_url from deployment details.

            Args:
               deployment_details (dict):  Created deployment details.

            Returns:
               deployment_url (str) - deployment URL that is used to manage the deployment

               A way you might use me is

            >>> scoring_endpoint = client.deployments.get_deployment_url(deployment)
        """
        Deployments._validate_type(deployment_details, 'deployment_details', dict, True)

        try:
            url = deployment_details.get('metadata').get('url')
        except Exception as e:
            raise WMLClientError('Getting deployment url from deployment details failed.', e)

        if url is None:
            raise MissingValue('deployment_details.metadata.url')

        return url

    def delete(self, deployment_uid=None, deployment_url=None):
        """
            Delete model deployment. Either deployment_uid or deployment_url must be specified.

            Args:
                deployment_uid (str):  Deployment UID (optional).
                deployment_url (str):  Deployment URL (optional).

            A way you might use me is

            >>> client.deployments.delete(deployment_url=deployment_url)
            >>> client.deployments.delete(deployment_uid)
            >>> client.deployments.delete(deployment_uid=deployment_uid)
        """
        Deployments._validate_type(deployment_uid, 'deployment_uid', str, False)
        Deployments._validate_type(deployment_url, 'deployment_url', str, False)

        if deployment_url is not None and not is_url(deployment_url):
            raise WMLClientError('\'deployment_url\' is not an url: \'{}\''.format(deployment_url))

        if deployment_uid is not None and not is_uid(deployment_uid):
            raise WMLClientError('\'deployment_uid\' is not an uid: \'{}\''.format(deployment_uid))
        elif deployment_uid is not None:
            deployment_url = self._get_url_for_uid(deployment_uid)

        if deployment_url is None and deployment_uid is None:
            raise WMLClientError('Both deployment_url and deployment_uid are empty.')

        response_delete = requests.delete(
            deployment_url,
            headers=get_headers(self._wml_token))

        self._handle_response(204, 'deployment deletion', response_delete, False)

    def score(self, scoring_url, payload):
        """
            Make scoring requests against deployed model.

              Args:
                 scoring_url (str):  scoring endpoint URL.

                 payload (dict): records to score.

              Returns:
                  scoring result (dict) - scoring result containing prediction and probability.

              A way you might use me is

              >>> scoring_payload = {"fields": ["GENDER","AGE","MARITAL_STATUS","PROFESSION"],
              "values": [["M",23,"Single","Student"],["M",55,"Single","Executive"]]}
              >>> predictions = client.deployments.score(scoring_url, scoring_payload)
        """
        Deployments._validate_type(scoring_url, 'scoring_url', str, True)
        Deployments._validate_type(payload, 'payload', dict, True)

        response_scoring = requests.post(
            scoring_url,
            json=payload,
            headers=get_headers(self._wml_token))

        return self._handle_response(200, 'scoring', response_scoring)

    def list(self):
        """
           List deployments.

           A way you might use me is

           >>> client.deployments.list()
        """
        from tabulate import tabulate

        details = self.get_details()
        resources = details['resources']
        values = [(m['metadata']['guid'], m['entity']['name'], m['entity']['type'], m['metadata']['created_at'], m['entity']['model_type']) for m in resources]
        table = tabulate([["GUID", "NAME", "TYPE", "CREATED", "FRAMEWORK"]] + values)
        print(table)
