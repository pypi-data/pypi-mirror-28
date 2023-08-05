"""Keras implementation of DCGAN.
"""

import numpy as np

from keras.layers import Input, Dense, Reshape, Flatten, Dropout
from keras.layers import BatchNormalization, Activation, ZeroPadding2D
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.convolutional import UpSampling2D, Conv2D
from keras.models import Sequential, Model

from deepmodels.core import commons
from deepmodels.core.models.vision.commons import DMGANModel
from deepmodels.engine.keras.models.commons import DMModelsKeras


class DMDCGANKeras(DMGANModel):
  """Keras implementation.
  """
  dmmodel_keras = DMModelsKeras()

  def __init__(self, model_params):
    super(DMDCGANKeras, self).__init__(model_params)

  def build_generator(self, inputs=None):
    noise_shape = (100, )
    model = Sequential()
    # 7 for 32, 8 for 64
    model.add(Dense(128 * 8 * 8, activation="relu", input_shape=noise_shape))
    model.add(Reshape((8, 8, 128)))
    model.add(BatchNormalization(momentum=0.8))
    model.add(UpSampling2D())
    model.add(Conv2D(128, kernel_size=3, padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(momentum=0.8))
    model.add(UpSampling2D())
    model.add(Conv2D(64, kernel_size=3, padding="same"))
    model.add(Activation("relu"))
    model.add(BatchNormalization(momentum=0.8))
    # added
    # 64x64
    # model.add(UpSampling2D())
    model.add(Conv2D(self.img_shape[2], kernel_size=3, padding="same"))
    # make sure output has same value range as input (-1, 1)
    model.add(Activation("tanh"))
    model.summary()
    noise = Input(shape=noise_shape)
    img = model(noise)
    self.generator = Model(noise, img)

  def build_discriminator(self, inputs=None):
    model = Sequential()
    model.add(
        Conv2D(
            32,
            kernel_size=3,
            strides=2,
            input_shape=self.img_shape,
            padding="same"))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dropout(0.25))
    model.add(Conv2D(64, kernel_size=3, strides=2, padding="same"))
    model.add(ZeroPadding2D(padding=((0, 1), (0, 1))))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dropout(0.25))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Conv2D(128, kernel_size=3, strides=2, padding="same"))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dropout(0.25))
    model.add(BatchNormalization(momentum=0.8))
    model.add(Conv2D(256, kernel_size=3, strides=1, padding="same"))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    model.summary()
    img = Input(shape=self.img_shape)
    validity = model(img)
    self.discriminator = Model(img, validity)

  def build_model(self, inputs=None):
    self.build_generator()
    self.build_discriminator()
    # build combined model for training generator.
    z = Input(shape=(100, ))
    generated_img = self.generator(z)
    gen_pred = self.discriminator(generated_img)
    self.model = Model(z, gen_pred)
    self.model.summary()

  def get_preprocess_fn(self):
    def preprocess_fn(raw_inputs):
      """Normalize input.
      """
      return (raw_inputs.astype(np.float32) - 127.5) / 127.5

    return preprocess_fn

  def preprocess(self, raw_inputs):
    return self.dmmodel_keras.preprocess(raw_inputs, self.get_preprocess_fn())
