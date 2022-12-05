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
single_run("/Users/bradpowell/Desktop/sub-01/Functional/run_1.nii.gz")
single_run("/Users/bradpowell/Desktop/sub-01/Functional/run_2.nii.gz")
single_run("/Users/bradpowell/Desktop/sub-01/Functional/run_3.nii.gz")

#!/usr/bin/env python

import sys
import os
import json

sys.path.insert(0, 'src')

import env_setup
from etl import get_data
from features import apply_features

from model import model_build


def main(targets):
    '''
    Runs the main project pipeline logic, given the targets.
    targets must contain: 'data', 'analysis', 'model'. 
    
    `main` runs the targets in order of data=>analysis=>model.
    '''

    env_setup.make_datadir()
    env_setup.auth()
    
    
    if 'test' in targets:
    

    if 'data' in targets:
        with open('config/data-params.json') as fh:
            data_cfg = json.load(fh)

        # make the data target
        data = get_data(**data_cfg)

    if 'features' in targets:
        with open('config/features-params.json') as fh:
            feats_cfg = json.load(fh)

        feats, labels = apply_features(data, **feats_cfg)

    if 'model' in targets:
        with open('config/model-params.json') as fh:
            model_cfg = json.load(fh)

        # make the data target
        model_build(feats, labels, **model_cfg)

    return


if __name__ == '__main__':
    # run via:
    # python main.py data features model
    targets = sys.argv[1:]
    main(targets)
