"""DeepModels version of VGG16.
"""

import os

from deepmodels.core.models.vision import vgg
from deepmodels.core import commons
from deepmodels.engine.tf.models.vision import model_factory, model_downloader
from deepmodels.engine.tf import base_model


class DMVGGTF(vgg.DMVGG):
  """TensorFlow implementation of VGG.
  """

  def __init__(self, net_type=commons.ModelType.VGG16):
    super(DMVGGTF, self).__init__(net_type)
    if net_type == commons.ModelType.VGG16:
      self.model_params.output_layer_names = ["vgg_16/fc7"]
    if net_type == commons.ModelType.VGG19:
      self.model_params.output_layer_names = ["vgg_19/fc7"]
    self.model_weight_fn = model_factory.get_builtin_net_weights_fn(
        self.model_params.model_type)
    if self.download_pretrained_model and not os.path.exists(
        self.model_weight_fn):
      model_downloader.download_net(self.model_params.model_type)

  def get_input_shape(self):
    return (None, self.model_params.input_img_height,
            self.model_params.input_img_width, 3)

  def build_model(self, inputs):
    logits, endpoints = model_factory.create_builtin_net(
        self.model_params.model_type, inputs, self.model_params.cls_num,
        self.model_params.model_mode)
    return logits, endpoints

  def get_preprocess_fn(self):
    preprocess_fn = model_factory.get_builtin_net_preprocess_fn(
        self.model_params.model_type, self.model_params.model_mode)
    return preprocess_fn

  def preprocess(self, inputs):
    preprocess_fn = self.get_preprocess_fn()
    return model_factory.preprocess(inputs, preprocess_fn,
                                    self.model_params.input_img_height,
                                    self.model_params.input_img_width)

  def print_model(self):
    base_model.print_variable_names()