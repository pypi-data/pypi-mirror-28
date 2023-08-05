"""Keras implementation of standard gan.
"""

from deepmodels.core.models.vision.commons import DMGANModel


class DMGANKeras(DMGANModel):
  """Keras implementation.
  """

  def __init__(self, model_params=None):
    super(DMGANKeras, self).__init__()

  def build_generator(self, inputs=None):
    pass

  def build_discriminator(self, inputs=None):
    pass
