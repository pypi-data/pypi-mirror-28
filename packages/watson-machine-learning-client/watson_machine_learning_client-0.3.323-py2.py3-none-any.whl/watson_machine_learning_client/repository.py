################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################


from repository_v3.mlrepositoryclient import MLRepositoryClient
from repository_v3.mlrepositoryartifact import MLRepositoryArtifact
from repository_v3.mlrepository import MetaProps
import requests
import json
from .utils import get_headers, get_artifact_uid
from .metanames import ModelDefinitionMetaNames, ModelMetaNames, ExperimentMetaNames
import os
from .wml_client_error import WMLClientError
from .href_definitions import is_uid, is_url
from .wml_resource import WMLResource
from multiprocessing import Pool


class Repository(WMLResource):
    """
    Manage your models using Watson Machine Learning Repository.
    """

    def __init__(self, client, wml_credentials, wml_token, ml_repository_client, instance_details):
        WMLResource.__init__(self, __name__, client, wml_credentials, wml_token, instance_details)
        Repository._validate_type(ml_repository_client, 'ml_repository_client', object, True)
        self._ml_repository_client = ml_repository_client
        self.DefinitionMetaNames = ModelDefinitionMetaNames()
        self.ModelMetaNames = ModelMetaNames()
        self.ExperimentMetaNames = ExperimentMetaNames()
        self._definition_endpoint = '{}/v3/ml_assets/training_definitions'.format(self._wml_credentials['url'])
        self._experiment_endpoint = '{}/v3/experiments'.format(self._wml_credentials['url'])

    def store_experiment(self, meta_props):
        """
           Store experiment into Watson Machine Learning repository on IBM Cloud.

           Args:

               meta_props (dict): meta data of the experiment configuration. To see available meta names use:
               >>> client.repository.ExperimentMetaNames.get()

           Returns:
               experiment details (dict) - stored experiment details.

           A way you might use me is

           >>> metadata = {
           >>>  client.repository.ExperimentMetaNames.NAME: "my_experiment",
           >>>  client.repository.ExperimentMetaNamesDESCRIPTION: "mnist best model",
           >>>  client.repository.ExperimentMetaNames.AUTHOR_NAME: "John Smith",
           >>>  client.repository.ExperimentMetaNames.AUTHOR_EMAIL: "js@js.com",
           >>>  client.repository.ExperimentMetaNames.EVALUATION_METHOD: "multiclass",
           >>>  client.repository.ExperimentMetaNames.EVALUATION_METRIC: "accuracy",
           >>>  client.repository.ExperimentMetaNames.TRAINING_DATA_REFERENCE: {},
           >>>  client.repository.ExperimentMetaNames.TRAINING_RESULTS_REFERENCE: {},
           >>>  client.repository.ExperimentMetaNames.TRAINING_REFERENCES: [
           >>>      { "name": "mnist_nn",
           >>>        "training_definition_url": definition_url_1,
           >>>        "command": "python3 mnist_softmax.py --trainingIters 100",
           >>>        "compute_configuration": {"size": "small"},
           >>>      },
           >>>      { "name": "mnist_cnn",
           >>>        "training_definition_url": definition_url_2,
           >>>        "command": "python3 mnist_lenet.py --trainingIters 100",
           >>>        "compute_configuration": {"size": "small"},
           >>>      },
           >>>   ],
           >>> }
           >>> experiment_details = client.repository.store_experiment(meta_props=metadata)
           >>> experiment_url = client.repository.get_experiment_url(experiment_details)
        """
        Repository._validate_type(meta_props, 'meta_props', dict, False)

        experiment_metadata = {
                       "settings": {
                          "name": meta_props[self.ExperimentMetaNames.NAME],
                          "description": meta_props[self.ExperimentMetaNames.DESCRIPTION],
                          "author": {
                             "name": meta_props[self.ExperimentMetaNames.AUTHOR_NAME],
                             "email": meta_props[self.ExperimentMetaNames.AUTHOR_EMAIL]
                          },
                          "evaluation_definition": {
                             "method": meta_props[self.ExperimentMetaNames.EVALUATION_METHOD],
                             "metrics": [
                                {
                                   "name": meta_props[self.ExperimentMetaNames.EVALUATION_METRIC],
                                }
                             ]
                          }
                       },
                       "training_references": meta_props[self.ExperimentMetaNames.TRAINING_REFERENCES],
                       "training_data_reference": meta_props[self.ExperimentMetaNames.TRAINING_DATA_REFERENCE],
                       "training_results_reference": meta_props[self.ExperimentMetaNames.TRAINING_RESULTS_REFERENCE],
                    }

        response_experiment_post = requests.post(self._experiment_endpoint, json=experiment_metadata, headers=get_headers(self._wml_token))

        return self._handle_response(201, 'saving experiment', response_experiment_post)

    def store_definition(self, training_definition, meta_props):
        """
           Store training definition into Watson Machine Learning repository on IBM Cloud.

           Args:
               training_definition (str):  path to zipped model_definition.

               meta_props (dict): meta data of the training definition. To see available meta names use:
               >>> client.repository.DefinitionMetaNames.get()


           Returns:
               definition details (dict) - stored training definition details.

           A way you might use me is

           >>> metadata = {
           >>>  client.repository.DefinitionMetaNames.NAME: "my_training_definition",
           >>>  client.repository.DefinitionMetaNames.DESCRIPTION: "my_description",
           >>>  client.repository.DefinitionMetaNames.AUTHOR_NAME: "John Smith",
           >>>  client.repository.DefinitionMetaNames.AUTHOR_EMAIL: "js@js.com",
           >>>  client.repository.DefinitionMetaNames.FRAMEWORK_NAME: "tensorflow",
           >>>  client.repository.DefinitionMetaNames.FRAMEWORK_VERSION: "1.2",
           >>>  client.repository.DefinitionMetaNames.RUNTIME_NAME: "python",
           >>>  client.repository.DefinitionMetaNames.RUNTIME_VERSION: "3.5",
           >>>  client.repository.DefinitionMetaNames.EXECUTION_COMMAND: "python3 tensorflow_mnist_softmax.py --trainingIters 20"
           >>> }
           >>> definition_details = client.repository.store_definition(training_definition_filepath, meta_props=metadata)
           >>> definition_url = client.repository.get_definition_url(definition_details)
        """
        Repository._validate_type(training_definition, 'training_definition', str, True)
        Repository._validate_type(meta_props, 'meta_props', dict, False)

        # TODO to be replaced with repository client

        training_definition_metadata = {
                               "name": meta_props[self.DefinitionMetaNames.NAME],
                               "description": meta_props[self.DefinitionMetaNames.DESCRIPTION],
                               "framework": {
                                   "name": meta_props[self.DefinitionMetaNames.FRAMEWORK_NAME],
                                   "version": meta_props[self.DefinitionMetaNames.FRAMEWORK_VERSION],
                                   "runtimes": [{
                                        "name": meta_props[self.DefinitionMetaNames.RUNTIME_NAME],
                                        "version": meta_props[self.DefinitionMetaNames.RUNTIME_VERSION]
                                    }]
                                },
                               "command": meta_props[self.DefinitionMetaNames.EXECUTION_COMMAND]
        }

        response_definition_post = requests.post(self._definition_endpoint, json=training_definition_metadata, headers=get_headers(self._wml_token))

        details = self._handle_response(201, 'saving model definition', response_definition_post)

        definition_version_content_url = response_definition_post.json().get('entity').get(
            'training_definition_version').get('content_url')
        # save model definition content
        put_header = {'Authorization': "Bearer " + self._wml_token, 'Content-Type': 'application/octet-stream'}
        data = open(training_definition, 'rb').read()
        response_definition_put = requests.put(definition_version_content_url, data=data, headers=put_header)

        self._handle_response(200, 'saving model definition content', response_definition_put)

        return details

    def _publish_from_object(self, model, name, meta_props=None, training_data=None, training_target=None):
        """
        Store model from object in memory into Watson Machine Learning repository on Cloud
        """
        try:
            ml_repository_client = MLRepositoryClient(self._wml_credentials['url'])
            ml_repository_client.authorize(self._wml_credentials['username'], self._wml_credentials['password'])

            if meta_props is None:
                meta_data = MetaProps({})
            else:
                meta_data = MetaProps(meta_props)

            if 'pyspark.ml.pipeline.PipelineModel' in str(type(model)):
                model_artifact = MLRepositoryArtifact(model, name=name, meta_props=meta_data, training_data=training_data)
            else:
                model_artifact = MLRepositoryArtifact(model, name=name, meta_props=meta_data, training_data=training_data, training_target=training_target)

            saved_model = ml_repository_client.models.save(model_artifact)
        except Exception as e:
            raise WMLClientError("Publishing model failed.", e)
        else:
            return self.get_details(saved_model.uid)

    def _publish_from_training(self, model, name, meta_props=None, training_data=None, training_target=None):
        """
        Store trained model from object storage into Watson Machine Learning repository on IBM Cloud
        """
        ml_asset_endpoint = '{}/v3/models/{}/ml_asset'.format(self._wml_credentials['url'], model)
        details = self._client.training.get_details(model)

        if details is not None:
            base_payload = {self.DefinitionMetaNames.NAME: name}

            if meta_props is None:
                payload = base_payload
            else:
                payload = dict(base_payload, **meta_props)

            response_model_put = requests.put(ml_asset_endpoint, json=payload, headers=get_headers(self._wml_token))

            saved_model_details = self._handle_response(202, 'saving trained model', response_model_put)

            model_guid = WMLResource._get_required_element_from_dict(saved_model_details, 'saved_model_details', ['entity', 'ml_asset_guid'])
            content_status_endpoint = self._wml_credentials['url'] + '/v3/ml_assets/models/' + str(model_guid)
            response_content_status_get = requests.get(content_status_endpoint, headers=get_headers(self._wml_token))

            state = self._handle_response(200, 'checking saved model content status', response_content_status_get)['entity']['model_version']['content_status']['state']

            while ('persisted' not in state) and ('persisting_failed' not in state) and ('failure' not in state):
                response_content_status_get = requests.get(content_status_endpoint, headers=get_headers(self._wml_token))

                state = self._handle_response(200, 'checking saved model content status', response_content_status_get)['entity']['model_version']['content_status']['state']

            if 'persisted' in state:
                return saved_model_details
            else:
                raise WMLClientError('Saving trained model in repository for url: \'{}\' failed.'.format(content_status_endpoint), response_content_status_get.text)

    def _publish_from_file(self, model, name, meta_props=None, training_data=None, training_target=None):
        """
        Store saved model into Watson Machine Learning repository on IBM Cloud
        """
        import tarfile
        import zipfile

        model_filepath = model
        if os.path.isdir(model):
            # TODO currently tar.gz is required for tensorflow - the same ext should be supported for all frameworks
            if os.path.basename(model) == '':
                model = os.path.dirname(model)
            filename = os.path.basename(model) + '.tar.gz'
            current_dir = os.getcwd()
            os.chdir(model)
            target_path = os.path.dirname(model)

            with tarfile.open(os.path.join('..', filename), mode='w:gz') as tar:
                tar.add('.')

            os.chdir(current_dir)
            model_filepath = os.path.join(target_path, filename)

        if tarfile.is_tarfile(model_filepath) or zipfile.is_zipfile(model_filepath):
            try:
                ml_repository_client = MLRepositoryClient(self._wml_credentials['url'])
                ml_repository_client.authorize(self._wml_credentials['username'], self._wml_credentials['password'])

                if meta_props is None:
                    error_msg = "meta_props value have to be specified"
                    print(error_msg)
                    raise ValueError(error_msg)
                else:
                    meta_data = MetaProps(meta_props)

                model_artifact = MLRepositoryArtifact(model_filepath, name=name, meta_props=meta_data)
                saved_model = ml_repository_client.models.save(model_artifact)
            except Exception as e:
                raise WMLClientError("Publishing model failed.", e)
            else:
                return self.get_details(saved_model.uid)
        else:
            raise WMLClientError('Saving trained model in repository failed. \'{}\' file does not have valid format'.format(model_filepath))

    def publish(self, model, name, meta_props=None, training_data=None, training_target=None):
        """
        This method is deprecated. Please use store_model() instead.
        """
        self.logger.warn("Method is deprecated. Use store_model() instead.")
        return self.store_model(model, name, meta_props=meta_props, training_data=training_data, training_target=training_target)

    def store_model(self, model, name, meta_props=None, training_data=None, training_target=None):
        """
        Store trained model into Watson Machine Learning repository on Cloud.

        Args:
            model (object/str):  The train model object (e.g: spark PipelineModel), or path to saved model, or trained model guid.

            name (str):  The name for model to use.

            meta_props (dict): meta data of the training definition. To see available meta names use:
            >>> client.repository.ModelMetaNames.get()

            training_data (spark dataframe, pandas dataframe, numpy.ndarray or list):  Spark DataFrame supported for spark models. Pandas dataframe, numpy.ndarray or list supported for scikit-learn models.

            training_target (array): array with labels required for scikit-learn models.

        Returns:
            details (dict) - stored model details.

        A way you might use me with spark model is

        >>> stored_model_details = client.repository.store_model(local_model, name, meta_props={"authorName":"John Smith"}, training_data=None)

         A way you might use me with scikit-learn model is

        >>> stored_model_details = client.repository.store_model(local_model, name, meta_props=None, training_data=None, training_target=None)
        """
        Repository._validate_type(model, 'model', object, True)
        Repository._validate_type(name, 'name', str, True)
        Repository._validate_type(meta_props, 'meta_props', dict, False)
        # Repository._validate_type(training_data, 'training_data', object, False)
        # Repository._validate_type(training_target, 'training_target', list, False)

        if not isinstance(model, str):
            saved_model = self._publish_from_object(model=model, name=name, meta_props=meta_props, training_data=training_data, training_target=training_target)
        else:
            if os.path.isfile(model) or os.path.isdir(model):
                saved_model = self._publish_from_file(model=model, name=name, meta_props=meta_props, training_data=training_data, training_target=training_target)
            else:
                saved_model = self._publish_from_training(model=model, name=name, meta_props=meta_props, training_data=training_data, training_target=training_target)

        return saved_model

    def load(self, artifact_uid=None, artifact_url=None):
        """
        Load model from repository to object in local environment.

        Args:
            artifact_uid (string):  stored model UID (optional).
            artifact_url (string):  stored model URL (optional).

        Returns:
            model (object) - trained model.

        A way you might use me is

        >>> model = client.repository.load(model_uid)
        >>> model = client.repository.load(artifact_uid=model_uid)
        >>> model = client.repository.load(artifact_url=model_url)
        """
        Repository._validate_type(artifact_uid, 'artifact_uid', str, False)
        Repository._validate_type(artifact_url, 'artifact_url', str, False)

        artifact_uid = get_artifact_uid(artifact_uid, artifact_url)

        try:
            ml_repository_client = MLRepositoryClient(self._wml_credentials['url'])
            ml_repository_client.authorize(self._wml_credentials['username'], self._wml_credentials['password'])
            loaded_model = ml_repository_client.models.get(artifact_uid)
            loaded_model = loaded_model.model_instance()
            self.logger.info('Successfully loaded artifact with artifact_uid: {}'.format(artifact_uid))
            return loaded_model
        except Exception as e:
            raise WMLClientError("Loading model with artifact_uid: \'{}\' failed.".format(artifact_uid), e)

    def download(self, artifact_uid=None, artifact_url=None, filename=None):
        """
        Download model from repository to local file.

        Args:
            artifact_uid (string):  stored model UID (optional).
            artifact_url (string):  stored model URL (optional).
            filename (string):  name of local file to create (optional).

        Side effect:
            save model to file.

        A way you might use me is

        >>> client.repository.download(artifact_url=model_url, filename='downloaded_model.tar.gz')
        """
        Repository._validate_type(artifact_uid, 'artifact_uid', str, False)
        Repository._validate_type(artifact_url, 'artifact_url', str, False)
        Repository._validate_type(filename, 'filename', str, False)

        artifact_uid = get_artifact_uid(artifact_uid, artifact_url)

        artifact_url = self._href_definitions.get_model_last_version_href(artifact_uid)

        try:
            artifact_content_url = artifact_url + '/content'
            downloaded_model = self._ml_repository_client.repository_api.download_artifact_content(artifact_content_url, accept='application/gzip')
            self.logger.info('Successfully downloaded artifact with artifact_url: {}'.format(artifact_url))
        except Exception as e:
            raise WMLClientError("Downloading model with artifact_url: \'{}\' failed.".format(artifact_url), e)

        try:
            with open(filename, 'wb') as f:
                f.write(downloaded_model.data)
            self.logger.info('Successfully saved artifact to file: \'{}\''.format(filename))
            return None
        except IOError as e:
            raise WMLClientError("Saving model with artifact_url: \'{}\' failed.".format(filename), e)

    def delete(self, artifact_uid=None, artifact_url=None):
        """
          Delete model, definition or experiment from repository.

          Args:
              artifact_uid (string):  stored model, definition, or experiment UID (optional if url provided).
              artifact_url (string):  stored model, definition, or experiment URL (optional if uid provided).

          A way you might use me is
          >>> client.repository.delete(artifact_uid)
          >>> client.repository.delete(artifact_uid=artifact_uid)
          >>> client.repository.delete(artifact_url=artifact_url)
        """
        Repository._validate_type(artifact_uid, 'artifact_uid', str, False)
        Repository._validate_type(artifact_url, 'artifact_url', str, False)

        artifact_uid = get_artifact_uid(artifact_uid, artifact_url)

        artifact_type = self._check_artifact_type(artifact_uid)
        self.logger.debug('Attempting deletion of artifact with type: \'{}\''.format(str(artifact_type)))

        if artifact_type['model'] is True:
            try:
                deleted = self._ml_repository_client.models.remove(artifact_uid)
                self.logger.info('Successfully deleted model with artifact_uid: \'{}\''.format(artifact_uid))
                self.logger.debug('Return object: {}'.format(deleted))
                return
            except Exception as e:
                raise WMLClientError("Model deletion failed.", e)
        elif artifact_type['definition'] is True:
            definition_endpoint = self._definition_endpoint + '/' + artifact_uid
            self.logger.debug('Deletion artifact definition endpoint: {}'.format(definition_endpoint))
            response_delete = requests.delete(definition_endpoint, headers=get_headers(self._wml_token))

            self._handle_response(204, 'model definition deletion', response_delete, False)
            return

        elif artifact_type['experiment'] is True:
            experiment_endpoint = self._experiment_endpoint + '/' + artifact_uid
            self.logger.debug('Deletion artifact experiment endpoint: {}'.format(experiment_endpoint))
            response_delete = requests.delete(experiment_endpoint, headers=get_headers(self._wml_token))

            self._handle_response(204, 'experiment deletion', response_delete, False)
            return

        else:
            raise WMLClientError('Artifact with artifact_uid: \'{}\' does not exist.'.format(artifact_uid))

    def get_details(self, artifact_uid=None, artifact_url=None):
        """
           Get metadata of stored artifacts. If uid is not specified returns all models and definitions metadata.

           Args:
               artifact_uid (str):  stored model, definition or experiment UID (optional).
               artifact_url (str):  stored model, definition or experiment URL (optional).

           Returns:
               details (dict) - stored artifacts metadata.

           A way you might use me is

           >>> details = client.repository.get_details(artifact_uid)
           >>> details = client.repository.get_details(artifact_uid=artifact_uid)
           >>> details = client.repository.get_details()
           >>> details = client.repository.get_details(artifact_url=artifact_url)
        """
        Repository._validate_type(artifact_uid, 'artifact_uid', str, False)
        Repository._validate_type(artifact_url, 'artifact_url', str, False)

        artifact_uid = get_artifact_uid(artifact_uid, artifact_url, False)

        if artifact_uid is None:
            model_details = self.get_model_details()
            definition_details = self.get_definition_details()
            details = {'models:': model_details, 'definitions': definition_details}
        else:
            uid_type = self._check_artifact_type(artifact_uid)
            if uid_type['model'] is True:
                details = self.get_model_details(model_uid=artifact_uid)
            elif uid_type['definition'] is True:
                details = self.get_definition_details(definition_uid=artifact_uid)
            elif uid_type['experiment'] is True:
                details = self.get_definition_details(experiment_uid=artifact_uid)
            else:
                raise WMLClientError('Getting artifact details failed. Artifact uid: \'{}\' not found.'.format(artifact_uid))

        return details

    def get_model_details(self, model_uid=None, model_url=None):
        """
           Get metadata of stored models. If model uid is not specified returns all models metadata.

           Args:
               model_uid (str):  stored model, definition or pipeline UID (optional).
               model_url (str):  stored model, definition or pipeline URL (optional).

           Returns:
               model details (dict) - stored model(s) metadata.

           A way you might use me is

           >>> model_details = client.repository.get_model_details(model_uid)
           >>> model_details = client.repository.get_model_details(model_uid=model_uid)
           >>> models_details = client.repository.get_model_details()
           >>> model_details = client.repository.get_model_details(model_url=model_url)
        """
        Repository._validate_type(model_uid, 'model_uid', str, False)
        Repository._validate_type(model_url, 'model_url', str, False)

        url = self._instance_details.get('entity').get('published_models').get('url')

        if model_uid is None and model_url is None:
            response_get = requests.get(
                url,
                headers=get_headers(self._wml_token))
        else:
            if model_url is not None:
                if not is_url(model_url):
                    raise('Failure during getting model details, invalid url: \'{}\''.format(model_url))
                else:
                    url = model_url
            else:
                if not is_uid(model_uid):
                    raise('Failure during getting model details, invalid uid: \'{}\''.format(model_uid))
                else:
                    url = url + "/" + model_uid
            response_get = requests.get(
                url,
                headers=get_headers(self._wml_token))

        return self._handle_response(200, 'getting model details', response_get)

    def get_definition_details(self, definition_uid=None, definition_url=None):
        """
            Get metadata of stored definitions. If definition uid is not specified returns all model definitions metadata.

            Args:
                definition_uid (str):  stored model definition UID (optional).
                definition_url (str):  stored model definition URL (optional).

            Returns:
                definition details (dict) - stored definition(s) metadata.

            A way you might use me is

            >>> definition_details = client.repository.get_definition_details(definition_uid)
            >>> definition_details = client.repository.get_definition_details(definition_uid=definition_uid)
            >>> definition_details = client.repository.get_definition_details()
            >>> definition_details = client.repository.get_definition_details(definition_url=definition_url)
         """
        Repository._validate_type(definition_uid, 'definition_uid', str, False)
        Repository._validate_type(definition_url, 'definition_url', str, False)

        url = self._definition_endpoint

        if definition_uid is None and definition_url is None:
            response_get = requests.get(url, headers=get_headers(self._wml_token))
        else:
            if definition_url is not None:
                if not is_url(definition_url):
                    raise WMLClientError('Failure during getting definition details, invalid url: \'{}\''.format(definition_url))
                else:
                    url = definition_url
            else:
                if not is_uid(definition_uid):
                    raise WMLClientError('Failure during getting definition details, invalid uid: \'{}\''.format(definition_uid))
                else:
                    url = url + '/' + definition_uid
            response_get = requests.get(url, headers=get_headers(self._wml_token))

        return self._handle_response(200, 'getting definition details', response_get)

    def get_experiment_details(self, experiment_uid=None, experiment_url=None):
        """
            Get metadata of stored experiments. If neither experiment uid nor url is specified all experiments metadata is returned.

            Args:
                experiment_uid (str):  stored experiment UID (optional).
                experiment_url (str):  stored experiment URL (optional).

            Returns:
                experiment details (dict) - stored experiment(s) metadata.

            A way you might use me is

            >>> experiment_details = client.repository.get_experiment_details(experiment_uid)
            >>> experiment_details = client.repository.get_experiment_details(experiment_uid=experiment_uid)
            >>> experiment_details = client.repository.get_experiment_details()
            >>> experiment_details = client.repository.get_experiment_details(experiment_url=experiment_url)
         """
        Repository._validate_type(experiment_uid, 'experiment_uid', str, False)
        Repository._validate_type(experiment_url, 'experiment_url', str, False)

        url = self._experiment_endpoint

        if experiment_uid is None and experiment_url is None:
            response_get = requests.get(url, headers=get_headers(self._wml_token))
        else:
            if experiment_url is not None:
                if not is_url(experiment_url):
                    raise WMLClientError('Failure during getting experiment details, invalid url: \'{}\''.format(experiment_url))
                else:
                    url = experiment_url
            else:
                if not is_uid(experiment_uid):
                    raise WMLClientError('Failure during getting experiment details, invalid uid: \'{}\''.format(experiment_uid))
                else:
                    url = url + '/' + experiment_uid
            response_get = requests.get(url, headers=get_headers(self._wml_token))

        return self._handle_response(200, 'getting experiment details', response_get)

    @staticmethod
    def get_model_url(model_details):
        """
            Get url of stored model.

            Args:
                model_details (dict):  stored model details.

            Returns:
                url (str) - url to stored model.

            A way you might use me is

            >>> model_url = client.repository.get_model_url(model_details)
        """
        Repository._validate_type(model_details, 'model_details', object, True)

        return WMLResource._get_required_element_from_dict(model_details, 'model_details', ['metadata', 'url'])

    @staticmethod
    def get_model_uid(model_details):
        """
            Get uid of stored model.

            Args:
                model_details (dict):  stored model details.

            Returns:
                uid (str) - uid of stored model.

            A way you might use me is

            >>> model_uid = client.repository.get_model_uid(model_details)
        """
        Repository._validate_type(model_details, 'model_details', object, True)

        return WMLResource._get_required_element_from_dict(model_details, 'model_details', ['metadata', 'guid'])

    @staticmethod
    def get_definition_url(definition_details):
        """
            Get url of stored definition.

            Args:
                definition_details (dict):  stored definition details.

            Returns:
                url (str) - url of stored definition.

            A way you might use me is

            >>> definition_url = client.repository.get_definition_url(definition_details)
        """
        Repository._validate_type(definition_details, 'definition_details', object, True)

        return WMLResource._get_required_element_from_dict(definition_details, 'definition_details', ['metadata', 'url'])

    @staticmethod
    def get_definition_uid(definition_details):
        """
            Get uid of stored model.

            Args:
                definition_details (dict):  stored definition details.

            Returns:
                uid (str) - uid of stored model.

            A way you might use me is

            >>> definition_uid = client.repository.get_definition_uid(definition_details)
        """
        Repository._validate_type(definition_details, 'definition_details', object, True)

        return WMLResource._get_required_element_from_dict(definition_details, 'definition_details', ['metadata', 'guid'])

    @staticmethod
    def get_experiment_uid(experiment_details):
        """
            Get uid of stored experiment.

            Args:
                experiment_details (dict):  stored experiment details.

            Returns:
                uid (str) - uid of stored experiment.

            A way you might use me is

            >>> experiment_uid = client.repository.get_experiment_uid(experiment_details)
        """
        Repository._validate_type(experiment_details, 'experiment_details', object, True)

        return WMLResource._get_required_element_from_dict(experiment_details, 'experiment_details', ['metadata', 'guid'])

    @staticmethod
    def get_experiment_url(experiment_details):
        """
            Get url of stored experiment.

            Args:
                experiment_details (dict):  stored experiment details.

            Returns:
                url (str) - url of stored experiment.

            A way you might use me is

            >>> experiment_url = client.repository.get_experiment_url(experiment_details)
        """
        Repository._validate_type(experiment_details, 'experiment_details', object, True)

        return WMLResource._get_required_element_from_dict(experiment_details, 'experiment_details', ['metadata', 'url'])

    def list(self):
        """
           List stored models, definitions and experiments.

           A way you might use me is

           >>> client.repository.list()
        """
        from tabulate import tabulate

        headers = get_headers(self._wml_token)

        with Pool(processes=4) as pool:
            model_get = pool.apply_async(Repository._get, (self._instance_details.get('entity').get('published_models').get('url'), headers))
            definition_get = pool.apply_async(Repository._get, (self._definition_endpoint, headers))
            experiment_get = pool.apply_async(Repository._get, (self._experiment_endpoint, headers))

            model_resources = json.loads(model_get.get().text)['resources']
            definition_resources = json.loads(definition_get.get().text)['resources']
            # experiment_resources = json.loads(experiment_get.get().text)['resources']

        model_values = [(m['metadata']['guid'], m['entity']['name'], m['metadata']['created_at'], m['entity']['model_type'], 'model') for m in model_resources]
        # experiment_values = [(m['metadata']['guid'], m['entity']['settings']['name'], m['metadata']['created_at'], '-', 'experiment') for m in experiment_resources]
        # TODO will be changed to camel case - then, only one line from existing should remain
        try:
            definition_values = [(m['metadata']['guid'], m['entity']['name'], m['metadata']['createdAt'], m['entity']['framework']['name'], 'definition') for m in definition_resources]
        except:
            definition_values = [(m['metadata']['guid'], m['entity']['name'], m['metadata']['created_at'], m['entity']['framework']['name'], 'definition') for m in definition_resources]

        # TODO values = sorted(list(set(model_values + definition_values + experiment_values)), key=lambda x: x[4])
        values = sorted(list(set(model_values + definition_values)), key=lambda x: x[4])
        table = tabulate([["GUID", "NAME", "CREATED", "FRAMEWORK", "TYPE"]] + values)
        print(table)

    @staticmethod
    def _get(url, headers):
        return requests.get(url, headers=headers)

    def _check_artifact_type(self, artifact_uid):
        Repository._validate_type(artifact_uid, 'artifact_uid', object, True)
        is_model = False
        is_definition = False
        is_experiment = False

        with Pool(processes=4) as pool:
            definition_future = pool.apply_async(self._get, (
                self._definition_endpoint + '/' + artifact_uid,
                get_headers(self._wml_token)
            ))
            model_future = pool.apply_async(self._get, (
                self._instance_details.get('entity').get('published_models').get('url') + "/" + artifact_uid,
                get_headers(self._wml_token)
            ))
            experiment_future = pool.apply_async(self._get, (
                self._experiment_endpoint + "/" + artifact_uid,
                get_headers(self._wml_token)
            ))
            response_definition_get = definition_future.get()
            response_model_get = model_future.get()
            response_experiment_get = experiment_future.get()

        self.logger.debug('Response({})[{}]: {}'.format(self._definition_endpoint + '/' + artifact_uid, response_definition_get.status_code, response_definition_get.text))
        self.logger.debug('Response({})[{}]: {}'.format(self._instance_details.get('entity').get('published_models').get('url') + "/" + artifact_uid, response_model_get.status_code, response_model_get.text))
        self.logger.debug('Response({})[{}]: {}'.format(self._experiment_endpoint + "/" + artifact_uid, response_experiment_get.status_code, response_experiment_get.text))

        if response_model_get.status_code == 200:
            is_model = True
            return {'definition': is_definition, 'model': is_model, 'experiment': is_experiment}
        elif response_definition_get.status_code == 200:
            is_definition = True
            return {'definition': is_definition, 'model': is_model, 'experiment': is_experiment}
        elif response_experiment_get.status_code == 200:
            is_experiment = True
            return {'definition': is_definition, 'model': is_model, 'experiment': is_experiment}
        else:
            return {'definition': is_definition, 'model': is_model, 'experiment': is_experiment}
