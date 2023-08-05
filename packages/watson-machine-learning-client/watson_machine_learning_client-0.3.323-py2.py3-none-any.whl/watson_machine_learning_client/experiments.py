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
from .utils import get_headers, get_artifact_uid
import time
import tqdm
import sys
from .wml_client_error import MissingValue, WMLClientError
from .href_definitions import is_uid, is_url
from .wml_resource import WMLResource
from multiprocessing import Pool


class Experiments(WMLResource):
    """
       Run new experiment.
    """

    def __init__(self, client, wml_credentials, wml_token, instance_details):
        WMLResource.__init__(self, __name__, client, wml_credentials, wml_token, instance_details)
        self._experiments_uids_cache = {}

    def _get_experiment_uid(self, experiment_run_uid=None, experiment_run_url=None):
        if experiment_run_uid is None and experiment_run_url is None:
            raise MissingValue('experiment_run_id/experiment_run_url')

        if experiment_run_uid is not None and experiment_run_uid in self._experiments_uids_cache:
            return self._experiments_uids_cache[experiment_run_uid]

        if experiment_run_url is not None:
            m = re.search('.+/v3/experiments/{[^\/]+}/runs/{[^\/]+}', experiment_run_url)
            _experiment_id = m.group(1)
            _experiment_run_id = m.group(2)
            self._experiments_uids_cache.update({_experiment_run_id: _experiment_id})
            return _experiment_id

        details = self.get_details()
        resources = details['resources']

        try:
            el = [x for x in resources if x['metadata']['run_id'] == experiment_run_uid][0]
        except Exception as e:
            raise WMLClientError('Cannot find experiment_uid for experiment_run_uid: \'{}\''.format(experiment_run_uid), e)

        experiment_uid = el['metadata']['experiment_id']
        self._experiments_uids_cache.update({experiment_run_uid: experiment_uid})
        return experiment_uid

    def run(self, experiment_uid=None, experiment_url=None, asynchronous=True):
        """
            Run experiment. Either experiment_uid or experiment_url must be specified.

            Args:
                experiment_uid (str): ID of experiment (optional).
                experiment_url (str): URL of experiment (optional).
                asynchronous (bool): Default True means that experiment is started and progress can be checked later. False - method will wait till experiment end and print experiment stats.

           Returns:
               run_details (dict) - experiment run details.

            A way you might use me is

            >>> experiment_run_status = client.experiments.run(experiment_uid)
            >>> experiment_run_status = client.experiments.run(experiment_uid=experiment_uid)
            >>> experiment_run_status = client.experiments.run(experiment_url=experiment_url)
            >>> experiment_run_status = client.experiments.run(experiment_uid, asynchronous=False)
            >>> experiment_run_status = client.experiments.run(experiment_uid=experiment_uid, asynchronous=False)
            >>> experiment_run_status = client.experiments.run(experiment_url=experiment_url, asynchronous=False)
        """
        Experiments._validate_type(experiment_uid, 'experiment_uid', str, False)
        Experiments._validate_type(experiment_url, 'experiment_url', str, False)
        Experiments._validate_type(asynchronous, 'asynchronous', bool, True)
        experiment_uid = get_artifact_uid(experiment_uid, experiment_url)
        run_url = self._href_definitions.get_experiment_runs_href(experiment_uid)

        response = requests.post(run_url, headers=get_headers(self._wml_token))

        # TODO should be 202
        result_details = self._handle_response(200, 'experiment run', response)

        experiment_run_uid = self.get_run_uid(result_details)
        self._experiments_uids_cache.update({experiment_run_uid: experiment_uid})

        if asynchronous:
            return result_details
        else:
            start = time.time()
            print('Run of ' + str(experiment_uid) + ' started ...')

            status = self.get_status(experiment_run_uid)
            state = status['state']

            # TODO add iterations progress based on details
            while ('completed' not in state) and ('error' not in state) and ('canceled' not in state):
                elapsed_time = time.time() - start
                print("Elapsed time: " + str(elapsed_time) + " -> run state: " + str(state))
                sys.stdout.flush()
                status = self.get_status(experiment_run_uid)
                state = status['state']
                for i in tqdm.tqdm(range(10)):
                    time.sleep(1)

            if 'completed' in state:
                print('Run of \'{}\' finished successfully.'.format(str(experiment_run_uid)))
            else:
                print(
                    'Run of \'{}\' failed with status: \'{}\'.'.format(experiment_run_uid, str(status)))

            # TODO probably details should be get one more time
            self.logger.debug('Response({}): {}'.format(state, result_details))
            return result_details

    def get_status(self, experiment_run_uid=None, experiment_run_url=None):
        """
            Get experiment status. Either experiment_run_uid or experiment_run_url must be specified.

            Args:
                experiment_run_uid (str): ID of experiment run (optional).
                experiment_run_url (str): URL of experiment run (optional).

            Returns:
                status (dict) - experiment status.

            A way you might use me is

            >>> experiment_status = client.experiments.get_status(experiment_run_uid)
            >>> experiment_status = client.experiments.get_status(experiment_run_uid=experiment_run_uid)
            >>> experiment_status = client.experiments.get_status(experiment_run_url=experiment_run_url)
        """
        Experiments._validate_type(experiment_run_uid, 'experiment_run_uid', str, False)
        Experiments._validate_type(experiment_run_url, 'experiment_run_url', str, False)
        details = self.get_details(experiment_run_uid=experiment_run_uid, experiment_run_url=experiment_run_url)

        try:
            status = WMLResource._get_required_element_from_dict(details, 'details', ['entity', 'experiment_run_status'])
        except Exception as e:
            # TODO more specific
            raise WMLClientError('Failed to get from details state of experiment.', e)

        if status is None:
            raise MissingValue('entity.experiment_run_status')

        return status

    @staticmethod
    def _get_details_helper(url, headers, setting):
        response_get = requests.get(
            url + '/runs',
            headers=headers)
        if response_get.status_code == 200:
            details = json.loads(response_get.text)

            if 'resources' in details:
                resources = details['resources']
            else:
                resources = [details]

            for r in resources:
                r['entity'].update({'_parent_settings': setting})
            return resources
        else:
            return []

    def get_details(self, experiment_uid=None, experiment_url=None, experiment_run_uid=None, experiment_run_url=None):
        """
           Get metadata of experiment run(s).

           Args:
               experiment_uid (str):  experiment UID (optional).
               experiment_url (str):  experiment URL (optional).
               experiment_run_uid (str):  experiment run UID (optional).
               experiment_run_url (str):  experiment run URL (optional).

           Returns:
               experiment run details (dict) - experiment run(s) metadata.

           A way you might use me is

           >>> experiment_details = client.experiments.get_details(experiment_run_uid=experiment_run_uid)
           >>> experiment_details = client.experiments.get_details(experiment_run_url=experiment_run_url)
           >>> experiment_details = client.experiments.get_details(experiment_uid)
           >>> experiment_details = client.experiments.get_details(experiment_url=experiment_url)
           >>> experiment_details = client.experiments.get_details()
        """
        Experiments._validate_type(experiment_uid, 'experiment_uid', str, False)
        Experiments._validate_type(experiment_url, 'experiment_url', str, False)
        Experiments._validate_type(experiment_run_uid, 'experiment_run_uid', str, False)
        Experiments._validate_type(experiment_run_url, 'experiment_run_url', str, False)

        _experiment_uid = get_artifact_uid(experiment_uid, experiment_url, False)
        _experiment_run_uid = get_artifact_uid(experiment_run_uid, experiment_run_url, False)

        if _experiment_uid is None and _experiment_run_uid is not None:
            _experiment_uid = self._get_experiment_uid(_experiment_run_uid)

        if _experiment_uid is None:
            experiments = self._client.repository.get_experiment_details()

            try:
                urls_and_settings = [(experiment['metadata']['url'], experiment['entity']['settings']) for experiment in experiments['resources']]

                self.logger.debug('Preparing details for urls and settings: {}'.format(urls_and_settings))

                res = []

                with Pool(processes=4) as pool:
                    tasks = []
                    for url_and_setting in urls_and_settings:
                        url = url_and_setting[0]
                        setting = url_and_setting[1]
                        tasks.append(pool.apply_async(Experiments._get_details_helper, (url, get_headers(self._wml_token), setting)))

                    for task in tasks:
                        res.extend(task.get())

            except Exception as e:
                raise WMLClientError('Error during getting all experiments details.', e)
            return {"resources": res}

        url = self._client.repository.get_experiment_url(self._client.repository.get_experiment_details(_experiment_uid)) + '/runs'

        if _experiment_run_uid is None:
            response_get = requests.get(
                url,
                headers=get_headers(self._wml_token))
            response = self._handle_response(200, 'getting experiment details', response_get)
            setting = self._client.repository.get_experiment_details(experiment_uid=_experiment_uid)['entity']['settings']
            for r in response['resources']:
                r['entity'].update({'_parent_settings': setting})
            return response
        else:
            url = url + "/" + _experiment_run_uid
            response_get = requests.get(
                url,
                headers=get_headers(self._wml_token))
            response = self._handle_response(200, 'getting experiment run details', response_get)
            setting = self._client.repository.get_experiment_details(experiment_uid=_experiment_uid)['entity']['settings']
            response['entity'].update({'_parent_settings': setting})
            return response

    @staticmethod
    def get_run_url(experiment_run_details):
        """
            Get experiment run url.

            Args:
                experiment_run_details (obj): details of experiment run.

            Returns:
                url (str) - experiment run url.

            A way you might use me is

            >>> experiment_run_url = client.experiments.get_run_url(experiment_run_details)
        """

        Experiments._validate_type(experiment_run_details, 'experiment_run_details', object, True)

        try:
            # TODO probably should be entity.url
            url = WMLResource._get_required_element_from_dict(experiment_run_details, 'experiment_run_details', ['metadata', 'url'])
        except Exception as e:
            raise WMLClientError('Failure during getting experiment url from details.', e)

        # TODO uncomment
        # if not is_url(url):
        #     raise WMLClientError('Experiment url: \'{}\' is invalid.'.format(url))

        return url

    @staticmethod
    def get_run_uid(experiment_run_details):
        """
            Get experiment run uid.

            Args:
                experiment_run_details (obj): details of experiment run.

            Returns:
                uid (str) - experiment run uid.

            A way you might use me is

            >>> experiment_run_uid = client.experiments.get_run_uid(experiment_run_details)
        """

        Experiments._validate_type(experiment_run_details, 'experiment_run_details', object, True)

        # TODO probably should be just entity.guid
        try:
            uid = WMLResource._get_required_element_from_dict(experiment_run_details, 'experiment_run_details', ['metadata', 'run_id'])
        except Exception as e:
            raise WMLClientError('Failure during getting experiment uid from details.', e)

        if not is_uid(uid):
            raise WMLClientError('Experiment uid: \'{}\' is invalid.'.format(uid))

        return uid

    def delete(self, experiment_run_uid=None, experiment_run_url=None):
        """
            Delete experiment run. Either experiment_run_uid or experiment_run_url must be specified.

            Args:
                experiment_run_uid (str):  experiment run UID (optional).
                experiment_run_url (str):  experiment run URL (optional).

            A way you might use me is

            >>> client.experiments.delete(experiment_run_uid)
            >>> client.experiments.delete(experiment_run_uid=experiment_run_uid)
            >>> client.experiments.delete(experiment_run_url=experiment_run_url)
        """
        Experiments._validate_type(experiment_run_uid, 'experiment_run_uid', str, False)
        Experiments._validate_type(experiment_run_url, 'experiment_run_url', str, False)

        experiment_uid = self._get_experiment_uid(experiment_run_uid, experiment_run_url)
        experiment_run_uid = get_artifact_uid(experiment_run_uid, experiment_run_url)

        run_url = self._href_definitions.get_experiment_run_href(experiment_uid, experiment_run_uid)

        response = requests.delete(run_url, headers=get_headers(self._wml_token))

        self._handle_response(204, 'experiment deletion', response, False)

    def list(self, experiment_uid=None, experiment_url=None):
        """
            List experiment runs.

            A way you might use me is

            >>> client.experiments.list()
            >>> client.experiments.list(experiment_uid)
            >>> client.experiments.list(experiment_uid=experiment_uid)
            >>> client.experiments.list(experiment_url=experiment_url)
        """
        Experiments._validate_type(experiment_uid, 'experiment_uid', str, False)
        Experiments._validate_type(experiment_url, 'experiment_url', str, False)

        from tabulate import tabulate

        details = self._client.experiments.get_details(experiment_uid=experiment_uid, experiment_url=experiment_url)
        resources = details['resources']

        values = [(m['metadata']['experiment_id'], m['metadata']['run_id'], m['entity']['_parent_settings']['name'], m['entity']['experiment_run_status']['state'], m['metadata']['created_at']) for m in resources]
        table = tabulate([["GUID (experiment)", "GUID (run)", "NAME (experiment)", "STATE", "CREATED"]] + values)
        print(table)

    def monitor(self, experiment_run_uid=None, experiment_run_url=None):
        """
            Monitor experiment run log files (prints log content to console). Either experiment_run_uid or experiment_run_url must be specified.

            Args:
                experiment_run_uid (str) - ID of experiment run (optional).
                experiment_run_url (str) - URL of experiment run (optional).

            A way you might use me is

            >>> client.experiments.monitor(experiment_run_uid)
            >>> client.experiments.monitor(experiment_run_uid=experiment_run_uid)
            >>> client.experiments.monitor(experiment_run_url=experiment_run_url)
        """
        Experiments._validate_type(experiment_run_uid, 'experiment_run_uid', str, False)
        Experiments._validate_type(experiment_run_url, 'experiment_run_url', str, False)

        if experiment_run_uid is None and experiment_run_url is None:
            raise WMLClientError('Both experiment_run_uid and experiment_run_url are empty.')

        details = self.get_details(experiment_run_uid=experiment_run_uid, experiment_run_url=experiment_run_url)
        for training_status in details['entity']['training_statuses']:
            print('\n')
            print('#' * 50)
            print("\nMonitoring for training_guid: \'{}\'\n".format(training_status['training_guid']))
            print('#' * 50)
            print('')
            self._client.training.monitor(run_uid=training_status['training_guid'])
