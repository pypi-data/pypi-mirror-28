"""Test tensorflow classifier.
"""

import numpy as np
from scipy.ndimage import imread

import tensorflow as tf

from deepmodels.core import commons
from deepmodels.engine.tf.models.vision import vgg
from deepmodels.engine.tf.data.vision.imagenet import imagenet
from deepmodels.engine.tf.learners import dm_classifier


class TestTFClassifier(object):
  def test_clf_creation(self):
    try:
      with tf.Graph().as_default():
        data = imagenet.ImageNetTFVGG()
        model = vgg.DMVGGTF()
        model.model_params.model_mode = commons.ModelMode.TEST
        clf = dm_classifier.DMClassifierTF(model, data)
      assert True
    except Exception as ex:
      print ex.message
      assert False

  def test_clf_training(self):
    pass

  def test_clf_pred(self):
    with tf.Graph().as_default():
      data = imagenet.ImageNetTFVGG()
      model = vgg.DMVGGTF()
      model.model_params.model_mode = commons.ModelMode.TEST
      model.model_params.output_layer_names = []
      clf = dm_classifier.DMClassifierTF(model, data)
      clf.start()
      img = imread("/mnt/Lab/imgs/1_25_25406.jpg")
      imgs = np.expand_dims(img, 0)
      pred_labels, _ = clf.predict(imgs, False)
      for label in pred_labels[0][:5]:
        print data.get_label_name(label)
    assert True
