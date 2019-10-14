# ICS (Intelligent Course Search) Research

Scripts in this repository are used to:

1. Train models to tag word embeddings with semantics, i.e. infer topics for courses
1. Perform model selection and optimization.  

*Disclaimer: data redacted for privacy purposes.*

## sh retrain.sh

calls scripts

	semantic_model.py
	group_keywords.py
	
## `semantic_model.py [options]`

Creates bag of words representations for the text-valued column, and trains a logistic regression model using the full vector space to predict those bag of words.  

### Input: 

    - word embeddings you would like to perform semantic analysis on
    - text-valued data corresponding to word embeddings

### Options

    -v vectorfile_path: location of word embeddings you would like to perform semantic analysis on
    -i infofile_path: location of text-valued data corresponding to word embeddings
    -t textcolumn: column in infofile to be preprocessed and vectorized
	-b tf_bias: the bias constant for term-frequency
	-r research_file: flag indicating whether or not research file should be generated

Research file includes keyword groups including top topics / keywords within description, out of description, as well as random baselines.  

## `cv_grid_search.py`

Performs a 5-fold cross validation grid search across the following hyperparameters: 

    - use_hidden_layer: train a multinomial regression model or a multilayer perceptron
    - num_epochs: number of epochs to train models
    - use_idf: True to use tf-idf scores, false to only use tf in BOW representation
	- tf_bias: term-frequency bias, controls specificity of words in BOW representation
    - max_df: control for corpus specific words