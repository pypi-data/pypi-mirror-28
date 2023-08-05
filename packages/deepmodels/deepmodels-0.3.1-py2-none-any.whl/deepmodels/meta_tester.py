"""Run an all-in-one test for unittests included in subdirectories.
Assume all test files start with prefix of 'test'.
"""

import os

import deepmodels.shared.data_manager as data_man


def main():
  """Find all tests and run them.
  """
  proj_dir = data_man.get_project_dir()
  tf_dir = os.path.join(proj_dir, "tf")
  test_fns = data_man.find_files(tf_dir, "test_*.py")
  # run all test files.
  for test_fn in test_fns:
    print "running test file: {}".format(test_fn)
    os.system("python {}".format(test_fn))
  print "all tests done."


if __name__ == "__main__":
  main()
