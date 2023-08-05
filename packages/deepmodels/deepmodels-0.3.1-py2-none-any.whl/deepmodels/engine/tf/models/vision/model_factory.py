"""Manager for deepmodels models.
"""

import os

import tensorflow as tf

from deepmodels.core import commons

from deepmodels.shared import data_manager
from deepmodels.engine.tf.tfmodels.models.slim.nets import nets_factory
from deepmodels.engine.tf.tfmodels.models.slim.preprocessing import preprocessing_factory

# from deepmodels.tf.core.dm_models import dm_vgg
# from deepmodels.tf.core.dm_models import dm_inception
# from deepmodels.tf.core.dm_models import dm_cifar

# def get_dm_model(model_type):
#   """A factory to spawn deepmodels.

#   Args:
#     model_type: type of network model.
#   Returns:
#     corresponding deepmodel model object.
#   """
#   if commons.is_inception_model(model_type):
#     incep = dm_inception.InceptionDM(model_type)
#     return incep
#   elif commons.is_vgg_model(model_type):
#     vgg = dm_vgg.VGGDM(model_type)
#     return vgg
#   elif commons.is_cifar_model(model_type):
#     cifar = dm_cifar.CIFARDM(model_type)
#     return cifar
#   else:
#     raise ValueError("not supported model type.")


def get_generic_preprocess_fn(scaling=False, whitening=True, distortion=False):
  """Create a generic preprocessing function.

  Args:
    scaling: scale image pixel to 0~1 value.
    whitening: apply per image whitening.
    distortion: apply distortion on image to create variations.
  """

  def preprocess_fn(img, target_height, target_width):
    """General preprocess function.

    Args:
      img: input single image tensor.
      target_height: target image height.
      target_width: target image width.
    Returns:
      preprocess function.
    """
    img = tf.to_float(img)
    if scaling:
      img = tf.multiply(img, (1.0 / 255))
    if whitening:
      img = tf.image.per_image_standardization(img)
    if distortion:
      pass
    tf.image.resize_images(img, (target_height, target_width))
    return img

  return preprocess_fn


def is_tf_builtin_model_by_name(model_name):
  """Check if it is a built-in model from tf models.
  """
  tf_models = [
      "cifarnet", "inception_v1", "inception_v2", "inception_v3",
      "inception_v4", "vgg_16", "vgg_19", "alexnet_v2", "inception_resnet_v2"
  ]
  if model_name in tf_models:
    return True
  else:
    return False


def is_tf_builtin_model_by_type(model_type):
  """Check if it is a built-in model from tf models.
  """
  tf_models = [
      commons.ModelType.CIFAR10, commons.ModelType.INCEPTION_V1,
      commons.ModelType.INCEPTION_V2, commons.ModelType.INCEPTION_V3,
      commons.ModelType.INCEPTION_V4, commons.ModelType.VGG16,
      commons.ModelType.VGG19, commons.ModelType.ALEX_V2,
      commons.ModelType.INCEPTION_RESNET_V2
  ]
  if model_type in tf_models:
    return True
  else:
    return False


def create_builtin_net(model_type,
                       inputs,
                       cls_num,
                       mode=commons.ModelMode.TRAIN):
  """Build a network that is included in official model repo.

  Args:
    model_type: type of network.
    inputs: input tensor, batch or placeholder.
    cls_num: output class number.
    mode: model mode.
  Returns:
    net: network output.
    end_points: dictionary of named layer outputs.
  """
  if not is_tf_builtin_model_by_type(model_type):
    raise ValueError("net type is not supported.")

  # print "is training: {}".format(mode != commons.ModelMode.TEST)
  target_net = nets_factory.get_network_fn(
      commons.ModelType.model_names[model_type],
      cls_num,
      weight_decay=0.00004,
      is_training=mode != commons.ModelMode.TEST)
  logits, end_points = target_net(inputs)
  return logits, end_points


def get_builtin_net_weights_fn(model_type):
  """Retrieve built-in network weights file path.

  Used for loading weights.

  Args:
    model_type: type of network.
  Returns:
    network weight file.
  """
  if not is_tf_builtin_model_by_type(model_type):
    raise ValueError("net type is not supported.")
  proj_dir = os.path.dirname(__file__)
  ckpt_dir = os.path.join(proj_dir, commons.ModelType.model_names[model_type])
  ckpt = os.path.join(ckpt_dir,
                      commons.ModelType.model_names[model_type] + ".ckpt")
  return ckpt


def get_builtin_net_preprocess_fn(model_type,
                                  model_mode=commons.ModelMode.TRAIN):
  """Perform preprocess for a network.

  Args:
    model_type: type of network.
    target_width: target image width.
    target_height: target image height.
    model_mode: mode of the model.
  Returns:
    preprocess function for the given network.
  """
  preprocess_fn = None
  if not is_tf_builtin_model_by_type(model_type):
    # use default one.
    preprocess_fn = get_generic_preprocess_fn(True, False, False)
  else:
    preprocess_fn = preprocessing_factory.get_preprocessing(
        commons.ModelType.model_names[model_type],
        is_training=model_mode != commons.ModelMode.TEST)
  return preprocess_fn


def apply_batch_net_preprocess(inputs, preprocess_fn, target_width,
                               target_height):
  """Apply preprocess op to batch images.

  Args:
    inputs: batch images with shape (batch_size, h, w, ch).
    preprocess_fn: function with format (inputs, imgh, imgw).
    target_width: target image width.
    target_height: target image height.
  Returns:
    preprocessed batch images.
  """
  all_inputs = tf.unstack(inputs)
  processed_inputs = []
  for cur_input in all_inputs:
    new_input = preprocess_fn(cur_input, target_height, target_width)
    processed_inputs.append(new_input)
  new_inputs = tf.stack(processed_inputs)
  return new_inputs


def preprocess(np_inputs, preprocess_fn, img_width, img_height):
  """Apply preprocessing function to inputs.

  Args:
    np_inputs: numpy array for input tensor.
    preprocess_fn: preprocess function.
  """
  assert np_inputs.ndim == 3 or np_inputs.ndim == 4, "invalid image format for preprocessing"
  if np_inputs.ndim == 3:
    np_inputs = np.expand_dims(np_inputs, axis=0)
  with tf.Graph().as_default() as cur_g:
    input_tensor = tf.convert_to_tensor(np_inputs, dtype=tf.uint8)
    all_inputs = tf.unstack(input_tensor)
    processed_inputs = []
    for cur_input in all_inputs:
      new_input = preprocess_fn(cur_input, img_height, img_width)
      processed_inputs.append(new_input)
    new_inputs = tf.stack(processed_inputs)
    with tf.Session(graph=cur_g) as sess:
      processed_inputs = sess.run(new_inputs)
  return processed_inputs


# TODO(jiefeng): move to data related place?
# def net_label_names(net_type):
#   """Get label names for a network.

#   Args:
#     net_type: network type.
#   Returns:
#     a label to string dict for name mapping.
#   """
#   if net_type not in {
#       commons.ModelTypes.VGG16, commons.ModelTypes.INCEPTION_V3,
#       commons.ModelTypes.INCEPTION_V1
#   }:
#     raise ValueError("Only VGG16 labels are supported now.")
#   net_name = net_params[net_type].model_name
#   proj_dir = data_manager.get_project_dir()
#   label_fn = os.path.join(proj_dir, "models/{}/{}_labels.txt".format(net_name,
#                                                                      net_name))
#   label_name_dict = {}
#   with open(label_fn, "r") as f:
#     label_str = f.read()
#     label_name_dict = eval(label_str)
#     # label_names = f.readlines()
#     # label_name_dict = {i:label_names[i].rstrip() for i in range(len(label_names))}
#   return label_name_dict