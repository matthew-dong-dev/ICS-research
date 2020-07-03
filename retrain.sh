#!/bin/bash

echo '[INFO] Beginning ICS retraining...'
python ./scripts/data_joining.py
echo '[INFO] Running semantic model...'
python ./scripts/semantic_model.py -v ./data/aligned_course_vecs.tsv -i ./data/aligned_course_info.tsv

# set -e 

# while getopts ":b:v:" opt; do
#   case $opt in
#     b) 
# 		export tfbias=$OPTARG
# 		echo "[INFO] setting -b tfbias: $tfbias"
#       ;;
#     v) 
# 		export vectorfile=$OPTARG
# 		echo "[INFO] setting -v vectorfile: $vectorfile"
#       ;;
#     \?) 
# 		echo "Usage: cmd [-b] (tf-bias) [-v] (vector file)"
# 		echo "Invalid option: -$OPTARG" 
# 		exit 1
#       ;;
#      :)
# 	    echo "Option -$OPTARG requires an argument." 
# 	    exit 1
#       ;;
#   esac
# done

# tf_bias_list=($(seq 0 .5 $tfbias))
# for i in ${tf_bias_list[@]}; do

#     printf "=========================== Training model with tf-bias: %s\n" "${i}"
#     python ./scripts/semantic_model.py -v ./data/course_vecs.tsv -r ./data/course_info.tsv -t course_description -b ${i} 

# done
