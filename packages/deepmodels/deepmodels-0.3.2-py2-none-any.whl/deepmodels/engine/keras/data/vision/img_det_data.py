"""Keras image detection.
"""

from deepmodels.core.data.vision.img_det_data import InfoKey, ImgDetDataset


class ImgDetDatasetKeras(ImgDetDataset):
  """Keras implementation of image detection dataset.
  """

  def __init__(self, ds_name=None, save_dir=None):
    super(ImgDetDatasetKeras, self).__init__(ds_name, save_dir, None)
    self.ds_info.set_value(InfoKey.ENGINE, "keras")

  def build_from_metadata(self, meta_fn, data_type, save_fn_prefix):
    """Keras implementation.
    """
    # set data filenames.
    assert data_type in [commons.DataType.TRAIN, commons.DataType.TEST]
    data_fn = tools.gen_data_filename(save_fn_prefix,
                                      commons.DataFileType.HDF5, data_type)
    if data_type == commons.DataType.TRAIN:
      self.ds_info.set_value(InfoKey.TRAIN_DATA_FN, data_fn)
    else:
      self.ds_info.set_value(InfoKey.TEST_DATA_FN, data_fn)