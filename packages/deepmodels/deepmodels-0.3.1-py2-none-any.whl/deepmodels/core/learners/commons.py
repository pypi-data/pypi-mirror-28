"""Base class for learners in deepmodels.
"""

import abc

from deepmodels.core import commons
from deepmodels.core.data import commons as data_common
from deepmodels.core.models import commons as model_common


class DMLearner(object):
  """Base class for deepmodels learners.

  Attributes:
    input_tensor_name: name of input tensor, can be set to a custom name.
    output_tensor_name: name of output tensor.
    vars_to_train: variables to train.
    vars_to_restore: variables to restore from a model file.
  """
  __metaclass__ = abc.ABCMeta

  input_var_name = ""
  output_var_names = []
  vars_to_train = None
  vars_to_restore = None
  dm_model = None
  dm_data = None

  def __init__(self, dm_model_, dm_data_):
    """Initialization.

    Args:
      dm_model_: deep model object.
      dm_data_: dataset object.
    """
    self.set_dm_model(dm_model_)
    self.set_dm_data(dm_data_)

  @abc.abstractmethod
  def start(self):
    """Start the learner.

    After calling this method, other methods should be available to use.
    """
    pass

  @abc.abstractmethod
  def set_dm_model(self, dm_model):
    """Use a dm model object.

    Check model type.
    """
    pass

  @abc.abstractmethod
  def set_dm_data(self, dm_data):
    """Use a dm data object.

    Check data type.
    """
    pass

  # TODO(jiefeng): not all learners need labels, e.g. gan.
  @abc.abstractmethod
  def compute_losses(self, gt_labels, pred_logits):
    """Compute classification loss given labels and predictions.

    Args:
      gt_labels: ground truth labels in one-hot encoding.
      pred_logits: prediction logits.

    Returns:
      computed loss tensor.
    """
    pass

  @abc.abstractmethod
  def get_outputs(self, input_data, output_layer_name, preprocessed=False):
    """Compute outputs from a specified layer.

    Args:
      input_data: input data for estimation.
      output_layer_name: which layer to compute output.
      preprocessed: if the data has been preprocessed.
    
    Returns:
      output values.
    """
    pass

  @abc.abstractmethod
  def train(self, train_params):
    pass

  def train_batch(self, batch_data):
    """Train a batch of samples.
    """
    pass

  @abc.abstractmethod
  def test(self, test_params):
    pass
