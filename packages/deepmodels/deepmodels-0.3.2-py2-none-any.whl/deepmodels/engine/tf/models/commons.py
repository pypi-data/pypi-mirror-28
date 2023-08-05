"""Shared definition of deep models.

Provide an organized structure for deep networks.
We will use existing slim model library so
will not reimplement them here.
"""

import os

import numpy as np
import tensorflow as tf

from deepmodels.tf.core import commons
from deepmodels.shared import data_manager


class NetworkDM(object):
  """Class template for metadata of a network.

  It contains information regarding the model itself,
  e.g. name, definition, labels etc.
  Good to be used together with a template to simplify process.
  """

  # model graph.
  graph = tf.Graph()
  # network parameters.
  net_params = commons.ModelParams()
  # network data files.
  net_graph_fn = ""
  net_weight_fn = ""
  download_pretrained_model = False
  # exclude scopes when restoring weights
  restore_scope_exclude = []
  # mapping from predicted label to name string.
  net_label_names = {}

  def __init__(self, model_params=None):
    """Initialize model.
    """
    if model_params is not None:
      self.net_params = model_params

  def __del__(self):
    if tf.get_default_graph() is self.graph:
      tf.reset_default_graph()

  def use_graph(self):
    """Use model graph as default tf graph.
    """
    assert self.graph is not None, "model graph is none"
    if tf.get_default_graph() is not self.graph:
      self.graph.as_default()
      print "using {} graph".format(self.net_params.model_name)

  # TODO(jiefeng): how to recover original tf graph as default.
  def reset_graph(self):
    """Reset current graph to default global graph.
    """
    tf.get_default_graph().as_default()

  def config_model(self, cls_num=None, mode=None):
    """Set model parameters.

    Args:
      cls_num: class number for classification.
      mode: train, val or test.
    """
    if cls_num != None:
      self.net_params.cls_num = cls_num
    if mode != None:
      self.net_params.model_mode = mode

  def build_model(self, inputs, learner_type=commons.LearnerType.Classifier):
    """Define network model.
    """
    if learner_type == commons.LearnerType.Classifier:
      logits, endpoints = create_builtin_net(self.net_params.model_type,
                                             inputs, self.net_params.cls_num,
                                             self.net_params.model_mode)
      return logits, endpoints
    else:
      raise ValueError("only classifier is supported.")

  def get_preprocess_fn(self):
    """Obtain a corresponding preprocess function.
    """
    preprocess_fn = get_builtin_net_preprocess_fn(self.net_params.model_type,
                                                  self.net_params.model_mode)
    return preprocess_fn

  def preprocess(self, inputs):
    """Perform preprocess.

    Args:
      inputs: raw input to the model.
    Returns:
      preprocessed input data.
    """
    preprocess_fn = self.get_preprocess_fn()
    assert inputs.ndim == 3 or inputs.ndim == 4, "invalid image format for preprocessing"
    if inputs.ndim == 3:
      inputs = np.expand_dims(inputs, axis=0)
    with tf.Graph().as_default() as cur_g:
      input_tensor = tf.convert_to_tensor(inputs, dtype=tf.uint8)
      all_inputs = tf.unstack(input_tensor)
      processed_inputs = []
      for cur_input in all_inputs:
        new_input = preprocess_fn(cur_input, self.net_params.input_img_height,
                                  self.net_params.input_img_width)
        processed_inputs.append(new_input)
      new_inputs = tf.stack(processed_inputs)
      with tf.Session(graph=cur_g) as sess:
        processed_inputs = sess.run(new_inputs)
    return processed_inputs

  def get_label_names(self):
    """Obtain corresponding label names.

    Return dictionary mapping label to string name.
    """
    pass
