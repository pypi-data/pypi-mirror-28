"""Template class for image classifier.
"""

import abc

from deepmodels.core.learners.commons import DMLearner
from deepmodels.core.data.vision import img_clf_data
from deepmodels.core.models.commons import DMModel


class DMImgClassifier(DMLearner):
  """Classifier template class.

  Work with general feature input (image or vector).
  """

  def set_dm_data(self, dm_data):
    assert isinstance(dm_data, img_clf_data.ImgClfDataset)
    self.dm_data = dm_data

  def set_dm_model(self, dm_model):
    assert isinstance(dm_model, DMModel)
    self.dm_model = dm_model

  @abc.abstractmethod
  def predict(self, input_data, preprocessed=True):
    """Get prediction value from a tensor.

    Args:
      input_data: raw inputs as numpy array to predict.
      preprocessed: if data has been preprocessed.

    Returns:
      two matrices with each row for each sample and
    ranked label id and probability.
    """
    pass
