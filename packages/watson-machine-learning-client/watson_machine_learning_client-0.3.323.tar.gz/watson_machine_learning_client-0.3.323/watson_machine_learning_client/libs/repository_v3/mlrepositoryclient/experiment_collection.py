################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################


import logging, re

from repository_v3.mlrepository import MetaNames, PipelineArtifact
from repository_v3.swagger_client.api_client import ApiException
from repository_v3.swagger_client.models import MlAssetsCreateExperimentInput, MlAssetsCreateModelInput, \
    MlAssetsCreateModelOutput , MlAssetsCreateExperimentOutput

from repository_v3.util import  Json2ObjectMapper
import json
from .experiment_adapter import ExperimentAdapter
from repository_v3.swagger_client.models.author_repository import AuthorRepository
from repository_v3.swagger_client.models.framework_output_repository import FrameworkOutputRepository
from repository_v3.swagger_client.models.connection_object_with_name_repository import ConnectionObjectWithNameRepository
from repository_v3.swagger_client.models.ml_assets_create_experiment_input import MlAssetsCreateExperimentInput
from repository_v3.swagger_client.models.array_data_input_repository import  ArrayDataInputRepository

logger = logging.getLogger('ExperimentCollection')


class ExperimentCollection:
    """
    Client operating on experiments in repository service.

    :param str base_path: base url to Watson Machine Learning instance
    :param MLRepositoryApi repository_api: client connecting to repository rest api
    :param MLRepositoryClient client: high level client used for simplification and argument for constructors
    """
    def __init__(self, base_path, repository_api, client):

        from repository_v3.mlrepositoryclient import MLRepositoryApi, MLRepositoryClient

        if not isinstance(base_path, str) and not isinstance(base_path, unicode):
            raise ValueError('Invalid type for base_path: {}'.format(base_path.__class__.__name__))

        if not isinstance(repository_api, MLRepositoryApi):
            raise ValueError('Invalid type for repository_api: {}'.format(repository_api.__class__.__name__))

        if not isinstance(client, MLRepositoryClient):
            raise ValueError('Invalid type for client: {}'.format(client.__class__.__name__))

        self.base_path = base_path
        self.repository_api = repository_api
        self.client = client

    def _extract_mlassets_create_experiment_output(self, service_output):
        latest_version = service_output.entity['experiment_version']
        return ExperimentAdapter(service_output, latest_version, self.client).artifact()

    def all(self):
        """
        Gets info about all experiments which belong to this user.

        Not complete information is provided by all(). To get detailed information about experiment use get().

        :return: info about experiments
        :rtype: list[ExperimentsArtifact]
        """
        all_experiments = self.repository_api.repository_list_experiments()
        list_pipeline_artifact = []
        if all_experiments is not None:
            resr = all_experiments.resources
            for iter1 in resr:
                exper_entity = iter1.entity
                ver_url = iter1.entity['training_definition_version']
                list_pipeline_artifact.append(ExperimentAdapter(iter1, ver_url, self.client).artifact())
            return list_pipeline_artifact
        else:
            return []

    def versions(self, experiment_id):
        """
        Gets all available versions.

        Not implemented yet.

        :param str experiment_id: uid used to identify model
        :return: ???
        :rtype: list[str]
        """

        if not isinstance(experiment_id, str) and  not isinstance(experiment_id, unicode):
            raise ValueError('Invalid type for experiment_id: {}'.format(experiment_id.__class__.__name__))

        experiment_ver_output = self.repository_api.repository_list_experiment_versions(experiment_id)

        list_pipeline_artifact = [PipelineArtifact]
        if experiment_ver_output is not None:
            resr = experiment_ver_output.resources
            for iter1 in resr:
                exper_entity = iter1.entity
                ver_url = iter1.entity['training_definition_version']
                list_pipeline_artifact.append(ExperimentAdapter(iter1, ver_url, self.client).artifact())
            return list_pipeline_artifact
        else:
            raise ApiException('Pipeline with guid={} not found'.format(experiment_id))

    def get(self, experiment_id):

        """
        Gets detailed information about experiment.

        :param str experiment_id: uid used to identify experiment
        :return: returned object has all attributes of SparkPipelineArtifact but its class name is PipelineArtifact
        :rtype: PipelineArtifact(SparkPipelineLoader)
        """

        if not isinstance(experiment_id, str) and  not isinstance(experiment_id, unicode):
            raise ValueError('Invalid type for experiment_id: {}'.format(experiment_id.__class__.__name__))

        experiment_output = self.repository_api.v3_ml_assets_experiments_experiment_id_get(experiment_id)

        if experiment_output is not None:
            ver_url = experiment_output.entity['training_definition_version']
            return ExperimentAdapter(experiment_output, ver_url, self.client).artifact()
        else:
            raise Exception('Model with guid={} not found'.format(experiment_id))


    def version(self, experiment_id, ver):
        """
        Gets experiment version with given experiment_id and ver

        :param str experiment_id: uid used to identify experiment
        :param str ver: uid used to identify version of experiment
        :return: returned object has all attributes of SparkPipelineArtifact but its class name is PipelineArtifact
        :rtype: PipelineArtifact(SparkPipelineLoader)
        """

        if not isinstance(experiment_id, str) and not isinstance(experiment_id, unicode):
            raise ValueError('Invalid type for experiment_id: {}'.format(experiment_id.__class__.__name__))

        #if not isinstance(ver.encode('ascii'), str):
        if not isinstance(ver, str) and not isinstance(ver, unicode):
            raise ValueError('Invalid type for ver: {}'.format(ver.__class__.__name__))

        experiment_output = self.repository_api.repository_get_experiment_version(experiment_id, ver)

        if experiment_output is not None:
            ver_url = experiment_output.entity['training_definition_version']
            return ExperimentAdapter(experiment_output, ver_url, self.client).artifact()
            #return self._extract_experiments_from_output(experiment_output)
        else:
            raise Exception('Model with guid={} not found'.format(experiment_id))

    def version_from_url(self, artifact_version_url):
        """
        Gets experiment version from given href

        :param str artifact_version_href: href identifying artifact and version
        :return: returned object has all attributes of SparkPipelineArtifact but its class name is PipelineArtifact
        :rtype: PipelineArtifact(SparkPipelineLoader)
        """

        if not isinstance(artifact_version_url, str) and not isinstance(artifact_version_url, unicode):
            raise ValueError('Invalid type for artifact_version_href: {}'
                             .format(artifact_version_url.__class__.__name__))

        #if artifact_version_url.startswith(self.base_path):
        matched = re.search(
                '.*/v3/ml_assets/experiments/([A-Za-z0-9\-]+)/versions/([A-Za-z0-9\-]+)', artifact_version_url)
        matchedV2 = re.search(
            '.*/v2/artifacts/pipelines/([A-Za-z0-9\-]+)/versions/([A-Za-z0-9\-]+)', artifact_version_url)

        matchedV3 = re.search(
            '.*/v3/ml_assets/training_definitions/([A-Za-z0-9\-]+)/versions/([A-Za-z0-9\-]+)', artifact_version_url)
        if matched is not None:
            experiment_id = matched.group(1)
            version_id = matched.group(2)
            return self.version(experiment_id, version_id)
        elif matchedV2 is not None:
            experiment_id = matchedV2.group(1)
            version_id = matchedV2.group(2)
            return self.version(experiment_id, version_id)
        elif matchedV3 is not None:
            experiment_id = matchedV3.group(1)
            version_id = matchedV3.group(2)
            return self.version(experiment_id, version_id)
        else:
            raise ValueError('Unexpected artifact version href: {} format'.format(artifact_version_url))
        #else:
        #    raise ValueError('The artifact version href: {} is not within the client host: {}').format(
        #        artifact_version_url,
        #        self.base_path
        #    )

    def remove(self, experiment_id):
        """
        Removes experiment with given experiment_id.

        :param str experiment_id: uid used to identify experiment
        """

        if not isinstance(experiment_id, str) and not isinstance(experiment_id, unicode):
            raise ValueError('Invalid type for experiment_id: {}'.format(experiment_id.__class__.__name__))

        return self.repository_api.v3_ml_assets_experiments_experiment_id_delete(experiment_id)

    def save(self, artifact):
        """
        Saves experiment in repository service.

        :param SparkPipelineArtifact artifact: artifact to be saved in the repository service
        :return: saved artifact with changed MetaProps
        :rtype: SparkPipelineArtifact
        """

        logger.debug('Creating a new experiment: {}'.format(artifact.name))

        if not issubclass(type(artifact), PipelineArtifact):
            raise ValueError('Invalid type for artifact: {}'.format(artifact.__class__.__name__))

        if artifact.meta.prop(MetaNames.EXPERIMENT_VERSION_URL) is not None:
            raise ApiException(400, 'Invalid operation: save the same experiment artifact twice')

        try:
            experiment_id = artifact.uid
            if experiment_id is None:
                experiment_input = self._prepare_experiment_input(artifact)
                r = self.repository_api.ml_assets_experiment_creation_with_http_info(experiment_input)
                statuscode = r[1]
                if statuscode is not 201:
                    logger.info('Error while creating experiment: no location header')
                    print("response code froms service: ", statuscode)
                    raise ApiException(404, 'No artifact location')

                experiment_artifact = self._extract_experiments_from_output(r)
                location = r[2].get('Location')
                location_match = re.search('.*/v3/ml_assets/training_definitions/([A-Za-z0-9\\-]+)', location)

                if location_match is not None:
                    experiment_id = location_match.group(1)
                else:
                    logger.info('Error while creating experiment: no location header')
                    raise ApiException(404, 'No artifact location')
                artifact_with_guid = artifact._copy(experiment_id)
                #version_location = experiment_artifact.meta.prop(MetaNames.EXPERIMENT_VERSION_URL).encode('ascii')
                version_location = experiment_artifact.meta.prop(MetaNames.TRAINING_DEFINITION_VERSION_URL)
                version_id = experiment_artifact.meta.prop(MetaNames.VERSION)
                experiment_artifact.pipeline_instance = lambda: artifact.ml_pipeline

                if version_location is not None:
                    content_stream = artifact_with_guid.reader().read()
                    self.repository_api.upload_pipeline_version(experiment_id, version_id, content_stream)
                    content_stream.close()
                    artifact_with_guid.reader().close()
                    return experiment_artifact
                else:
                    logger.info('Error while creating experiment version: no location header')
                    raise ApiException(404, 'No artifact location')
            else:
                raise ApiException(404, 'Pipeline not found')

        except Exception as e:
            logger.info('Error in experiment creation')
            import traceback
            print(traceback.format_exc())
            raise e

    def _extract_experiments_from_output(self, service_output):

        latest_version = service_output[0].entity['training_definition_version']
        return ExperimentAdapter(service_output[0], latest_version, self.client).artifact()

    @staticmethod
    def _prepare_experiment_input(artifact):
        exper_input = MlAssetsCreateExperimentInput()
        exper_input.name = artifact.name
        exper_input.description = artifact.meta.prop(MetaNames.DESCRIPTION)

        exper_input.author = AuthorRepository(
             artifact.meta.prop(MetaNames.AUTHOR_NAME),
             artifact.meta.prop(MetaNames.AUTHOR_EMAIL)
        )

        exper_input.framework = FrameworkOutputRepository(
              artifact.meta.prop(MetaNames.FRAMEWORK_NAME),
              artifact.meta.prop(MetaNames.FRAMEWORK_VERSION)
        )


        if artifact.meta.prop(MetaNames.TRAINING_DATA_REFERENCE) is not None:
            dataref_list=artifact.meta.prop(MetaNames.TRAINING_DATA_REFERENCE)
            if isinstance(dataref_list, str):
               dataref_list = json.loads(artifact.meta.prop(MetaNames.TRAINING_DATA_REFERENCE))
            training_data_list = []
            if isinstance(dataref_list, list):
                for iter1 in dataref_list:
                    training_data = ConnectionObjectWithNameRepository(
                        iter1.get('name', None),
                        iter1.get('connection', None),
                        iter1.get('source', None)
                    )
                    training_data_list.append(training_data)
            elif isinstance(dataref_list, dict):
                training_data = ConnectionObjectWithNameRepository(
                    dataref_list.get('name', None),
                    dataref_list.get('connection', None),
                    dataref_list.get('source', None)
                )
                training_data_list.append(training_data)
            else:

                raise ApiException(404, 'Pipeline not found')
            exper_input.training_data_reference = training_data_list

        return exper_input

#    @staticmethod
#    def _get_version_input(artifact):
#     return PipelineVersionInput(artifact.meta.prop(MetaNames.PARENT_VERSION))
