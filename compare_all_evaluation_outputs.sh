
while read LINE;
  do sh get_results_spearman_models.sh $LINE results_spearman_models

done < 'unique_run_ids.txt'
