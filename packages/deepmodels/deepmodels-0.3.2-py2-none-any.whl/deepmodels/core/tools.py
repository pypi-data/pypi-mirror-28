"""Shared tool functions.
"""

import json
import os
import glob
import urllib2
import PIL.Image
import numpy as np

from cStringIO import StringIO

from deepmodels.core import commons


def pretty_print_json(obj_val):
  print(json.dumps(obj_val, indent=2, sort_keys=True))


def gen_data_filename(fn_prefix,
                      file_type=commons.DataFileType.METADATA,
                      data_type=commons.DataType.TRAIN):
  """Generate filename for corresponding data.

  Args:
    fn_prefix: prefix of the filename.
    file_type: target file type.
    data_type: type of data file.
  Returns:
    generated filename.
  """
  if file_type == commons.DataFileType.METADATA:
    if data_type == commons.DataType.TRAIN:
      return "{}__train.csv".format(fn_prefix)
    if data_type == commons.DataType.TEST:
      return "{}__test.csv".format(fn_prefix)
    if data_type == commons.DataType.LABEL:
      return "{}__labels.txt".format(fn_prefix)
  if file_type == commons.DataFileType.TFRECORD:
    if data_type == commons.DataType.TRAIN:
      return "{}__train.tfrecord".format(fn_prefix)
    if data_type == commons.DataType.TEST:
      return "{}__test.tfrecord".format(fn_prefix)
    if data_type == commons.DataType.VALIDATE:
      return "{}__validate.tfrecord".format(fn_prefix)
  if file_type == commons.DataFileType.HDF5:
    if data_type == commons.DataType.TRAIN:
      return "{}__train.h5".format(fn_prefix)
    if data_type == commons.DataType.TEST:
      return "{}__test.h5".format(fn_prefix)
    if data_type == commons.DataType.VALIDATE:
      return "{}__validate.h5".format(fn_prefix)


def convert_data_filename(input_fn, dst_file_type, dst_data_type):
  """Convert one data filename to another.

  Args:
    input_fn: input data filename.
    There should be no '__' in filename other than the last part.
    dst_file_type: target data file type.
    dst_data_type: target data type.
  Returns:
    converted data filename.
  """
  sep_idx = input_fn.find("__")
  assert sep_idx != -1, "invalid input data filename."
  return gen_data_filename(input_fn[:sep_idx], dst_file_type, dst_data_type)


def verify_fn_ext(fn, ext):
  """Assert if file is in valid format.

  Args:
    fn: filename.
    ext: file extension, e.g. jpg, png.
  """
  assert os.path.splitext(fn)[1] == ext, "file must be in {} format.".format(
      ext)


def read_img_data(img_path, target_img_shape=(256, 256, 3), use_arr=True):
  """Read image data based on the path type.

  Args:
    img_path: file path or url.
    target_img_shape: final output image shape, (height, width, channels).
    use_arr: fetch numpy array format or raw binary.

  Returns:
    image data in the requested type. None if error.
    If array, all resized to (256, 256)
  """
  try:
    # read image data.
    img_bin_data = None
    if os.path.exists(img_path):
      with open(img_path, "rb") as f:
        img_bin_data = f.read()
    else:
      # download
      user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
      header = {'User-agent': user_agent}
      res_data = urllib2.Request(img_path, None, header)
      res_fh = urllib2.urlopen(res_data)
      img_bin_data = res_fh.read()
    # convert to format.
    if use_arr:
      pil_img = PIL.Image.open(StringIO(img_bin_data))
      if target_img_shape[2] == 1:
        new_img = pil_img.convert("L")
      else:
        new_img = pil_img.convert("RGB")
      new_img = new_img.resize((target_img_shape[1], target_img_shape[0]))
      # when it converts to array, the height becomes the first dimension.
      return np.array(new_img)
    else:
      return img_bin_data
  except Exception as ex:
    print("error reading image data: {}".format(ex.message))
    return None


def list_files(target_dir, fn_exts):
  """List all files match given extensions.

  Match both upper and lower cases.

  Args:
    fn_exts: a list of file extension in the form of "*.jpg".
  
  Returns:
    a list of found files.
  """
  all_exts = []
  for ext in fn_exts:
    all_exts.append(ext.lower())
    all_exts.append(ext.upper())
  all_exts = set(all_exts)
  all_fns = []
  for cur_ext in all_exts:
    cur_fns = glob.glob(os.path.join(target_dir, cur_ext))
    all_fns.extend(cur_fns)
  return all_fns
