"""Shared methods for keras engine.
"""

from keras import optimizers
from deepmodels.core import commons


def get_optimizer(train_params):
  """Create an optimizer object with train parameters. 
  """
  assert isinstance(train_params, commons.TrainTestParams)
  commons.OPTMethod.check_valid(train_params.opt_method)
  if train_params.opt_method == commons.OPTMethod.SGD:
    my_optimizer = optimizers.SGD(lr=train_params.init_lr,
                                  decay=0.0,
                                  momentum=train_params.momentum,
                                  nesterov=True)
  if train_params.opt_method == commons.OPTMethod.RMSPROP:
    # recommend to use the default.
    my_optimizer = optimizers.RMSprop(
        lr=train_params.init_lr, rho=0.9, epsilon=None, decay=0.0)
  if train_params.opt_method == commons.OPTMethod.ADAM:
    # TODO(jiefeng): using object doesn't work.
    my_optimizer = "adam"
    # my_optimizer = optimizers.Adam(lr=train_params.init_lr)
  if train_params.opt_method == commons.OPTMethod.ADAGRAD:
    # recommended to use the default.
    my_optimizer = optimizers.Adagrad(
        lr=train_params.init_lr, epsilon=None, decay=0.0)
  if train_params.opt_method == commons.OPTMethod.ADADELTA:
    # recommended defaults.
    my_optimizer = optimizers.Adadelta(lr=1.0)
  return my_optimizer
