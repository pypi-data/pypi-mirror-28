"""Test tf vision models.
"""

from deepmodels.core import commons
from deepmodels.engine.tf.models.vision import vgg
from deepmodels.engine.tf.models.vision import model_downloader


class TestTFVisionModels(object):
  def test_vgg(self):
    model = vgg.DMVGGTF()
    assert True

  def test_download(self):
    model_downloader.download_net(commons.ModelType.VGG19)
    assert True
