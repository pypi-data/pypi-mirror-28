"""Shared code for tensorflow based learners.
"""

import tensorflow as tf
import tensorflow.contrib.slim as slim

from deepmodels.engine.tf import base_model


class DMLearnerTF(object):
  """Base class for TF implementation.
  """

  def set_key_vars(self, restore_scope_exclude, train_scopes):
    """Set critical variables for relevant tasks.

    Set vars_to_train and vars_to_restore.
    Called after build_model.

    Args:
      restore_scope_exclude: variable scopes to exclude for restoring.
      train_scopes: variable scopes to train.
    """
    vars_to_restore = slim.get_variables_to_restore(
        exclude=restore_scope_exclude)
    vars_to_train = []
    if train_scopes is not None:
      for scope in train_scopes:
        variables = slim.get_variables(scope=scope)
        vars_to_train.extend(variables)
    if not vars_to_train:
      print "[set_key_vars: info] No variables to train were defined." \
            " Will train ALL variables."
      vars_to_train = None
    else:
      print "variables to train: "
      print vars_to_train
    return vars_to_restore, vars_to_train

  def build_model(self, dm_model, inputs):
    """Construct network graph using dm_model build_model().

    The internal input/output_tensor_name will be set based on
    dm_model.net_params.input/output_layer_name from endpoints.

    Args:
      dm_model: deepmodel model object.
      inputs: input data, either data vectors or images.

    Returns:
      prediction and endpoints.
    """
    output_tensor_names = []
    outputs, endpoints = dm_model.build_model(inputs)
    if dm_model.model_params.input_layer_name != "":
      input_tensor_name = endpoints[
          dm_model.model_params.input_layer_name].name
    else:
      input_tensor_name = inputs.name
    if dm_model.model_params.output_layer_names:
      for layer_name in dm_model.model_params.output_layer_names:
        output_tensor_names.append(endpoints[layer_name].name)
    else:
      output_tensor_names = [outputs.name]
    return outputs, endpoints, input_tensor_name, output_tensor_names

  def get_outputs(self,
                  sess,
                  input_tensor_name,
                  input_data,
                  target_tensor_names,
                  dm_model,
                  preprocessed=True):
    """Get outputs from a list of tensors.

    Args:
      input_data: raw network input as numpy array.
      preprocessed: if the data has been preprocessed.
      target_tensor_names: target tensors to evaluate.
      Use internal output_tensor_name as default.

    Returns:
      evaluated tensor values.
    """
    if not preprocessed:
      input_data = dm_model.preprocess(input_data)
    assert input_data.ndim == 4
    tensor_vals = []
    for tensor_name in target_tensor_names:
      cur_tensor_name = tensor_name
      tensor_val = base_model.eval_tensor(sess, input_tensor_name, input_data,
                                          cur_tensor_name)
      tensor_vals.append(tensor_val)
    return tensor_vals

  def load_model_from_checkpoint_fn(self, sess, model_fn, vars_to_restore):
    """Load weights from file and keep in memory.

    Args:
      sess: tensorflow session.
      model_fn: saved model file.
      vars_to_restore: vars to be restored.
    """
    print "start loading from checkpoint file..."
    if vars_to_restore is None:
      vars_to_restore = slim.get_variables()
    restore_func = slim.assign_from_checkpoint_fn(model_fn, vars_to_restore)
    print "restoring model from {}".format(model_fn)
    restore_func(sess)
    print "model restored."

  def load_model_from_pb(self, pb_fn):
    """Load model data from a binary protobuf file.

    Args:
      pb_fn: protobuf file.
    """
    pass

  def save_model_for_prediction(self, save_ckpt_fn, vars_to_save=None):
    """Save model data only needed for prediction.

    Args:
      save_ckpt_fn: checkpoint file to save.
      vars_to_save: a list of variables to save.
    """
    if vars_to_save is None:
      vars_to_save = slim.get_model_variables()
      vars_restore_to_exclude = []
      for scope in self.dm_model.restore_scope_exclude:
        vars_restore_to_exclude.extend(slim.get_variables(scope))
      # remove not restored variables.
      vars_to_save = [
          v for v in vars_to_save if v not in vars_restore_to_exclude
      ]
    base_model.save_model(save_ckpt_fn, self.sess, vars_to_save)