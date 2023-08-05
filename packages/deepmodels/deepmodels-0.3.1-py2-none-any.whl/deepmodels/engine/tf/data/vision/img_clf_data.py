"""Tensorflow implementation.
"""

import os

from deepmodels.core import commons
from deepmodels.core.data.vision.img_clf_data import InfoKey, ImgClfDataset
from deepmodels.core import tools
from deepmodels.engine.tf.data.vision import data_provider


class ImgClfDatasetTF(ImgClfDataset):
  """Tensorflow implementation of image classification dataset.
  """

  def __init__(self, ds_name=None, save_dir=None, ds_info=None):
    super(ImgClfDatasetTF, self).__init__(ds_name, save_dir, ds_info)
    self.ds_info.set_value(InfoKey.ENGINE, "tf")

  def build_from_metadata(self,
                          meta_fn,
                          data_type,
                          save_fn_prefix,
                          has_header_=True,
                          label_col_=1):
    """Convert metadata to format used for training.
    """
    # set data filenames.
    assert data_type in [commons.DataType.TRAIN, commons.DataType.TEST]
    tfrecord_fn = tools.gen_data_filename(
        save_fn_prefix, commons.DataFileType.TFRECORD, data_type)
    if data_type == commons.DataType.TRAIN:
      self.ds_info.set_value(InfoKey.TRAIN_DATA_FN, tfrecord_fn)
    else:
      self.ds_info.set_value(InfoKey.TEST_DATA_FN, tfrecord_fn)
    # convert metadata to data file.
    if not os.path.exists(tfrecord_fn):
      data_provider.convert_clf_data_to_tfrecord(meta_fn, tfrecord_fn)
    # save info to disk.
    self.ds_info.save_info()

  def build_from_folder(self, data_folder, img_format=commons.ImgFormat.JPG):
    """Build dataset from a given folder.

    Metadata file is first created and converted to 
    tfrecord files.
    """
    # set up files.
    self.ds_info.set_value(InfoKey.IMG_FORMAT, img_format)
    save_fn_prefix = os.path.join(data_folder,
                                  self.ds_info.get_value(InfoKey.NAME))
    # generate metadata.
    vals = self.gen_metadata_from_folder(data_folder, save_fn_prefix,
                                         img_format)
    self.ds_info.set_value(InfoKey.TRAIN_META_FN, vals[0])
    self.ds_info.set_value(InfoKey.TEST_META_FN, vals[1])
    self.ds_info.set_value(InfoKey.LABEL_ID_TO_NAME, vals[2])
    self.ds_info.set_value(InfoKey.LABEL_NAME_TO_ID, vals[3])

    # convert db to tfrecord.
    self.build_from_metadata(
        self.ds_info.get_value(InfoKey.TRAIN_META_FN), commons.DataType.TRAIN,
        save_fn_prefix)
    self.build_from_metadata(
        self.ds_info.get_value(InfoKey.TEST_META_FN), commons.DataType.TEST,
        save_fn_prefix)
    # save dataset info.
    self.ds_info.save_info()

  def gen_batch_data(self,
                     data_type=commons.DataType.TRAIN,
                     batch_size=32,
                     target_img_height=128,
                     target_img_width=128,
                     preprocess_fn=None):
    if data_type == commons.DataType.TRAIN:
      data_fn = self.ds_info.get_value(InfoKey.TRAIN_RECORD_FN)
    if data_type == commons.DataType.TEST:
      data_fn = self.ds_info.get_value(InfoKey.TEST_RECORD_FN)
    all_data = data_provider.input_clf_data_from_tfrecord(
        data_fn,
        img_format=self.ds_info.get_value(InfoKey.IMG_FORMAT),
        img_depth=3,
        img_width=target_img_width,
        img_height=target_img_height,
        batch_size=batch_size,
        preprocess_fn=preprocess_fn,
        shuffle=True)
    img_batch, label_batch, samp_num = all_data
    print "loaded data. sample number: {}".format(samp_num)
    return img_batch, label_batch, samp_num