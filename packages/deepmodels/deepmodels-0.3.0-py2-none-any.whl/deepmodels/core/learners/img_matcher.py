"""Template class for image matcher.
"""

import os
import numpy as np

import tensorflow as tf
import tensorflow.contrib.slim as slim

from deepmodels.core import base_model
from deepmodels.core import losses
from deepmodels.core.learners.dm_learner import DMLearner
from deepmodels.shared import data_manager
from deepmodels.shared import search_tools


class DMMatcher(DMLearner):
  """A template class of matcher using triplet loss.
  """

  def compute_losses(self, anchor_feats, pos_feats, neg_feats, train_params):
    """Compute training losses.

    Override only when non-standard loss for a particular model.

    Args:
      anchor_feats: features for anchor batch.
      pos_feats: features for positive batch.
      neg_feats: features for negative batch.
      pred_logits: prediction logits.
    Returns:
      computed losses.
    """
    triplet_loss = losses.triplet_loss(anchor_feats, pos_feats, neg_feats,
                                       train_params.matcher_margin,
                                       train_params.matcher_triplet_type)
    tf.losses.add_loss(triplet_loss)
    tf.summary.scalar("losses/triplet_loss", triplet_loss)

  def train(self,
            train_anchor_batch,
            train_pos_batch,
            train_neg_batch,
            train_params,
            preprocessed=True):
    """Training process of the matcher.

    Each input data should have same shape.

    Args:
      train_anchor_batch: anchor batch.
      train_pos_batch: positive batch.
      train_neg_batch: negative batch.
      train_params: commons.TrainTestParams object.
      preprocessed: if data has been preprocessed.
    """
    self.check_dm_model_exist()
    self.dm_model.use_graph()
    # get embedding for all batches.
    all_batches = tf.concat(
        0, [train_anchor_batch, train_pos_batch, train_neg_batch])
    if not preprocessed:
      all_batches = self.dm_model.preprocess(all_batches)
    all_feats, _ = self.build_model(all_batches)
    anchor_feats, pos_feats, neg_feats = tf.split(all_feats, 3, axis=0)
    self.set_key_vars(train_params.restore_scopes_exclude,
                      train_params.train_scopes)
    self.compute_losses(anchor_feats, pos_feats, neg_feats, train_params)
    init_fn = None
    if train_params.fine_tune:
      # self.vars_to_restore is supposed to be set in set_key_vars
      print("[dm_matcher.train: info] Trying to restore variables: {}".format(
          self.vars_to_restore))
      init_fn = slim.assign_from_checkpoint_fn(train_params.custom["model_fn"],
                                               self.vars_to_restore)
    if not train_params.resume_training:
      data_manager.remove_dir(train_params.train_log_dir)
    if train_params.use_regularization:
      regularization_loss = tf.add_n(tf.losses.get_regularization_losses())
      tf.summary.scalar("losses/regularization_loss", regularization_loss)

    total_loss = tf.losses.get_total_loss(
        add_regularization_losses=train_params.use_regularization)
    base_model.train_model_given_loss(
        total_loss, self.vars_to_train, train_params, init_fn=init_fn)

  # TODO(jiefeng): to load weights from file.
  def test(self,
           gal_data,
           gal_labels,
           probe_data,
           probe_labels,
           test_params,
           preprocessed=True):
    """Testing process of the classifier.

    Args:
      gal_data: gallery data as numpy array.
      gal_labels: gallery labels.
      probe_data: probe data as numpy array.
      probe_labels: probe labels.
      test_params: commons.TrainTestParams object.
      preprocessed: if data has been preprocessed.
    """
    self.check_dm_model_exist()
    data_shape = gal_data.shape
    data_shape[0] = None
    inputs = tf.placeholder(tf.float32, shape=data_shape)
    if not preprocessed:
      inputs = self.dm_model.preprocess(inputs)
    feats, _ = self.build_model(inputs)
    gal_feats = self.get_output(gal_data, feats.name)
    probe_feats = self.get_output(probe_data, feats.name)
    save_prefix = os.path.join(test_params.test_log_dir,
                               test_params.custom["eval_name"])
    dist_mat = search_tools.comp_distmat(
        probe_feats, gal_feats, dist_type=search_tools.DistType.L2)
    search_tools.evaluate(
        test_params.custom["eval_name"],
        dist_mat,
        np.asarray(gal_labels),
        np.asarray(probe_labels),
        save_fn_prefix=save_prefix)
