import os
import sys

# add tensorflow model directory.
cur_fn_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(cur_fn_dir, "tfmodels/models/slim/"))

from deepmodels.engine.tf import data
from deepmodels.engine.tf import models
from deepmodels.engine.tf import learners
from deepmodels.engine.tf import tfmodels
from deepmodels.engine.tf import common_flags