"""Shared utilities for keras models.
"""

import numpy as np


class DMModelsKeras(object):
  """Class with common functions for keras models.
  """

  def preprocess(self, inputs, preprocess_fn):
    """Preprocess all inputs with a function.
    """
    assert type(inputs).__module__ == np.__name__ and len(inputs.shape) == 4
    new_inputs = []
    for cur_input in inputs:
      new_input = preprocess_fn(cur_input)
      new_inputs.append(new_input)
    return np.array(new_inputs)