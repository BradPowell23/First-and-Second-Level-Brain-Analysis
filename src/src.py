def single_run(image_file, view_file, recall_file, confounds_file):
  events_view = pd.read_csv(view_file, sep='\t')
  events_view['trial_type'] = 'view'
  events_recall = pd.read_csv(recall_file, sep='\t')
  events_recall['trial_type'] = 'recall'
  events = pd.concat([events_view, events_recall])
  confounds = pd.read_csv(confounds_file, sep='\t')

  timings = np.arange(0, len(confounds))
  design_matrix_constant = make_first_level_design_matrix(timings, events, drift_model=None)
  design_matrix = pd.concat([design_matrix_constant, confounds], axis=1)

  view_array = np.zeros(len(design_matrix.columns))
  view_array[1] = 1

  recall_array = np.zeros(len(design_matrix.columns))
  recall_array[0] = 1

  conditions = {
      'view': view_array,
      'recall': recall_array,
  }
  view_minus_recall = conditions['view'] - conditions['recall']
  plot_contrast_matrix(view_minus_recall, design_matrix=design_matrix)

  fmri_imgs = image.load_img(image_file)
  avg_img = mean_img(fmri_imgs)
  
  #Model
  fmri_glm = FirstLevelModel(t_r=1,
                            noise_model='ar1',
                            standardize=False,
                            hrf_model='spm',
                            drift_model=None,
                            high_pass=.01)
  fmri_glm = fmri_glm.fit(fmri_imgs, design_matrices = design_matrix)
  z_map = fmri_glm.compute_contrast(view_minus_recall,
                                    output_type='z_score')

  #Activation Maps
  plot_stat_map(z_map, bg_img=avg_img, threshold=3.0,
                display_mode='z', cut_coords=3, black_bg=True,
                title='View minus Recall (Z>3)')
  plt.show()

  _, threshold = threshold_stats_img(z_map, alpha=.001, height_control='fpr')
  print('Uncorrected p<0.001 threshold: %.3f' % threshold)
  plot_stat_map(z_map, bg_img=avg_img, threshold=threshold,
              display_mode='z', cut_coords=3, black_bg=True,
              title='View minus Recall (p<0.001)')
  plt.show()

  _, threshold = threshold_stats_img(z_map, alpha=.05, height_control='bonferroni')
  print('Bonferroni-corrected, p<0.05 threshold: %.3f' % threshold)
  plot_stat_map(z_map, bg_img=avg_img, threshold=threshold,
                display_mode='z', cut_coords=3, black_bg=True,
                title='View minus Recall (p<0.05, corrected)')
  plt.show()
  
  _, threshold = threshold_stats_img(z_map, alpha=.05, height_control='fdr')
  print('False Discovery rate = 0.05 threshold: %.3f' % threshold)
  plot_stat_map(z_map, bg_img=avg_img, threshold=threshold,
                display_mode='z', cut_coords=3, black_bg=True,
                title='View minus Recall (fdr=0.05)')
  plt.show()

  clean_map, threshold = threshold_stats_img(z_map, alpha=.05, height_control='fdr', cluster_threshold=10)
  plot_stat_map(clean_map, bg_img=avg_img, threshold=threshold,
                display_mode='z', cut_coords=3, black_bg=True,
                title='View minus Recall (fdr=0.05), clusters > 10 voxels')
  plt.show()
  
  view_img(z_map, threshold = 3.0)
