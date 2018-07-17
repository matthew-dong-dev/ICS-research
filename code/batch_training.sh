#!/bin/bash

set -e 
# exit if keyboard interrupt

while getopts ":b:f:" opt; do
  case $opt in
    b) 
		export tfbias=$OPTARG
		echo "tfbias: $tfbias"
      ;;
    f) 
		export vectorfile=$OPTARG
		echo "vectorfile: $vectorfile"
      ;;
    \?) 
		echo "Usage: cmd [-b] (tf-bias) [-f] (vector file)"
		echo "Invalid option: -$OPTARG" 
		exit 1
      ;;
     :)
	    echo "Option -$OPTARG requires an argument." 
	    exit 1
      ;;
  esac
done

if [ $OPTIND -eq 1 ]; then echo "No options were passed"; exit 1; fi

# ==================================================================

tf_bias_list=($(seq 0 .5 $tfbias))

# run Python script on range of tf-bias values
for i in ${tf_bias_list[@]}; do

    printf "=========================== Training with tf-bias: %s\n" "${i}"
    python semantic_model.py -v ../input_data/analogy_vecs.tsv -r ../input_data/vector_text.tsv -t description -b ${i} 

done

python group_keywords.py