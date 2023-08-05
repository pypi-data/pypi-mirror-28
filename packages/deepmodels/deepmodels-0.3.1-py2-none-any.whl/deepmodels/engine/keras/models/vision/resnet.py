"""Keras version of ResNet model.
"""

import numpy as np

import cv2

from keras.models import Model, load_model
from keras.applications import resnet50

from deepmodels.core import commons
from deepmodels.core.models.vision import resnet
from deepmodels.engine.keras.models import commons as model_commons


class DMResNetKeras(resnet.DMResNet):
  """Keras implementation of Resnet.
  """
  dmmodel_keras = model_commons.DMModelsKeras()

  def __init__(self, model_type=commons.ModelType.RESNET_50):
    super(DMResNetKeras, self).__init__(model_type)

  def build_model(self, inputs=None, use_fcs=True):
    """Build resnet model.

    Args:
      inputs: input tensor, use None if not specified.
      use_fcs: whether to include fully connected layers.
    """
    if use_fcs:
      # will use (224, 224, 3) as default value.
      input_shape = None
    else:
      input_shape = tuple(self.get_input_shape()[1:])
    if self.model_params.model_type == commons.ModelType.RESNET_50:
      self.model = resnet50.ResNet50(
          input_tensor=inputs,
          input_shape=input_shape,
          weights="imagenet",
          include_top=use_fcs)
    self.model_params.output_layer_names = [self.model.layers[-1].name]
    print "resnet model built"

  def get_layer_names(self):
    layer_names = []
    for layer in self.model.layers:
      layer_names.append(layer.name)
    return layer_names

  def get_preprocess_fn(self):
    """Function taking numpy array as input.

    Apply transformation to any input image to target image format.
    """

    def preprocess_fn(img):
      assert len(img.shape) == 3
      img_height, img_width, img_channels = img.shape
      _, target_height, target_width, _ = self.get_input_shape()
      if img_height != target_height or img_width != target_width:
        img = cv2.resize(img, (target_width, target_height))
      return img * (1. / 255)

    if self.model_params.model_type == commons.ModelType.RESNET_50:
      # return resnet50.preprocess_input
      return preprocess_fn

  def preprocess(self, raw_inputs):
    """Batch preprocess inputs.
    """
    return self.dmmodel_keras.preprocess(raw_inputs, self.get_preprocess_fn())

  def save_model(self, model_fn):
    self.model.save(model_fn)

  def load_model(self, model_fn):
    self.model = load_model(model_fn)
    print "model loaded from: {}".format(model_fn)
