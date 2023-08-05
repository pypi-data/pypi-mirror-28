"""Shared definition of a model.

Provide an organized structure for deep networks.
We will use existing slim model library so
will not reimplement them here.
"""

import abc
import os

from deepmodels.core import commons
from deepmodels.shared import data_manager


class DMModel(object):
  """Class template for metadata of a base model.

  It contains information regarding the model itself,
  e.g. name, definition, labels etc.
  Used together with a template to simplify process.
  """
  __metaclass__ = abc.ABCMeta

  # model parameters.
  model_params = None
  # model data files.
  model_def_fn = ""
  model_weight_fn = ""
  download_pretrained_model = True
  # exclude scopes when restoring weights
  restore_scope_exclude = []
  # model object.
  model = None

  def __init__(self, model_params):
    """Initialize model.
    """
    # assert isinstance(model_params, commons.ModelParams)
    self.model_params = model_params

  def __del__(self):
    pass

  def print_summary(self):
    """Print model details.
    """
    pass

  @abc.abstractmethod
  def get_layer_names(self):
    """Return a list of layer names.
    """
    pass

  @abc.abstractmethod
  def get_input_shape(self):
    """Return the shape of inputs.

    First dimension should be the batch size and
    set to None.
    """
    pass

  @abc.abstractmethod
  def build_model(self, inputs):
    """Define learning model.
    """
    pass

  @abc.abstractmethod
  def get_preprocess_fn(self):
    """Obtain a corresponding preprocess function.
    """
    pass

  @abc.abstractmethod
  def preprocess(self, raw_inputs):
    """Perform preprocess.

    Args:
      raw_inputs: raw input to the model.
    Returns:
      preprocessed input data.
    """
    pass

  def save_model(self, model_fn):
    pass

  def load_model(self, model_fn):
    pass
