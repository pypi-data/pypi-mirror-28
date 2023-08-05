"""Keras implementation of GAN.
"""

import math
import os
import time

import numpy as np

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from keras import optimizers
from keras.models import Model as KerasModel
from keras.optimizers import Adam

from deepmodels.core import commons
from deepmodels.core.learners import dm_gan
from deepmodels.engine.keras.data.vision import img_gen_data


class DMImgGANKeras(dm_gan.DMImgGAN):
  """Keras class of GAN.
  """

  def set_dm_data(self, dm_data):
    assert isinstance(dm_data, img_gen_data.ImgGenDatasetKeras)
    self.dm_data = dm_data

  def start(self):
    assert self.dm_model is not None
    assert self.dm_data is not None

  def compute_losses(self, gt_labels, pred_logits):
    pass

  def get_outputs(self, input_data, output_layer_name, preprocessed=False):
    pass

  def train(self, train_params):
    # get data.
    input_shape = self.dm_model.get_input_shape()
    print "dm model input shape: {}".format(input_shape)
    data_generator = self.dm_data.gen_batch_data(
        data_type=commons.DataType.TRAIN,
        batch_size=32,
        target_img_height=input_shape[0],
        target_img_width=input_shape[1],
        preprocess_fn=self.dm_model.get_preprocess_fn())
    # build model.
    self.dm_model.build_model(None)
    # compile models.
    optimizer = Adam(0.0002, 0.5)
    # only train generator in the whole model.
    self.dm_model.generator.compile(
        loss="binary_crossentropy", optimizer=optimizer)
    self.dm_model.discriminator.compile(
        loss="binary_crossentropy", optimizer=optimizer, metrics=["accuracy"])
    self.dm_model.discriminator.trainable = False
    self.dm_model.model.compile(
        loss="binary_crossentropy", optimizer=optimizer)
    # start training.
    save_dir = os.path.join(train_params.log_dir, "sample_imgs")
    for epoch in range(train_params.max_epochs):
      """Train discriminator.
      """
      for batch_id in range(train_params.batch_num_per_epoch):
        img_batch = next(data_generator)
        batch_size = img_batch.shape[0]
        # Sample noise and generate a batch of new images
        noise = np.random.normal(0, 1, (batch_size, 100))
        gen_imgs = self.dm_model.generator.predict(noise)
        # Train the discriminator (real classified as ones and generated as zeros)
        d_loss_real = self.dm_model.discriminator.train_on_batch(
            img_batch, np.ones((batch_size, 1)))
        d_loss_fake = self.dm_model.discriminator.train_on_batch(
            gen_imgs, np.zeros((batch_size, 1)))
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
        """Train generator.
        """
        noise = np.random.normal(0, 1, (batch_size, 100))
        # Train the generator (wants discriminator to mistake images as real)
        g_loss = self.dm_model.model.train_on_batch(noise,
                                                    np.ones((batch_size, 1)))
        # Output the progress
        print("epoch:{}, batch: {} - [D loss: {}, acc.: {}%] [G loss: {}]".
              format(epoch, batch_id, d_loss[0], 100 * d_loss[1], g_loss))
      # If at save interval => save generated image samples
      if epoch % train_params.save_interval_secs == 0:
        gen_imgs = self.generate_imgs(25)
        self.save_imgs(gen_imgs, save_dir, "epoch_{}".format(epoch))

  def save_imgs(self, imgs, save_dir, fname):
    """Save generated images for checking.

    Args:
      imgs: (num, height, width, channels) ndarray.
      save_dir: directory for saving.
      fname: file name.
    """
    if not os.path.exists(save_dir):
      os.makedirs(save_dir)
    num_imgs = imgs.shape[0]
    r = int(math.sqrt(num_imgs))
    c = num_imgs / r
    fig, axs = plt.subplots(r, c)
    cnt = 0
    for i in range(r):
      for j in range(c):
        # grayscale
        if imgs.shape[3] == 1:
          axs[i, j].imshow(imgs[cnt, :, :, 0], cmap="gray")
        else:
          axs[i, j].imshow(imgs[cnt, :, :, :])
        axs[i, j].axis("off")
        cnt += 1
        if cnt >= num_imgs:
          break
    fig.savefig(os.path.join(save_dir, "{}.png".format(fname)))
    plt.close()

  def test(self, test_params):
    pass

  def generate_imgs(self, num=1):
    # sample image.
    # convert to proper format.
    noise = np.random.normal(0, 1, (num, 100))
    gen_imgs = self.dm_model.generator.predict(noise)
    # Rescale images 0 - 1
    gen_imgs = 0.5 * gen_imgs + 0.5
    return gen_imgs
