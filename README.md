# ICS Research

Scripts in this repository are used for 

1. training models to tag word embeddings with semantics, i.e. infer topics for courses and
1. Perform model selection optimizattion.  

*Disclaimer: data redacted for privacy purposes.*

## sh retrain.sh

calls scripts

	semantic_model.py
	group_keywords.py
	
## `semantic_model.py [options]`

Creates bag of words representations for the text-valued column, and trains a logistic regression model using the full vector space to predict those bag of words.  

Input: 

    - word embeddings you would like to perform semantic analysis on
    - text-valued data corresponding to word embeddings

### Options

    -v vectorfile_path
    -r textfile_path
    -t textcolumn

## `cv_grid_search.py [options]`

Performs a 5-fold cross validation grid search across the following hyperparameters: 

    - tf_bias: term-frequency bias, controls specificity of words 
    - use_hidden_layer: train a multinomial regression model or a multi-layer perceptron
    - num_epochs: number of epochs to train models
    - use_idf: whether or not to use inverse document frequency in tf-TfidfVectorizer
    - max_df: control for corpus specific words