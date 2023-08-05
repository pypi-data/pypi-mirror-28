"""Data providers for various datasets.
"""

import csv
import glob
import os
import random
import urllib2

from tqdm import tqdm

import tensorflow as tf

from deepmodels.core import commons
from deepmodels.engine.tf import common_flags
from deepmodels.engine.tf import tools

flags = tf.app.flags
FLAGS = flags.FLAGS


def decode_img_tensor(img_bin_data, img_format):
  """Wrapper to decode image data.

  tf.images.decode_images returns a tensor without shape.
  """
  if img_format == commons.ImgFormat.JPG:
    img_tensor = tf.image.decode_jpeg(img_bin_data, channels=3)
  if img_format == commons.ImgFormat.PNG:
    img_tensor = tf.image.decode_png(img_bin_data, channels=3)
  return img_tensor


def load_labelname_fn(label_fn):
  """Parse label names from file generated from metadata function.

  Args:
    label_fn: file containing label names.
  Returns:
    dictionary mapping label to name.
  """
  with open(label_fn, "r") as f:
    label_names_str = f.read()
    label_name_dict = eval(label_names_str)
    return label_name_dict


def read_img_data(img_fn):
  """Read binary image data using tf functions.

  Args:
    img_fn: image file.
  Returns:
    binary image data.
  """
  if os.path.exists(img_fn):
    with tf.Graph().as_default():
      value = tf.read_file(img_fn)
      with tf.Session() as sess:
        img_data = sess.run(value)
  else:
    # download
    user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"
    header = {'User-agent': user_agent}
    res_data = urllib2.Request(img_fn, None, header)
    res_fh = urllib2.urlopen(res_data)
    img_data = res_fh.read()
  return img_data


def load_img_fns(img_dir,
                 img_width,
                 img_height,
                 img_format=commons.ImgFormat.PNG,
                 preprocess_fn=None):
  """Load all image from given files to tf tensor.

  Args:
    img_fns: file names for images.
    img_width: image width.
    img_height: image height.
    img_format: format of image file.
    preprocess_fn: function for preprocessing.
  Returns:
    imgs: loaded image data.
    img_fns: image file names for logging.
  """
  img_format_str = "*.jpg" if img_format == commons.ImgFormat.JPG else "*.png"
  img_fns = glob.glob(os.path.join(img_dir, img_format_str))
  print img_fns
  img_data = []
  for img_fn in img_fns:
    value = tf.read_file(img_fn)
    img_content = decode_img_tensor(value, img_format)
    if preprocess_fn is not None:
      img_content = preprocess_fn(img_content, img_height, img_width)
    else:
      img_content = tf.image.resize_images(img_content,
                                           (img_height, img_width))
    img_data.append(img_content)
  imgs = tf.stack(img_data)
  return imgs, img_fns


def gen_triplet_metadata_from_img_fns(img_dir,
                                      save_fn_prefix,
                                      img_format=commons.ImgFormat.JPG,
                                      train_ratio=0.8):
  """Generate csv file containing image triplet.

  File format: <anchor_img_path, pos_img_path, neg_img_path>

  Args:
    img_dir: root directory. Each subfolder is a category.
    save_fn_prefix: prefix for saved files.
    img_format: jpg or png.
    train_ratio: 0.8.
  """
  # list all category directories.
  cate_dirs = os.listdir(img_dir)
  cate_dirs = [os.path.join(img_dir, x) for x in cate_dirs]
  cate_dirs = [x for x in cate_dirs if os.path.isdir(x)]
  img_ext = "*.png"
  if img_format == commons.ImgFormat.JPG:
    img_ext = "*.jpg"
  train_data = []
  test_data = []
  label_names = []
  # list image files.
  for cate_id, cur_cate_dir in enumerate(cate_dirs):
    cur_cate_name = os.path.basename(cur_cate_dir.strip("/"))
    label_names.append(cur_cate_name)
    cur_fns = glob.glob(os.path.join(cur_cate_dir, img_ext))
    random.shuffle(cur_fns)
    total_fn_num = len(cur_fns)
    all_labels = [cate_id] * total_fn_num
    train_fn_num = int(total_fn_num * train_ratio)
    train_data.extend(zip(cur_fns[:train_fn_num], all_labels[:train_fn_num]))
    test_data.extend(zip(cur_fns[train_fn_num:], all_labels[train_fn_num:]))


def clf_input_from_image_fns(meta_fn,
                             img_depth=3,
                             img_width=224,
                             img_height=224,
                             batch_size=16,
                             preprocess_fn=None,
                             shuffle=True):
  """Feed images from files.
  Args:
    meta_fn: file of the metadata.
    img_depth: number of channels.
    img_width: width of target image.
    img_height: height of target image.
    batch_size: size of each batch.
    preprocess_fn: preprocessing function, <img_data, height, width>.
    shuffle: whether to shuffle or not.
  Returns:
    input queue for batch data.
  """
  # probing
  samp_num = 0
  cls_num = 0
  img_ext = "jpg"
  img_fns = []
  img_labels = []
  with open(meta_fn, "r") as f:
    reader = csv.reader(f)
    for row in reader:
      samp_num += 1
      img_ext = row[0][-3:]
      img_fns.append(row[0])
      img_labels.append(int(row[1]))
    cls_num = len(set(img_labels))

  # build input queue from csv file.
  # filename_queue = tf.train.string_input_producer([meta_fn])
  # text_reader = tf.TextLineReader()
  # _, records = text_reader.read(filename_queue)
  # # decode csv content.
  # record_defaults = [tf.constant([], dtype=tf.string),
  #                    tf.constant([], dtype=tf.int64)]
  # img_fn, img_label = tf.decode_csv(records, record_defaults=record_defaults)

  img_fn_tensor = tf.convert_to_tensor(img_fns, tf.string)
  img_label_tensor = tf.convert_to_tensor(img_labels, tf.int64)
  img_fn, img_label = tf.train.slice_input_producer(
      [img_fn_tensor, img_label_tensor],
      num_epochs=None,
      shuffle=True,
      seed=161803)

  # read image.
  img_content = tf.read_file(img_fn)
  if img_ext == "png":
    img_data = tf.image.decode_png(img_content, img_depth)
  if img_ext == "jpg":
    img_data = tf.image.decode_jpeg(img_content, img_depth)
  if preprocess_fn is not None:
    img_data = preprocess_fn(img_data, img_height, img_width)
  # create batch
  if shuffle:
    img_batch, label_batch, fn_batch = tf.train.shuffle_batch(
        [img_data, img_label, img_fn],
        batch_size=batch_size,
        capacity=batch_size * 50,
        min_after_dequeue=batch_size * 20)
  else:
    img_batch, label_batch, fn_batch = tf.train.batch(
        [img_data, img_label, img_fn],
        batch_size=batch_size,
        capacity=batch_size * 20)
  return img_batch, label_batch, fn_batch, samp_num, cls_num


def convert_clf_data_to_tfrecord(meta_fn,
                                 save_fn,
                                 has_header=True,
                                 label_col=1):
  """Convert image files to a single tfrecord file.

  Args:
    meta_fn: file of the metadata.
    save_fn: file to save.
    has_header: if there is header row in csv.
    label_col: column number of target label.
  Returns:
    label name to id, and label id to name mapper.
  """
  # id to name
  label_names = {}
  # name to id
  label_ids = {}
  img_fns = []
  img_labels = []
  print "converting data from {}".format(meta_fn)
  with open(meta_fn, "r") as f:
    reader = csv.reader(f)
    cnt = 0
    for row in reader:
      if has_header and cnt == 0:
        cnt += 1
        continue
      img_fns.append(row[0])
      cur_label_name = row[label_col]
      if cur_label_name not in label_ids:
        # add new label.
        cur_label_id = len(label_ids)
        label_ids[cur_label_name] = cur_label_id
        label_names[cur_label_id] = cur_label_name
      else:
        cur_label_id = label_ids[cur_label_name]
      img_labels.append(int(cur_label_id))
      cnt += 1

  with tf.python_io.TFRecordWriter(save_fn) as record_writer:
    valid_num = 0
    for idx in tqdm(range(len(img_fns))):
      try:
        img_fn = img_fns[idx]
        img_label = img_labels[idx]
        img_data = read_img_data(img_fn)
        example = tf.train.Example(features=tf.train.Features(feature={
            "img_data":
            tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_data])),
            "cate_label": tf.train.Feature(int64_list=tf.train.Int64List(
                value=[img_label]))
        }))
        example_str = example.SerializeToString()
        record_writer.write(example_str)
        valid_num += 1
      except Exception as ex:
        print "error: {}; skipped file {}".format(str(ex), img_fn)
    print "{}% image data in metadata {} has been written to file {}".format(
        valid_num * 100.0 / len(img_fns), meta_fn, save_fn)
  return label_ids, label_names


def input_clf_data_from_tfrecord(data_fn,
                                 img_format=commons.ImgFormat.JPG,
                                 img_depth=3,
                                 img_width=224,
                                 img_height=224,
                                 batch_size=16,
                                 preprocess_fn=None,
                                 shuffle=True):
  """Load classification data from tfrecrod and create input pipeline.

  Args:
    data_fn: converted tfrecord data file.
    label_fn: file containing label names.
    img_format: image format.
    img_depth: number of channels.
    img_width: width of target image.
    img_height: height of target image.
    batch_size: size of each batch.
    preprocess_fn: preprocessing function, <img_data, height, width>.
    shuffle: whether to shuffle or not.
  Returns:
    input pipeline of classification data from tfrecord.
  """
  # get sample number.
  samp_num = 0
  for _ in tf.python_io.tf_record_iterator(data_fn):
    samp_num += 1
  print "total sample: {}".format(samp_num)
  keys_to_features = {
      "img_data": tf.FixedLenFeature(
          [], dtype=tf.string, default_value=""),
      "cate_label": tf.FixedLenFeature(
          [1], dtype=tf.int64, default_value=0)
  }
  # read from tfrecord.
  filename_queue = tf.train.string_input_producer([data_fn], capacity=10)
  reader = tf.TFRecordReader()
  _, serialized_samp = reader.read(filename_queue)
  example = tf.parse_single_example(serialized_samp, keys_to_features)
  img_data = example["img_data"]
  img_label = example["cate_label"]
  # parse image.
  img_data = tf.image.decode_image(img_data, img_depth)
  if preprocess_fn is not None:
    img_data = preprocess_fn(img_data, img_height, img_width)
  else:
    img_data = tf.image.resize_images(img_data, (img_height, img_width))
  # create batch.
  if shuffle:
    img_batch, label_batch = tf.train.shuffle_batch(
        [img_data, img_label],
        batch_size=batch_size,
        capacity=batch_size * 50,
        min_after_dequeue=batch_size * 20,
        allow_smaller_final_batch=True)
  else:
    img_batch, label_batch = tf.train.batch(
        [img_data, img_label],
        batch_size=batch_size,
        capacity=batch_size * 20,
        allow_smaller_final_batch=True)
  return img_batch, label_batch, samp_num


def main(_):
  gen_clf_metadata_from_img_fns(
      FLAGS.img_dir, FLAGS.save_prefix, train_ratio=FLAGS.train_ratio)


if __name__ == "__main__":
  tf.app.run()
