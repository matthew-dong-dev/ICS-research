tf_bias_list=($(seq 0 .5 2))

# RUNS THE TRAINING SCRIPT FOR MULTIPLE TF_BIAS VALUES AND RETURNS THE PREDICTED KEYWORDS

for i in ${tf_bias_list[@]}; do

    printf "=========================== Training with tf-bias: %s\n" "${i}"
    python semantic_model.py -v ../input_data/raw_vectors.tsv -r ../input_data/vector_text.tsv -t description -b ${i} 

done

python group_keywords.py