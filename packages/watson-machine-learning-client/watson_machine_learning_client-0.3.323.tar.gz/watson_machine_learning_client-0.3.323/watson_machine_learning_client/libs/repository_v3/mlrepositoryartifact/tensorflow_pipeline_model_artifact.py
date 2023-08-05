################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################


from repository_v3.mlrepository import MetaNames
from repository_v3.mlrepository import MetaProps
from repository_v3.mlrepository import ModelArtifact
from repository_v3.mlrepositoryartifact.tensorflow_pipeline_reader import TensorflowPipelineReader
from repository_v3.mlrepositoryartifact.generic_tar_reader import GenericTarGzReader
from repository_v3.mlrepositoryartifact.version_helper import TensorflowVersionHelper
from repository_v3.util.library_imports import LibraryChecker
from repository_v3.base_constants import *
from .python_version import PythonVersion

lib_checker = LibraryChecker()

if lib_checker.installed_libs[TENSORFLOW]:
    import tensorflow as tf

class TensorflowPipelineModelArtifact(ModelArtifact):
    """
    Class of Tensorflow model artifacts created with MLRepositoryCLient.

    """
    def __init__(self,tensorflow_pipeline_model,
                 signature_def_map,
                 tags=None,
                 assets_collection=None,
                 legacy_init_op=None,
                 clear_devices=False,
                 main_op=None,
                 uid=None, name=None, meta_props=MetaProps({}),):
        lib_checker.check_lib(TENSORFLOW)
        super(TensorflowPipelineModelArtifact, self).__init__(uid, name, meta_props)

        if not isinstance(tensorflow_pipeline_model,tf.Session):
            raise TypeError("sess should be of type : %s" % tf.Session)

        self.ml_pipeline_model   = tensorflow_pipeline_model
        self.signature_def_map = signature_def_map
        self.tags = tags
        self.assets_collection = assets_collection
        self.legacy_init_op = legacy_init_op
        self.clear_devices = clear_devices
        self.main_op = main_op

        self.ml_pipeline = None     # no pipeline or parent reference




        if meta_props.prop(MetaNames.RUNTIMES) is None and meta_props.prop(MetaNames.RUNTIME) is None:
            ver = PythonVersion.significant()
            runtimes = '[{"name":"python","version": "'+ ver + '"}]'
            self.meta.merge(
                MetaProps({MetaNames.RUNTIMES: runtimes})
            )

        self.meta.merge(
            MetaProps({
                MetaNames.FRAMEWORK_NAME:   TensorflowVersionHelper.model_type(tensorflow_pipeline_model),
                MetaNames.FRAMEWORK_VERSION: TensorflowVersionHelper.model_version(tensorflow_pipeline_model)
            })
        )

    def pipeline_artifact(self):
        """
        Returns None. Pipeline is not implemented for Tensorflow model.
        """
        pass

    def reader(self):
        """
        Returns reader used for getting pipeline model content.

        :return: reader for TensorflowPipelineModelArtifact.pipeline.Pipeline
        :rtype: TensorflowPipelineReader
        """
        try:
            return self._reader
        except:
            self._reader = TensorflowPipelineReader(self.ml_pipeline_model,
                                                    self.signature_def_map,
                                                    self.tags,
                                                    self.assets_collection,
                                                    self.legacy_init_op,
                                                    self.clear_devices,
                                                    self.main_op)
            return self._reader

    def _copy(self, uid=None, meta_props=None):
        if uid is None:
            uid = self.uid

        if meta_props is None:
            meta_props = self.meta

        return TensorflowPipelineModelArtifact(
            self.ml_pipeline_model,
            self.signature_def_map,
            self.tags,
            self.assets_collection,
            self.legacy_init_op,
            self.clear_devices,
            self.main_op,
            uid=uid,
            name=self.name,
            meta_props=meta_props
        )


class TensorflowPipelineModelTarArtifact(ModelArtifact):
    """
    Class of serialized Tensorflow model artifacts in tar.gz format and created
    with MLRepositoryCLient.

    """
    def __init__(self,
                 tensorflow_tar_artifact,
                 uid=None,
                 name=None,
                 meta_props=MetaProps({}),):
        if not (lib_checker.installed_libs[TENSORFLOW]):
            raise NameError("Please install Tensorflow package and re-execute the command")
        super(TensorflowPipelineModelTarArtifact, self).__init__(uid, name, meta_props)

        self.ml_pipeline_model = tensorflow_tar_artifact
        self.ml_pipeline = None     # no pipeline or parent reference


    def pipeline_artifact(self):
        """
        Returns None. Pipeline is not implemented for Tensorflow model.
        """
        pass

    def reader(self):
        """
        Returns reader used for getting pipeline model content.

        :return: reader for TensorflowPipelineModelArtifact.pipeline.Pipeline
        :rtype: TensorflowPipelineReader
        """
        try:
            return self._reader
        except:
            self._reader = GenericTarGzReader(self.ml_pipeline_model)
            return self._reader

    def _copy(self, uid=None, meta_props=None):
        if uid is None:
            uid = self.uid

        if meta_props is None:
            meta_props = self.meta

        return TensorflowPipelineModelTarArtifact(
            self.ml_pipeline_model,
            uid=uid,
            name=self.name,
            meta_props=meta_props
        )
