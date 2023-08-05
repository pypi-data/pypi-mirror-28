"""Keras version of MobileNet model.
"""

import numpy as np

from keras.models import Model, load_model
from keras.applications import mobilenet as keras_mobilenet

from deepmodels.core import commons
from deepmodels.core.models.vision import mobilenet
from deepmodels.engine.keras.models import commons as model_commons


class DMMobileNetKeras(mobilenet.DMMobileNet):
  """Keras implementation of MobileNet.
  """
  dmmodel_keras = model_commons.DMModelsKeras()

  def __init__(self):
    super(DMMobileNetKeras, self).__init__()

  def build_model(self, inputs=None, use_fcs=True):
    """Build mobilenet model.

    Args:
      inputs: input tensor, use None if not specified.
      use_fcs: whether to include fully connected layers.
    """
    if use_fcs:
      input_shape = None
    else:
      input_shape = tuple(self.get_input_shape()[1:])
    self.model = keras_mobilenet.MobileNet(
        input_tensor=inputs,
        input_shape=input_shape,
        weights="imagenet",
        include_top=use_fcs)
    self.model_params.output_layer_names = [self.model.layers[-1].name]
    print "mobilenet model built"

  def get_layer_names(self):
    layer_names = []
    for layer in self.model.layers:
      layer_names.append(layer.name)
    return layer_names

  def get_preprocess_fn(self):
    """Function taking numpy array as input.
    """

    def preprocess_fn(img):
      assert len(img.shape) == 3
      img_height, img_width, img_channels = img.shape
      _, target_height, target_width, _ = self.get_input_shape()
      if img_height != target_height or img_width != target_width:
        img = cv2.resize(img, (target_width, target_height))
      return img * (1. / 255)

    return preprocess_fn

  def preprocess(self, raw_inputs):
    """Batch preprocess inputs.
    """
    return self.dmmodel_keras.preprocess(raw_inputs, self.get_preprocess_fn())

  def save_model(self, model_fn):
    self.model.save(model_fn)

  def load_model(self, model_fn):
    self.model = load_model(
        model_fn,
        custom_objects={
            "relu6": mobilenet.relu6,
            "DepthwiseConv2D": mobilenet.DepthwiseConv2D
        })
    print "model loaded from: {}".format(model_fn)
