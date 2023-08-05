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
import re
from .utils import get_headers
import time
import tqdm
from .metanames import TrainingConfigurationMetaNames
import sys
from .wml_client_error import WMLClientError
from .href_definitions import is_uid, is_url
from .wml_resource import WMLResource


class Training(WMLResource):
    """
       Train new models.
    """

    def __init__(self, client, wml_credentials, wml_token, instance_details):
        WMLResource.__init__(self, __name__, client, wml_credentials, wml_token, instance_details)
        self._base_models_url = wml_credentials['url'] + "/v3/models"
        self.ConfigurationMetaNames = TrainingConfigurationMetaNames()

    @staticmethod
    def _is_training_uid(s):
        res = re.match('training\-[a-zA-Z0-9\-\_]+', s)
        return res is not None

    @staticmethod
    def _is_training_url(s):
        res = re.match('\/v3\/models\/training\-[a-zA-Z0-9\-\_]+', s)
        return res is not None

    @staticmethod
    def _artifact_url_to_uid(artifact_url):
        uid = artifact_url.split("/")[-1]
        if Training._is_training_uid(uid):
            return uid
        else:
            raise WMLClientError('Failure during getting uid from url, invalid uid: \'{}\''.format(uid))

    @staticmethod
    def _get_artifact_uid(artifact_uid, artifact_url, mandatory=True):
        if artifact_uid is not None and Training._is_training_uid(artifact_uid):
            return artifact_uid
        elif artifact_uid is not None:
            raise WMLClientError('Invalid uid: \'{}\'.'.format(artifact_uid))

        if artifact_url is not None and Training._is_training_url(artifact_url):
            return Training._artifact_url_to_uid(artifact_url)
        elif artifact_url is not None:
            raise WMLClientError('Passed url is not valid: \'{}\'.'.format(artifact_url))

        if mandatory:
            raise WMLClientError('Both uid and url are empty.')
        else:
            return None

    # def get_frameworks(self):
    #     """
    #        Get list of supported frameworks.
    #
    #        Returns:
    #            json - supported frameworks for training.
    #
    #        A way you might use me is
    #
    #        >>> model_details = client.training.get_frameworks()
    #     """
    #
    #     response_get = requests.get(self._base_models_url + "/frameworks", headers=get_headers(self._wml_token))
    #
    #     if response_get.status_code == 200:
    #         return json.loads(response_get.text)
    #     else:
    #         error_msg = 'Getting supported frameworks failed.' + '\n' + "Error msg: " + response_get.text
    #         print(error_msg)
    #         return None

    def get_status(self, run_uid=None, run_url=None):
        """
              Get training status.

              run_uid (str): ID of trained model (optional).
              run_url (str): URL of trained model (optional).

              Returns:
                  status (dict) - training run status.

              A way you might use me is

              >>> training_status = client.training.get_status(run_uid)
              >>> training_status = client.training.get_status(run_uid=run_uid)
              >>> training_status = client.training.get_status(run_url=run_url)
        """
        Training._validate_type(run_uid, 'run_uid', str, False)
        Training._validate_type(run_url, 'run_url', str, False)

        run_uid = Training._get_artifact_uid(run_uid, run_url, False)

        details = self.get_details(run_uid)

        if details is not None:
            return WMLResource._get_required_element_from_dict(details, 'details', ['entity', 'status'])
        else:
            raise WMLClientError('Getting trained model status failed. Unable to get model details for run_uid: \'{}\'.'.format(run_uid))

    def get_details(self, run_uid=None, run_url=None):
        """
              Get trained model details.

              Args:
                  run_uid (str): ID of trained model (optional, if not provided all runs details are returned).
                  run_url (str): URL of trained model (optional, if not provided all runs details are returned).

              Returns:
                  details (dict) - training run(s) details.

              A way you might use me is

              >>> trained_model_details = client.training.get_details(run_uid)
              >>> trained_model_details = client.training.get_details(run_uid=run_uid)
              >>> trained_models_details = client.training.get_details()
              >>> trained_model_details = client.training.get_details(run_url=run_url)
        """
        Training._validate_type(run_uid, 'run_uid', str, False)
        Training._validate_type(run_url, 'run_url', str, False)

        run_uid = Training._get_artifact_uid(run_uid, run_url, False)

        if run_uid is None:
            response_get = requests.get(self._base_models_url, headers=get_headers(self._wml_token))

            return self._handle_response(200, 'getting trained models details', response_get)
        else:
            get_details_endpoint = '{}/v3/models/'.format(self._wml_credentials['url']) + run_uid
            model_training_details = requests.get(get_details_endpoint, headers=get_headers(self._wml_token))

            return self._handle_response(200, 'getting trained models details', model_training_details)

    @staticmethod
    def get_run_url(run_details):
        """
            Get training run url from training run details.

            Args:
               run_details (dict):  Created training run details.

            Returns:
               run_url (str) - training run URL that is used to manage the training

               A way you might use me is

            >>> run_url = client.training.get_run_url(run_details)
        """
        Training._validate_type(run_details, 'run_details', object, True)
        return WMLResource._get_required_element_from_dict(run_details, 'run_details', ['metadata', 'url'])

    @staticmethod
    def get_run_uid(run_details):
        """
            Get uid of training run.

            Args:
                run_details (dict):  training run details.

            Returns:
                uid (str) - uid of training run.

            A way you might use me is

            >>> model_uid = client.training.get_run_uid(run_details)
        """
        Training._validate_type(run_details, 'run_details', object, True)
        return WMLResource._get_required_element_from_dict(run_details, 'run_details', ['metadata', 'guid'])

    def cancel(self, run_uid=None, run_url=None):
        """
              Cancel model training.

              Args:
                  run_uid (str): ID of trained model (optional).
                  run_url (str): URL of trained model (optional).

              A way you might use me is

              >>> client.training.cancel(run_uid)
              >>> client.training.cancel(run_uid=run_uid)
              >>> client.training.cancel(run_url=run_url)
        """
        Training._validate_type(run_uid, 'run_uid', str, False)
        Training._validate_type(run_url, 'run_url', str, False)

        run_uid = Training._get_artifact_uid(run_uid, run_url, True)

        patch_endpoint = self._base_models_url + '/' + str(run_uid)
        patch_payload = [
            {
                "op": "replace",
                "path": "/status/state",
                "value": "canceled"
            }
        ]

        response_patch = requests.patch(patch_endpoint, json=patch_payload, headers=get_headers(self._wml_token))

        self._handle_response(204, 'model training cancel', response_patch, False)
        return

    def run(self, meta_props, asynchronous=True, definition_uid=None, definition_url=None):
        """
           Train new model.
            Args:
               definition_uid (str): uid to saved model_definition/pipeline (optional).

               definition_url (str): url to saved model_definition/pipeline (optional).

               meta_props (dict): meta data of the training configuration. To see available meta names use:
               >>> client.training.ConfigurationMetaNames.show()

               asynchronous (bool): Default True means that training job is submitted and progress can be checked later.
               False - method will wait till job completion and print training stats.

           Returns:
               run_details (dict) - training run details.

           A way you might use me is

           >>> metadata = {
           >>>  client.training.ConfigurationMetaNames.NAME: "Hand-written Digit Recognition",
           >>>  client.training.ConfigurationMetaNames.AUTHOR_NAME: "John Smith",
           >>>  client.training.ConfigurationMetaNames.AUTHOR_EMAI: "JohnSmith@js.com",
           >>>  client.training.ConfigurationMetaNames.DESCRIPTION: "Hand-written Digit Recognition training",
           >>>  client.training.ConfigurationMetaNames.FRAMEWORK_NAME: "tensorflow",
           >>>  client.training.ConfigurationMetaNames.FRAMEWORK_VERSION: "1.2-py3",
           >>>  client.training.ConfigurationMetaNames.EXECUTION_COMMAND: "python3 convolutional_network.py --trainImagesFile ${DATA_DIR}/train-images-idx3-ubyte.gz --trainLabelsFile ${DATA_DIR}/train-labels-idx1-ubyte.gz --testImagesFile ${DATA_DIR}/t10k-images-idx3-ubyte.gz --testLabelsFile ${DATA_DIR}/t10k-labels-idx1-ubyte.gz --learningRate 0.001 --trainingIters 1000",
           >>>  client.training.ConfigurationMetaNames.EXECUTION_RESOURCE_SIZE: "small",
           >>>  client.training.ConfigurationMetaNames.TRAINING_DATA_REFERENCE: {
           >>>          "connection": {
           >>>              "endpoint_url": "https://s3-api.us-geo.objectstorage.service.networklayer.com",
           >>>              "aws_access_key_id": "***",
           >>>              "aws_secret_access_key": "***"
           >>>          },
           >>>          "source": {
           >>>              "container": "wml-dev",
           >>>          }
           >>>          "type": "s3_datastore"
           >>>      }
           >>> client.training.ConfigurationMetaNames.TRAINING_RESULTS_REFERENCE: {
           >>>          "connection": {
           >>>              "endpoint_url": "https://s3-api.us-geo.objectstorage.service.networklayer.com",
           >>>              "aws_access_key_id": "***",
           >>>              "aws_secret_access_key": "***"
           >>>          },
           >>>          "source": {
           >>>              "container": "wml-dev-results",
           >>>          }
           >>>          "type": "s3_datastore"
           >>>      },
           >>> }
           >>> run_details = client.training.run(definition_url=definition_url, meta_props=metadata)
           >>> run_uid = client.training.get_run_uid(run_details)
        """
        Training._validate_type(meta_props, 'meta_props', object, True)
        Training._validate_type(asynchronous, 'asynchronous', bool, True)
        Training._validate_type(definition_uid, 'definition_uid', str, False)
        Training._validate_type(definition_url, 'definition_url', str, False)

        if definition_url is None:
            if definition_uid is not None and is_uid(definition_uid):
                definition_url = self._href_definitions.get_definition_href(definition_uid)
            elif definition_uid is not None:
                raise WMLClientError('Invalid uid: \'{}\'.'.format(definition_uid))
            else:
                raise WMLClientError('Both uid and url are empty.')
        elif not is_url(definition_url):
            raise WMLClientError('Passed url is not valid: \'{}\'.'.format(definition_url))

        training_configuration_metadata = {
            "model_definition": {
                "framework": {
                    "name": meta_props[self.ConfigurationMetaNames.FRAMEWORK_NAME],
                    "version": meta_props[self.ConfigurationMetaNames.FRAMEWORK_VERSION]
                },
                "name": meta_props[self.ConfigurationMetaNames.NAME],
                "author": {
                    "name": meta_props[self.ConfigurationMetaNames.AUTHOR_NAME],
                    "email": meta_props[self.ConfigurationMetaNames.AUTHOR_EMAIL]
                },
                "description": meta_props[self.ConfigurationMetaNames.DESCRIPTION],
                "definition_href": definition_url,
                "execution": {
                    "command": meta_props[self.ConfigurationMetaNames.EXECUTION_COMMAND],
                    "resource": meta_props[self.ConfigurationMetaNames.EXECUTION_RESOURCE_SIZE]
                }
            },
            "training_data_reference": meta_props[self.ConfigurationMetaNames.TRAINING_DATA_REFERENCE],
            "training_results_reference": meta_props[self.ConfigurationMetaNames.TRAINING_RESULTS_REFERENCE]
        }

        train_endpoint = '{}/v3/models'.format(self._wml_credentials['url'])

        response_train_post = requests.post(train_endpoint, json=training_configuration_metadata,
                                            headers=get_headers(self._wml_token))

        run_details = self._handle_response(202, 'training', response_train_post)

        trained_model_guid = self.get_run_uid(run_details)

        if asynchronous is True:
            return run_details
        else:
            start = time.time()
            print('Training of ' + str(trained_model_guid) + ' started ...')

            status = self.get_status(trained_model_guid)
            state = status['state']

            # TODO add iterations progress based on details
            while ('completed' not in state) and ('error' not in state) and ('canceled' not in state):
                elapsed_time = time.time() - start
                print("Elapsed time: " + str(elapsed_time) + " -> training state: " + str(state))
                sys.stdout.flush()
                status = self.get_status(trained_model_guid)
                state = status['state']
                for i in tqdm.tqdm(range(10)):
                    time.sleep(1)

            if 'completed' in state:
                print('Training of \'{}\' finished successfully.'.format(str(trained_model_guid)))
            else:
                print('Training of \'{}\' failed with status: \'{}\'.'.format(trained_model_guid, str(status)))

            # TODO probably details should be get right before returning them
            self.logger.debug('Response({}): {}'.format(state, run_details))
            return run_details

    def list(self):
        """
           List training runs.

           A way you might use me is

           >>> client.training.list()
        """
        from tabulate import tabulate

        details = self.get_details()
        resources = details['resources']
        values = [(m["metadata"]['guid'], m["entity"]['status']['state'], m['metadata']['created_at'],
                   m['entity']['model_definition']['framework']['name']) for m in resources]
        table = tabulate([["GUID (training)", "STATE", "CREATED", "FRAMEWORK"]] + values)
        print(table)

    def delete(self, run_uid=None, run_url=None):
        """
            Delete trained model.

            Args:
                run_uid (str) - ID of trained model (optional).
                run_url (str) - URL of trained model (optional).

            A way you might use me is

            >>> trained_models_list = client.training.delete(run_uid)
            >>> trained_models_list = client.training.delete(run_uid=run_uid)
            >>> trained_models_list = client.training.delete(run_url=run_url)
        """
        Training._validate_type(run_uid, 'run_uid', str, False)
        Training._validate_type(run_url, 'run_url', str, False)

        run_uid = Training._get_artifact_uid(run_uid, run_url, True)

        response_delete = requests.delete(self._base_models_url + '/' + str(run_uid),
                                          headers=get_headers(self._wml_token))

        self._handle_response(204, 'trained model deletion', response_delete, False)

    def monitor(self, run_uid=None, run_url=None):
        """
            Monitor training log file (prints log content to console).

            Args:
                run_uid (str) - ID of trained model (optional).
                run_url (str) - URL of trained model (optional).

            A way you might use me is

            >>> client.training.monitor(run_uid)
            >>> client.training.monitor(run_uid=run_uid)
            >>> client.training.monitor(run_url=run_url)
        """
        Training._validate_type(run_uid, 'run_uid', str, False)
        Training._validate_type(run_url, 'run_url', str, False)

        run_uid = Training._get_artifact_uid(run_uid, run_url, True)

        from lomond import WebSocket

        monitor_endpoint = self._wml_credentials['url'].replace('https',
                                                                'wss') + "/v3/models/" + run_uid + "/monitor"
        websocket = WebSocket(monitor_endpoint)
        websocket.add_header(bytes("Authorization", "utf-8"), bytes("bearer " + self._wml_token, "utf-8"))

        print("Log monitor started.")

        for event in websocket:
            if event.name == 'text':
                text = json.loads(event.text)
                status = text['status']
                # TODO keeping both text and status because of bug - target just text
                if 'message' in status:
                    print(status["message"])
                elif 'message' in text:
                    print(text["message"])

        print("Log monitor done.")
