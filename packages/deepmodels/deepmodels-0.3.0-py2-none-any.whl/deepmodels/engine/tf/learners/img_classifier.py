"""TensorFlow version of dm classifier.
"""

import numpy as np

import tensorflow as tf
import tensorflow.contrib.slim as slim

from deepmodels.core import commons
from deepmodels.core.data.vision import img_clf_data
from deepmodels.core.learners import dm_classifier

from deepmodels.engine.tf.learners.commons import DMLearnerTF
from deepmodels.engine.tf import base_model
from deepmodels.engine.tf import common_flags
from deepmodels.shared import data_manager

flags = tf.app.flags
FLAGS = flags.FLAGS


def comp_train_accuracy(pred_logits, label_batch):
  """Compute classification accuracy on training data.

  Args:
    pred_logits: prediction logits.
    label_batch: label batch.

  Returns:
    top 1 classfication accuracy.
  """
  # issue with img_folder_data that produces 2 dimensional label_batch
  label_batch = tf.squeeze(label_batch)
  pred_cls = tf.cast(tf.argmax(pred_logits, 1), tf.int32)
  correct_prediction = tf.cast(
      tf.equal(pred_cls, tf.cast(label_batch, tf.int32)), tf.float32)
  accuracy = tf.reduce_mean(correct_prediction)
  accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
  tf.summary.scalar("eval/mean_clf_accuracy", accuracy)
  print "train/pred_cls_shape is: {}".format(tf.shape(pred_cls))
  print "train/label_batch_shape is: {}".format(tf.shape(label_batch))


class DMClassifierTF(dm_classifier.DMClassifier):
  """Tensorflow implementation of classifier.
  """
  # tf specific helper object.
  tf_learner = DMLearnerTF()
  sess = None

  def __init__(self, dm_model_, dm_data_):
    super(dm_classifier.DMClassifier, self).__init__(dm_model_, dm_data_)
    self.sess = tf.Session()

  def __del__(self):
    if self.sess is not None:
      del self.sess
      self.sess = None

  def start(self):
    """Prepare learner.
    """
    # only in test mode, load weights.
    # for finetune, weights will be loaded in train method (avoid redefining model).
    if self.dm_model.model_params.model_mode == commons.ModelMode.TEST:
      print "starting learner..."
      model_inputs = tf.placeholder(
          dtype=tf.float32,
          shape=self.dm_model.get_input_shape(),
          name="test_input")
      _, _, self.input_var_name, self.output_var_names = self.tf_learner.build_model(
          self.dm_model, model_inputs)
      # set variables to restore.
      self.vars_to_restore, self.vars_to_train = self.tf_learner.set_key_vars(
          self.dm_model.restore_scope_exclude, None)
      self.tf_learner.load_model_from_checkpoint_fn(
          self.sess, self.dm_model.model_weight_fn, self.vars_to_restore)
      print "learner started."

  def compute_losses(self, gt_labels, pred_logits):
    """Compute training losses.

    Override only when non-standard loss for a particular model.

    Args:
      gt_labels: ground truth labels in one-hot encoding.
      pred_logits: prediction logits.

    Returns:
      computed loss tensor.
    """
    clf_loss = tf.losses.softmax_cross_entropy(
        onehot_labels=gt_labels,
        logits=pred_logits,
        weights=1.0,
        scope="clf_loss")
    tf.summary.scalar("losses/clf_loss", clf_loss)
    return clf_loss

  def train(self, train_params, preprocessed=True):
    """Training process of the classifier.

    Args:
      train_params: commons.TrainTestParams object.
      preprocessed: if train data has been preprocessed.
    """
    assert isinstance(
        train_params,
        commons.TrainTestParams), "train params is not a valid type"
    # get training data from dataset.
    if preprocessed:
      preprocess_fn = self.dm_model.get_preprocess_fn()
    else:
      preprocess_fn = None
    train_input_batch, train_label_batch, samp_num = self.dm_data.gen_batch_data(
        data_type=commons.DataType.TRAIN,
        batch_size=train_params.batch_size,
        target_img_height=self.dm_model.model_params.input_img_height,
        target_img_width=self.dm_model.model_params.input_img_width,
        preprocess_fn=preprocess_fn)
    # build model.
    pred_logits, _, self.input_var_name, self.output_var_names = self.tf_learner.build_model(
        self.dm_model, train_input_batch)
    comp_train_accuracy(pred_logits, train_label_batch)
    tf.assert_equal(
        tf.reduce_max(train_label_batch),
        tf.convert_to_tensor(
            self.dm_model.model_params.cls_num, dtype=tf.int64))
    # compute loss.
    onehot_labels = tf.one_hot(
        train_label_batch,
        self.dm_model.model_params.cls_num,
        on_value=1.0,
        off_value=0.0)
    # onehot_labels = slim.one_hot_encoding(train_label_batch,
    #                                       model_params.cls_num)
    onehot_labels = tf.squeeze(onehot_labels)
    self.compute_losses(onehot_labels, pred_logits)
    # load pretrained model if needed.
    # set variables.
    self.vars_to_restore, self.vars_to_train = self.tf_learner.set_key_vars(
        train_params.restore_scopes_exclude, train_params.train_scopes)
    init_fn = None
    if train_params.fine_tune and not train_params.resume_training:
      init_fn = slim.assign_from_checkpoint_fn(train_params.custom["model_fn"],
                                               self.vars_to_restore)
    # this would not work if a tensorboard is running...
    if not train_params.resume_training:
      data_manager.remove_dir(train_params.train_log_dir)
    # display regularization loss.
    if train_params.use_regularization:
      regularization_loss = tf.add_n(tf.losses.get_regularization_losses())
      tf.summary.scalar("losses/regularization_loss", regularization_loss)
    total_loss = tf.losses.get_total_loss(
        add_regularization_losses=train_params.use_regularization)
    base_model.train_model_given_loss(
        total_loss, self.vars_to_train, train_params, init_fn=init_fn)

  def test(self, test_params, preprocessed=True):
    """Testing process of the classifier.

    Args:
      test_input_batch: input batch for testing.
      test_label_batch: class id for testing.
      test_params: commons.TrainTestParams object.
      preprocessed: if data has been preprocessed.
    """
    assert isinstance(test_params, commons.TrainTestParams)
    if preprocessed:
      preprocess_fn = self.dm_model.get_preprocess_fn()
    else:
      preprocess_fn = None
    test_input_batch, test_label_batch, cls_num = self.dm_data.get_batch_data(
        data_type=commons.DataType.TEST,
        batch_size=train_params.batch_size,
        target_img_height=self.dm_model.model_params.target_img_height,
        target_img_width=self.dm_model.model_params.target_img_width,
        preprocess_fn=preprocess_fn)
    pred_logits, _, _, _ = self.tf_learner.build_model(self.dm_model,
                                                       test_input_batch)
    pred_cls = tf.argmax(pred_logits, 1)
    metric_args = {
        "eval/mean_clf_accuracy":
        slim.metrics.streaming_accuracy(pred_cls, test_label_batch)
    }
    base_model.test_model_given_metrics(metric_args, test_params)

  def predict(self, input_data, preprocessed=False):
    """Get prediction value from a tensor.

    Args:
      input_data: raw inputs as numpy array to predict.
      preprocessed: if data has been preprocessed.

    Returns:
      two matrices with each row for each sample and
    ranked label id and probability.
    """
    pred_logits = self.tf_learner.get_outputs(
        self.sess,
        self.input_var_name,
        input_data,
        target_tensor_names=self.output_var_names,
        dm_model=self.dm_model,
        preprocessed=preprocessed)
    pred_probs = np.exp(pred_logits) / np.sum(np.exp(pred_logits))
    assert len(pred_probs) == 1, "classifier prediction is not valid"
    pred_probs = pred_probs[0]
    sorted_pred_labels = np.argsort(pred_probs, axis=1)[:, ::-1]
    sorted_pred_probs = np.sort(pred_probs, axis=1)[:, ::-1]
    return sorted_pred_labels, sorted_pred_probs