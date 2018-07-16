set -e # exit if keyboard interrupt

export tf_bias_limit=$1 # no spaces
echo "tf-bias limit: $tf_bias_limit"

tf_bias_list=($(seq 0 .5 $tf_bias_limit))

# Python script for range of tf bias values
for i in ${tf_bias_list[@]}; do

    printf "=========================== Training with tf-bias: %s\n" "${i}"
    python semantic_model.py -v ../input_data/raw_vectors.tsv -r ../input_data/vector_text.tsv -t description -b ${i} 

done

python group_keywords.py