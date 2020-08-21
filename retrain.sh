#!/bin/bash

set -e 

echo '[INFO] Beginning ICS retraining...'
python ./scripts/data_joining.py
echo '[INFO] Running semantic model...'
python ./scripts/semantic_model.py -v ./data/aligned_course_vecs.tsv -i ./data/aligned_course_info.tsv

# tf_bias_list=($(seq 0 .5 $tfbias))
# for i in ${tf_bias_list[@]}; do

#     printf "=========================== Training model with tf-bias: %s\n" "${i}"
#     python ./scripts/semantic_model.py -v ./data/course_vecs.tsv -r ./data/course_info.tsv -t course_description -b ${i} 

# done
