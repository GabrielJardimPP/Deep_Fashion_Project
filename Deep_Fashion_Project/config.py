# -*- coding: utf-8 -*-
# IMPORTS

import numpy as np
import os
import codecs  # Needs to be imported because of chinese characters
import pandas as pd
from PIL import *
import pickle
import time
import cv2
# GLOBAL

root = os.getcwd()
dataset_folder_path = os.path.join(root, 'Dataset')

Anno_path = os.path.join(dataset_folder_path, 'Anno')
list_attr_cloth = os.path.join(Anno_path, 'list_attr_cloth.txt')
list_attr_items = os.path.join(Anno_path, 'list_attr_items.txt')
list_attr_type = os.path.join(Anno_path, 'list_attr_type.txt')
list_bbox_consumer2shop = os.path.join(Anno_path, 'list_bbox_consumer2shop.txt')
list_item_consumer2shop = os.path.join(Anno_path, 'list_item_consumer2shop.txt')
list_landmarks_consumer2shop = os.path.join(Anno_path, 'list_landmarks_consumer2shop.txt')

Eval_path = os.path.join(dataset_folder_path, 'Eval')
list_eval_partition = os.path.join(Eval_path, 'list_eval_partition.txt')

Img_path = os.path.join(dataset_folder_path, 'Img')