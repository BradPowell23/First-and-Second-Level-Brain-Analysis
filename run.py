import nilearn
import numpy as np
import pandas as pd
from nilearn import plotting
from nilearn import image
from nilearn.glm.first_level import make_first_level_design_matrix
from nilearn.plotting import plot_stat_map, plot_anat, plot_img, view_img
from nilearn.glm.first_level import FirstLevelModel
from nilearn.image import concat_imgs, mean_img
from nilearn.plotting import plot_contrast_matrix
import matplotlib.pyplot as plt
from nilearn.glm import threshold_stats_img
from numpy import array

from src import *
single_run("/Users/bradpowell/Desktop/sub-01/ses-01/Functional/run_1.nii.gz")
single_run("/Users/bradpowell/Desktop/sub-01/ses-01/Functional/run_2.nii.gz")
single_run("/Users/bradpowell/Desktop/sub-01/ses-01/Functional/run_3.nii.gz")
