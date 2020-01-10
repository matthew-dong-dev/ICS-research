# ICS (Intelligent Course Search) Research

> [Research paper](https://link.springer.com/chapter/10.1007%2F978-3-030-29736-7_36)
> 
> [Deployed feature](https://askoski.berkeley.edu/search)

*Disclaimer: data redacted for privacy purposes.*

## `retrain.sh`

Calls 2 scripts:

1. `data_joining.py`
    - Aligns C2V embeddings with corresponding API pulled descriptions. 
1. `semantic_model.py`
    - Train models to tag course embeddings with semantics, i.e. infer topics for courses.
    
## `data_joining.py`

### Input: 
    
- `course_vectors.npy` from `model` folder in timestamped directory
- `course_info.tsv` from `shared/course_api/outputs`
- Uses course_subject and coures_num from API to create foreign key to join on `idx2course.json` identifier

### Output

- `aligned_course_info.tsv`
- `aligned_course_vecs.tsv`

## `semantic_model.py [options]`

Generates bag of words representations for course description, and trains translation model to map from embeddings to BOW and then predicts labels for each course.  Model hyperparameters currently hardcoded at top of script. 

### Sample Usage

    `python semantic_model.py -v ../data/aligned_course_vecs.tsv -i ../data/aligned_course_info.tsv`

### Input

    -v vectorfile_path: location of word embeddings you would like to perform semantic analysis on
    -i infofile_path: location of text-valued data corresponding to word embeddings
    -t textcolumn: column in infofile to be preprocessed and vectorized
	-b tf_bias: the bias constant for term-frequency
	-r research_file: flag indicating whether or not research file should be generated.  Research file includes keyword groups including top topics / keywords within description, out of description, as well as random baselines. 

### Output

    - Dumps pickle file (search_keywords.pkl) containing course_id, course_title, course_description, course_keywords, and course_alternative_names into the output directory
    - Updating search_keywords.pkl requires restarting the backend.  

---
	
## `cv_grid_search.py`

Performs a 5-fold cross validation grid search across the following hyperparameters: 

    - use_hidden_layer: train a multinomial regression model or a multilayer perceptron
    - num_epochs: number of epochs to train models
    - use_idf: True to use tf-idf scores, false to only use tf in BOW representation
	- tf_bias: term-frequency bias, controls specificity of words in BOW representation
    - max_df: control for corpus specific words