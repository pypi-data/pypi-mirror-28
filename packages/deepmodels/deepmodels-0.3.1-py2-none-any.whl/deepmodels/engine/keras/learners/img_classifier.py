"""Keras implementation of classifier.
"""

import glob
import os
import time

import numpy as np

from keras.models import Model as KerasModel
from keras import callbacks, optimizers

from deepmodels.core import commons
from deepmodels.core.data.vision.img_clf_data import InfoKey
from deepmodels.core.learners import img_classifier
from deepmodels.engine.keras.common import get_optimizer
from deepmodels.engine.keras.data.vision import img_clf_data


class DMImgClassifierKeras(img_classifier.DMImgClassifier):
  """Keras class of classifier.
  """

  def set_dm_data(self, dm_data):
    assert isinstance(dm_data, img_clf_data.ImgClfDatasetKeras)
    self.dm_data = dm_data

  def start(self):
    if self.dm_model.model_params.model_mode == commons.ModelMode.TEST:
      self.dm_model.load_model(self.dm_model.model_weight_fn)
      self.dm_model.model_params.output_layer_names = ["predictions"]

  def compute_losses(self, gt_labels, pred_logits):
    """No need to compute for keras.
    """
    pass

  def get_latest_model(self, save_dir):
    """Find latest modified model.
    """
    model_fns = glob.glob(os.path.join(save_dir, "*model*.h5"))
    latest_time = 0
    trained_model_fn = None
    for model_fn in model_fns:
      modified_time = os.path.getmtime(model_fn)
      if modified_time > latest_time:
        latest_time = modified_time
        trained_model_fn = model_fn
    return trained_model_fn

  def get_outputs(self, input_data, output_layer_name, preprocessed=False):
    shape_dim = len(input_data.shape)
    assert shape_dim == 3 or shape_dim == 4
    if shape_dim == 3:
      # make 4D.
      input_data = np.expand_dims(input_data, axis=0)
    if not preprocessed:
      input_data = self.dm_model.preprocess(input_data)
    target_model = KerasModel(
        inputs=self.dm_model.model.input,
        outputs=self.dm_model.model.get_layer(output_layer_name).output)
    return target_model.predict(input_data)

  def predict(self, input_data, preprocessed=True):
    """Predict class labels.
    """
    startt = time.time()
    # get value for the output layer.
    pred_probs = self.get_outputs(
        input_data, self.dm_model.model_params.output_layer_names[0],
        preprocessed)
    print "prediction time cost: {}s".format(time.time() - startt)
    assert len(pred_probs.shape) == 2
    # convert to label names.
    samp_probs = []
    for samp_id in range(len(pred_probs)):
      cur_preds = []
      for label_id, label_prob in enumerate(pred_probs[samp_id]):
        cur_preds.append((self.dm_data.get_label_name(label_id), label_prob))
      # sort by score from high to low.
      cur_preds.sort(key=lambda tup: tup[1], reverse=True)
      samp_probs.append(cur_preds)
    return samp_probs

  def train(self, train_params):
    # get data
    input_shape = self.dm_model.get_input_shape()
    train_data_generator = self.dm_data.gen_batch_data(
        data_type=commons.DataType.TRAIN,
        batch_size=train_params.batch_size,
        target_img_height=input_shape[1],
        target_img_width=input_shape[2],
        preprocess_fn=self.dm_model.get_preprocess_fn())
    # build model.
    if train_params.resume_training:
      # find latest modified file.
      if train_params.load_model_dir:
        trained_model_fn = self.get_latest_model(train_params.load_model_dir)
      else:
        trained_model_fn = self.get_latest_model(train_params.log_dir)
      assert os.path.exists(
          trained_model_fn), "no existing model existed, cannot resume training"
      self.dm_model.load_model(trained_model_fn)
    else:
      # TODO(jiefeng): add verification for keras based model.
      self.dm_model.build_model()
      # set layers to train.
      for layer in self.dm_model.model.layers:
        if layer.name in train_params.train_scopes or not train_params.train_scopes:
          layer.trainable = True
        else:
          layer.trainable = False
      print(self.dm_model.model.summary())
      # compile model.
      my_optimizer = get_optimizer(train_params)
      print "using optimizer: {}".format(my_optimizer)
      loss_name = "categorical_crossentropy"
      if self.dm_data.is_multi_label():
        loss_name = "binary_crossentropy"
      self.dm_model.model.compile(
          optimizer=my_optimizer, loss=loss_name, metrics=["accuracy"])
    # train.
    if train_params.do_validation:
      # get test data.
      test_data_generator = self.dm_data.gen_batch_data(
          data_type=commons.DataType.TEST,
          batch_size=train_params.batch_size,
          target_img_height=input_shape[1],
          target_img_width=input_shape[2],
          preprocess_fn=self.dm_model.get_preprocess_fn())
      test_steps = self.dm_data.ds_info.get_value(
          InfoKey.TEST_SAMPLE_COUNT) // train_params.batch_size
    else:
      test_data_generator = None
      test_steps = None
    print("start training...")
    model_fn_format = "model__epoch{epoch:03d}__valacc{val_acc:.3f}.h5"
    save_model_fn = os.path.join(train_params.log_dir, model_fn_format)
    self.dm_model.model.fit_generator(
        generator=train_data_generator,
        steps_per_epoch=train_params.batch_num_per_epoch,
        epochs=train_params.max_epochs,
        validation_data=test_data_generator,
        validation_steps=test_steps,
        callbacks=[
            callbacks.TensorBoard(log_dir=train_params.log_dir),
            callbacks.ModelCheckpoint(
                save_model_fn, period=train_params.save_model_epochs)
        ])

  def test(self, test_params, include_top5=False):
    """Perform standalone evaluation.

    Args:
      include_top5: add top5 classification accuracy as a metric.
    """
    assert not self.dm_data.is_multi_label()
    # get data
    input_shape = self.dm_model.get_input_shape()
    data_generator = self.dm_data.gen_batch_data(
        data_type=commons.DataType.TEST,
        batch_size=test_params.batch_size,
        target_img_height=input_shape[1],
        target_img_width=input_shape[2],
        preprocess_fn=self.dm_model.get_preprocess_fn())
    print "batch per epoch: {}".format(test_params.batch_num_per_epoch)
    # load model.
    trained_model_fn = self.get_latest_model(test_params.log_dir)
    self.dm_model.load_model(trained_model_fn)
    print(self.dm_model.model.summary())
    if include_top5:
      self.dm_model.model.compile(
          optimizer="Adam",
          loss="categorical_crossentropy",
          metrics=["top_k_categorical_accuracy"])
    else:
      self.dm_model.model.compile(
          optimizer="Adam",
          loss="categorical_crossentropy",
          metrics=["accuracy"])
    # predict
    scores = self.dm_model.model.evaluate_generator(
        data_generator, test_params.batch_num_per_epoch)
    print "metrics: {}".format(self.dm_model.model.metrics_names)
    print "all scores: {}".format(scores)
    print("classification accuracy: {}".format(scores[1]))
