#!/bin/bash

set -e 

while getopts ":b:v:" opt; do
  case $opt in
    b) 
		export tfbias=$OPTARG
		echo "[INFO] setting -b tfbias: $tfbias"
      ;;
    v) 
		export vectorfile=$OPTARG
		echo "[INFO] setting -v vectorfile: $vectorfile"
      ;;
    \?) 
		echo "Usage: cmd [-b] (tf-bias) [-v] (vector file)"
		echo "Invalid option: -$OPTARG" 
		exit 1
      ;;
     :)
	    echo "Option -$OPTARG requires an argument." 
	    exit 1
      ;;
  esac
done

if [ $OPTIND -eq 1 ]; then echo "Exiting: No options were passed"; exit 1; fi

# ==================================================================

tf_bias_list=($(seq 0 .5 $tfbias))

# run Python script on range of tf-bias values
for i in ${tf_bias_list[@]}; do

    printf "=========================== Training with tf-bias: %s\n" "${i}"
    python semantic_model.py -v $vectorfile -r ../input_data/vector_text.tsv -t description -b ${i} 

done

echo "[INFO] Finished training keywords, proceed to group and get unique keywords"

python group_keywords.py
