from sklearn import preprocessing
#import primitive
import sys
import os
#sys.path.append('corex_topic/')
from corextext.corextext.corex_topic import Corex
#import corex_topic.corex_topic as corex_text
from collections import defaultdict, OrderedDict
from scipy import sparse
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import numpy as np

import d3m_metadata.container as container
import d3m_metadata.hyperparams as hyperparams
import d3m_metadata.params as params
from d3m_metadata.metadata import PrimitiveMetadata

from primitive_interfaces.unsupervised_learning import UnsupervisedLearnerPrimitiveBase
from primitive_interfaces.base import CallResult
#from primitive_interfaces.params import Params
from d3m_metadata.hyperparams import Uniform, UniformInt, Union, Enumeration

from typing import NamedTuple,Optional, Sequence

import inspect
import typing

Input = container.DataFrame
Output = container.DataFrame

class CorexText_Params(params.Params):
    model: typing.Union[Corex, None]
    bow: typing.Union[TfidfVectorizer, None]
    get_text: bool 
    data_path: str
    #fitted: bool = False
    #training_inputs: Input = None
    # add support for resuming training / storing model information


class CorexText_Hyperparams(hyperparams.Hyperparams):
    n_hidden = Uniform(lower = 0, upper = 100, default = 10, q = 1, description = 'number of topics')
    max_df = Uniform(lower = .10, upper = 1.01, default = .9, q = .05, description = 'max percent document frequency of analysed terms')
    min_df = Union(OrderedDict([('int df' , Uniform(lower = 1, upper = 20, default = 2, q = 1, description = 'min integer document frequency of analysed terms')),
            ('pct df' , Uniform(lower = 0, upper = .10, default = .01, q = .01, description = 'min percent document frequency of analysed terms'))]), 
            default = 'int df')
    max_features = Union(OrderedDict([('none', Enumeration([None], default = None)), 
                ('int mf', Uniform(lower = 1000, upper = 50001, default = 50000, q = 1000, description = 'max number of terms to use'))]),
                default = 'none')


class CorexText(UnsupervisedLearnerPrimitiveBase[Input, Output, CorexText_Params, CorexText_Hyperparams]):  #(Primitive):
    """
    Learns latent factors / topics which explain the most multivariate information in bag of words representations of documents. Returns learned topic scores for each document. Also supports hierarchical models and 'anchoring' to encourage topics to concentrate around desired words.
    """
    metadata = PrimitiveMetadata({
          "schema": "v0",
          "id": "18e63b10-c5b7-34bc-a670-f2c831d6b4bf",
          "version": "0.2.3",
          "name": "corextext.corex_text.CorexText",
          "description": "Learns latent factors / topics which explain the most multivariate information in bag of words representations of documents. Returns learned topic scores for each document. Also supports hierarchical models and 'anchoring' to encourage topics to concentrate around desired words.",
          "python_path": "d3m.primitives.corex_text.CorexText",
          "original_python_path": "corextext.corex_text.CorexText",
          "source": {
              "name": "ISI",
              "contact": "mailto:brekelma@usc.edu",
              "uris": ["https://github.com/brekelma/corextext.git"]
              },

          "installation": [
            {
              "type":"PIP",
              "package":"corextext",
              "version":"0.2.3"
            }
            ],
          "algorithm_types": ["EXPECTATION_MAXIMIZATION_ALGORITHM", "LATENT_DIRICHLET_ALLOCATION"],
          "primitive_family": "FEATURE_CONSTRUCTION",
          "hyperparams_to_tune": ["n_hidden", "max_df", "min_df"]
        })
        #"preconditions": [],
    #      "effects": [],


    def __init__(self, *, hyperparams : CorexText_Hyperparams, random_seed : int =  0, docker_containers: typing.Dict[str, str] = None) -> None:

        super().__init__(hyperparams = hyperparams, random_seed = random_seed, docker_containers = docker_containers)
        
         
    def fit(self, *, timeout : float = None, iterations : int = None) -> CallResult[None]: #X : Sequence[Input]): 
        #self.columns = list(X)
        #X_ = X[self.columns].values # useless if only desired columns are passed
        if self.fitted:
            return

        if not hasattr(self, 'model') or self.model is None:
            self.model = Corex(n_hidden= self.hyperparams['n_hidden'], max_iter = iterations, seed = self.random_seed)#, **kwargs)

        if not hasattr(self, 'training_inputs'):
            raise ValueError("Missing training data.")

        if not hasattr(self, 'get_text'):
            raise ValueError("Missing get_text parameter")
        else:
            if not self.get_text:
                self.bow = TfidfVectorizer(input = 'content', decode_error='ignore', max_df = self.hyperparams['max_df'], min_df = self.hyperparams['min_df'], max_features = self.hyperparams['max_features'])
            else:
                self.bow = TfidfVectorizer(input = 'filename', max_df = self.hyperparams['max_df'], min_df = self.hyperparams['min_df'], max_features = self.hyperparams['max_features'])


        if iterations is not None:
            self.max_iter = iterations
            self.model.max_iter = self.max_iter
        else:
            self.max_iter = 250
            self.model.max_iter = self.max_iter

        bow = self.bow.fit_transform(self.training_inputs.values.ravel()) if not self.get_text else self.bow.fit_transform(self._get_raw_inputs())
        self.latent_factors = self.model.fit_transform(bow)
        self.fitted = True
        return CallResult(None, True, self.max_iter)


    def produce(self, *, inputs : Input, timeout : float = None, iterations : int = None) -> CallResult[Output]: # TAKES IN DF with index column
        #self.columns = list(X)
        #X_ = X[self.columns].values # useless if only desired columns are passed
        if iterations is not None:
            self.max_iter = iterations
            self.model.max_iter = self.max_iter
        else:
            self.max_iter = 250
            self.model.max_iter = self.max_iter

        if not self.fitted:
            bow = self.bow.fit_transform(inputs.values.ravel()) if not self.get_text else self.bow.fit_transform(self._get_raw_inputs(inputs = inputs, data_path = self.data_path))
            self.latent_factors = self.model.fit_transform(bow).astype(float)
            self.fitted = True
        else:
            bow = self.bow.transform(inputs.values.ravel()) if not self.get_text else self.bow.transform(self._get_raw_inputs(inputs = inputs, data_path = self.data_path))
            self.latent_factors = self.model.transform(bow).astype(float)

        # TO DO : Incorporate timeout, max_iter
        return CallResult(self.latent_factors, True, self.max_iter)

    def _fit_transform(self, inputs : Input, timeout : float = None, iterations : int = None) -> Sequence[Output]: # TAKES IN DF with index column
        #self.columns = list(X)
        #X_ = X[self.columns].values # useless if only desired columns are passed


        if iterations is not None:
            self.max_iter = iterations
            self.model.max_iter = self.max_iter

        bow = self.bow.fit_transform(inputs.values.ravel()) if not self.get_text else self.bow.fit_transform(self._get_raw_inputs(inputs = inputs))
        self.latent_factors = self.model.fit_transform(bow)
        self.fitted = True
        return self.latent_factors

    def _get_raw_inputs(self, inputs : Input = None, data_path = None) -> np.ndarray:
        print_ = True
        raw_inputs = self.training_inputs.values if inputs is None else inputs.values
        inp = self.training_inputs.values if inputs is None else inputs.values
        if data_path is not None:
            for idx, val in np.ndenumerate(inp):
                raw_inputs[idx] = os.path.join(data_path, val)
        elif self.data_path is not None:
            for idx, val in np.ndenumerate(inp):
                raw_inputs[idx] = os.path.join(self.data_path, val)
        else:
            warn('Data_path param not passed.')
        
        return raw_inputs.ravel()
    

    def set_training_data(self, *, inputs : Input) -> None:
        self.training_inputs = inputs
        self.fitted = False

    def get_params(self) -> CorexText_Params:
        return CorexText_Params(model = self.model, bow = self.bow, get_text = self.get_text, data_path = self.data_path)
                                #fitted = self.fitted, training_inputs = self.training_inputs)

    def set_params(self, *, params: CorexText_Params) -> None:
        self.model = params['model']
        self.bow = params['bow']
        self.get_text = params['get_text']
        self.data_path = params['data_path']
        #self.fitted = params.fitted
        #self.training_inputs = params.training_inputs

    def _annotation(self):
        if self._annotation is not None:
            return self._annotation
        self._annotation = Primitive()
        self._annotation.name = 'CorexText'
        self._annotation.task = 'FeatureExtraction'
        self._annotation.learning_type = 'UnsupervisedLearning'
        self._annotation.ml_algorithm = ['Dimension Reduction']
        self._annotation.tags = ['feature_extraction', 'text']
        return self._annotation

    def _get_feature_names(self):
        return ['CorexText_'+ str(i) for i in range(self.hyperparams['n_hidden'])]
