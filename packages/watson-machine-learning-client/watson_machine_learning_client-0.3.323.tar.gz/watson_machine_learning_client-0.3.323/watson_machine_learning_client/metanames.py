################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################
from repository_v3.mlrepository import MetaNames
from tabulate import tabulate


class ExperimentMetaNames:
    def __init__(self):
        self.NAME = "name"
        self.DESCRIPTION = "description"
        self.AUTHOR_NAME = "author_name"
        self.AUTHOR_EMAIL = "author_email"
        self.OPTIMIZATION_METHOD = "hyper_parameters_optimization"
        self.OPTIMIZATION_PARAMETERS = "parameters"
        self.EVALUATION_METHOD = "method"
        self.EVALUATION_METRIC = "metric_name"
        self.TRAINING_REFERENCES = "training_references"
        self.TRAINING_DATA_REFERENCE = "training_data_reference"
        self.TRAINING_RESULTS_REFERENCE = "training_results_reference"

    def get(self):
        return list(self.__dict__.keys())


class TrainingConfigurationMetaNames:

    def __init__(self):
        self.NAME = "name"
        self.DESCRIPTION = "description"
        self.AUTHOR_NAME = "author_name"
        self.AUTHOR_EMAIL = "author_email"
        self.FRAMEWORK_NAME = "framework_name"
        self.FRAMEWORK_VERSION = "framework_version"
        # TODO needed when bug fixed
        #self.RUNTIME_NAME = "runtime_name"
        #self.RUNTIME_VERSION = "runtime_version"
        self.TRAINING_DATA_REFERENCE = "training_data"
        self.TRAINING_RESULTS_REFERENCE = "training_results"
        self.EXECUTION_COMMAND = "command"
        self.EXECUTION_RESOURCE_SIZE = "resource"

    def get(self):
        return list(self.__dict__.keys())

    def show(self):
        training_data_reference = {
            "connection": {
                "auth_url": "https://identity.open.softlayer.com/v3",
                "user_name": "xxx",
                "password": "xxx",
                "region": "dallas",
                "domain_name": "xxx",
                "project_id": "xxx"
            },
            "source": {
                "bucket": "train-data"
            },
            "type": "bluemix_objectstore"
        }

        table = tabulate(
            [
                ["META_PROP NAME", "TYPE", "EXAMPLE VALUE"],
                [self.NAME, "str", "Hand-written Digit Recognition"],
                [self.DESCRIPTION, "str", "Hand-written Digit Recognition training"],
                [self.AUTHOR_NAME, "str", "John Smith"],
                [self.AUTHOR_EMAIL, "str", "John.Smith@x.x"],
                [self.FRAMEWORK_NAME, "str", "tensorflow"],
                [self.FRAMEWORK_VERSION, "str", "1.2-py3"],
                # TODO needed when bug fixed
                #[self.RUNTIME_NAME, "str", "python"],
                #[self.RUNTIME_VERSION, "str", "3.5"],
                [self.TRAINING_DATA_REFERENCE, "json", training_data_reference],
                [self.TRAINING_RESULTS_REFERENCE, "json", training_data_reference],
                [self.EXECUTION_COMMAND, "str", "python3 tensorflow_mnist_softmax.py --trainingIters 20"],
                [self.EXECUTION_RESOURCE_SIZE, "str", "small"]
            ]
        )
        print(table)


class ModelDefinitionMetaNames:

    def __init__(self):
        self.NAME = "name"
        self.DESCRIPTION = "description"
        self.AUTHOR_NAME = "author_name"
        self.AUTHOR_EMAIL = "author_email"
        self.FRAMEWORK_NAME = "framework_name"
        self.FRAMEWORK_VERSION = "framework_version"
        self.RUNTIME_NAME = "runtime_name"
        self.RUNTIME_VERSION = "runtime_version"
        self.EXECUTION_COMMAND = "command"

    def get(self):
        return list(self.__dict__.keys())

    def show(self):
        table = tabulate(
            [
                ["META_PROP NAME", "TYPE", "EXAMPLE VALUE"],
                [self.NAME, "str", "my_training_definition"],
                [self.DESCRIPTION, "str", "my_description"],
                [self.AUTHOR_NAME, "str", "John Smith"],
                [self.AUTHOR_EMAIL, "str", "John.Smith@x.x"],
                [self.FRAMEWORK_NAME, "str", "tensorflow"],
                [self.FRAMEWORK_VERSION, "str", "1.2-py3"],
                [self.RUNTIME_NAME, "str", "python"],
                [self.RUNTIME_VERSION, "str", "3.5"],
                [self.EXECUTION_COMMAND, "str", "python3 tensorflow_mnist_softmax.py --trainingIters 20"]
            ]
        )
        print(table)


class ModelMetaNames:

    def __init__(self):
        self.NAME = "name"
        self.DESCRIPTION = MetaNames.DESCRIPTION
        self.AUTHOR_NAME = MetaNames.AUTHOR_NAME
        self.AUTHOR_EMAIL = MetaNames.AUTHOR_EMAIL
        self.FRAMEWORK_NAME = MetaNames.FRAMEWORK_NAME
        self.FRAMEWORK_VERSION = MetaNames.FRAMEWORK_VERSION
        self.RUNTIME_NAME = "runtime_name"
        self.RUNTIME_VERSION = "runtime_version"

    def get(self):
        return list(self.__dict__.keys())

    def show(self):
        table = tabulate(
            [
                ["META_PROP NAME", "TYPE", "EXAMPLE VALUE"],
                [self.NAME, "str", "my_model"],
                [self.DESCRIPTION, "str", "my_description"],
                [self.AUTHOR_NAME, "str", "John Smith"],
                [self.AUTHOR_EMAIL, "str", "John.Smith@x.x"],
                [self.FRAMEWORK_NAME, "str", "tensorflow"],
                [self.FRAMEWORK_VERSION, "str", "1.2-py3"],
                [self.RUNTIME_NAME, "str", "python"],
                [self.RUNTIME_VERSION, "str", "3.5"]
            ]
        )
        print(table)
