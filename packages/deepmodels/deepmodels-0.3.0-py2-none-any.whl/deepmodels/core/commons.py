"""Shared definition for constants, classes.

Only put those that might be accessed from different modules.
Keep module specific definition isolated.
"""

# TODO(jiefeng): merge commons and update core code.

import math
import os


class Engine(object):
  TF = 0
  KERAS = 1
  CAFFE = 2
  CAFFE2 = 3
  TORCH = 4
  MXNET = 5


class DMConsts(object):
  """Extra Constants for DeepModels.
  """
  pass


class OPTMethod(object):
  """Optimization methods.
  """
  SGD = 0
  MOMENTUM = 1
  ADAM = 2
  ADAGRAD = 3
  ADADELTA = 4
  FTRL = 5
  RMSPROP = 6

  @staticmethod
  def check_valid(opt):
    assert opt in [
        OPTMethod.SGD, OPTMethod.ADADELTA, OPTMethod.ADAM, OPTMethod.RMSPROP
    ]


class ModelMode(object):
  """Mode of a model.
  """
  TRAIN = 0
  FT = 1
  TEST = 2


class LossType(object):
  """Type names for different losses.
  """
  # exclusive one class label.
  CLF_SOFTMAX_ONECLASS = 0
  # multi-class labels.
  CLF_SOFTMAX_MULTICLASS = 1
  CLF_SIGMOID = 2
  TRIPLET_L1 = 3
  TRIPLET_L2 = 4
  TRIPLET_HAMMING = 5


class ImgFormat(object):
  """Format of image file.
  """
  JPG = 0
  PNG = 1


class ModelType(object):
  """Network model types.

  Add both type and textual name for a new network.
  Simply use an unused number as id.
  """
  model_names = {}
  VGG16 = 0
  model_names[VGG16] = "vgg_16"
  VGG19 = 1
  model_names[VGG19] = "vgg_19"
  IMAGENET_GNET = 2
  model_names[IMAGENET_GNET] = "imagenet_gnet"
  VGG_S = 3
  model_names[VGG_S] = "vgg_s"
  VGG_S_GRAY = 13
  model_names[VGG_S_GRAY] = "vgg_s_gray"
  VGG_M = 22
  model_names[VGG_M] = "vgg_m"
  INCEPTION_V1 = 14
  model_names[INCEPTION_V1] = "inception_v1"
  INCEPTION_V2 = 15
  model_names[INCEPTION_V2] = "inception_v2"
  INCEPTION_V3 = 16
  model_names[INCEPTION_V3] = "inception_v3"
  INCEPTION_V4 = 23
  model_names[INCEPTION_V4] = "inception_v4"
  RESNET_50 = 17
  model_names[RESNET_50] = "resnet_50"
  RESNET_101 = 18
  model_names[RESNET_101] = "resnet_101"
  ALEX_V2 = 19
  model_names[ALEX_V2] = "alexnet_v2"
  INCEPTION_RESNET_V2 = 20
  model_names[INCEPTION_RESNET_V2] = "inception_resnet_v2"
  FACE_CASIA = 4
  FACE_CASIA_COLOR = 5
  FACE_CASIA_COLOR_PRELU = 6
  FACE_CASIA_HASH_COLOR_PRELU = 7
  MNIST = 8
  model_names[MNIST] = "mnist"
  CIFAR10 = 9
  model_names[CIFAR10] = "cifarnet"
  CIFAR100 = 10
  model_names[CIFAR100] = "cifarnet"
  CIFAR10_NIN = 11
  FACE_VGG = 12
  GOOGLENET = 14
  CUSTOM = 21
  MOBILENET = 30
  model_names[MOBILENET] = "mobilenet"


def is_valid_net_type(net_type):
  """Check if the net type is valid.
  """
  if net_type in ModelType.model_names.keys():
    return True
  else:
    return False


def is_inception_model(model_type):
  """Check if the model is an inception model.

  Args:
    model_type: type of model.
  """
  if model_type in [
      ModelType.INCEPTION_V1, ModelType.INCEPTION_V2, ModelType.INCEPTION_V3,
      ModelType.INCEPTION_V4
  ]:
    return True
  else:
    return False


def is_vgg_model(model_type):
  """Check if the model is a vgg model.

  Args:
    model_type: type of model.
  """
  if model_type in [
      ModelType.VGG16, ModelType.VGG19, ModelType.VGG_M, ModelType.VGG_S
  ]:
    return True
  else:
    return False


def is_resnet_model(model_type):
  """Check if the model is a resnet model.

  Args:
    model_type: type of model.
  """
  if model_type in [ModelType.RESNET_50, ModelType.RESNET_101]:
    return True
  else:
    return False


def is_cifar_model(model_type):
  """Check if the model is a cifar model.

  Args:
    model_type: type of model.
  """
  if model_type in [ModelType.CIFAR10, ModelType.CIFAR100]:
    return True
  else:
    return False


class DataType(object):
  """Type of the data.

  Used to categorize data.
  """
  TRAIN = 0
  VALIDATE = 1
  TEST = 2
  LABEL = 3


class DataFileType(object):
  """Type of data files.
  """
  METADATA = 0
  TFRECORD = 1
  HDF5 = 2


class InputDataFormat(object):
  """Format of input data.
  """
  FILE_NAME = 0
  IMG_DATA = 1


class NormType(object):
  """Norm type.
  """
  L1 = 0
  L2 = 1


class TripletType(object):
  """Ways to generate triplets.
  """
  Random = 0
  Hard = 1


class LearnerType(object):
  """Type of deepmodel learner.
  """
  Classifier = 0,
  Matcher = 1


class ModelParams(object):
  """Create general model related parameters.

  Custom params can be created by inheriting from this class.
  """

  def __init__(self,
               model_name="",
               model_type=ModelType.VGG16,
               model_mode=ModelMode.TRAIN,
               cls_num=100,
               input_layer_name="",
               output_layer_names=[],
               input_img_shape=(100, 100, 3),
               input_img_width=100,
               input_img_height=100,
               output_dim=100):
    """Initialize parameters.

    Args:
      model_name: name of the model.
      model_type: type of the model.
      model_mode: mode of the model.
      cls_num: class number for classification.
      input_layer_name: name of the input layer in model endpoints.
      output_layer_names: list of names of the output layer in model endpoints.
      input_img_shape: the shape of a single input image, 3D tuple (height, width, channels).
      input_img_width: width of input image.
      input_img_height: height of input image.
      output_dim: output dimension, e.g. class number.
    """
    self.model_name = model_name
    self.model_type = model_type
    self.model_mode = model_mode
    self.cls_num = cls_num
    self.input_layer_name = input_layer_name
    self.output_layer_names = output_layer_names
    self.input_img_shape = input_img_shape
    self.input_img_width = input_img_width
    self.input_img_height = input_img_height
    self.output_dim = output_dim
    self.custom = {}


class TrainTestParams(object):
  """Create general params for training and testing.

  Custom params can be created by inheriting from this class.
  """

  def __init__(self,
               log_dir,
               samp_num,
               batch_size=16,
               max_epochs=10,
               opt_method=OPTMethod.ADAM,
               init_lr=0.01,
               apply_lr_decay=False,
               decay_steps=4000,
               decay_rate=0.96,
               momentum=0.9,
               use_regularization=True,
               save_summaries_secs=20,
               save_model_epochs=1,
               task_id=0,
               resume_training=False,
               load_model_dir="",
               do_validation=False,
               session_config=None,
               eval_secs=10):
    """Initialize parameters.

    Args:
      log_dir: directory of training and testing.
      Suffix will be appended accordingly.
      samp_num: total number of samples.
      batch_size: size of a batch.
      max_epochs: how many times to go through entire training set.
      opt_method: optimization method.
      init_learning_rate: starting learning rate.
      apply_lr_decay: apply decay on learning rate.
      decay_steps: how many steps to decay.
      decay_rate: multiplier for decay.
      momentum: used if momentum optimization is used.
      save_summaries_secs: how often to save summaries.
      save_model_epochs: epoch interval to save models.
      load_model_dir: directory to load model for resuming training.
      If empty, use log_dir.
      task_id: used when multiple workers are used. use 0 usually.
      resume_training: continue training by loading saved checkpoint.
      eval_secs: to evaluate after secs.
    """
    self.log_dir = log_dir
    self.train_log_dir = os.path.join(self.log_dir, "train")
    self.test_log_dir = os.path.join(self.log_dir, "test")
    self.samp_num = samp_num
    self.batch_size = batch_size
    self.batch_num_per_epoch = int(
        math.ceil(self.samp_num * 1.0 / self.batch_size))
    self.opt_method = opt_method
    self.init_lr = init_lr
    self.apply_lr_decay = apply_lr_decay
    self.decay_steps = decay_steps
    self.decay_rate = decay_rate
    self.momentum = momentum
    self.max_epochs = max_epochs
    self.max_steps = self.batch_num_per_epoch * self.max_epochs
    self.use_regularization = use_regularization
    self.save_summaries_secs = save_summaries_secs
    self.save_model_epochs = save_model_epochs
    self.load_model_dir = load_model_dir
    self.task_id = task_id
    self.resume_training = resume_training
    self.do_validation = do_validation
    self.eval_secs = eval_secs
    self.fine_tune = False
    self.session_config = session_config
    self.restore_scopes_exclude = []
    # if empty, train everything.
    self.train_scopes = []
    # add basic learner params
    self.classifier = {}
    # add matcher default params
    self.matcher_margin = 0.2
    self.matcher_triplet_type = LossType.TRIPLET_L2
    # add custom params
    self.custom = {}
