"""Template class for image generators.
"""

import abc

from deepmodels.core.learners.commons import DMLearner
from deepmodels.core.data.vision import img_gen_data
from deepmodels.core.models.vision.commons import DMGANModel


class DMImgGAN(DMLearner):
  """Image generator template class.
  """

  def set_dm_data(self, dm_data):
    assert isinstance(dm_data, img_gen_data.ImgGenDataset)
    self.dm_data = dm_data

  def set_dm_model(self, dm_model):
    assert isinstance(dm_model, DMGANModel)
    self.dm_model = dm_model

  @abc.abstractmethod
  def generate_imgs(self, num):
    """Return a generated image from the model.
    """
    pass
