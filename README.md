# ICS Research

Scripts in this repository are used to generate inferred keywords and optimize model hyperparameters. 

## Synopsis

	`sh retrain.sh`

calls scripts

	semantic_model.py
	group_keywords.py
	
## `semantic_model.py [options]`

Creates bag of words representations for the text-valued column, and train a logistic regression model using the full vector space to predict those bag of words.  

Input: 

    - word embeddings you would like to perform semantic analysis on
    - text-valued data corresponding to word embeddings

### Options

    -v vectorfile_path
    -r textfile_path
    -t textcolumn

### Hyperparameter Arguments

    -b tf_bias
    -e num_epochs
    -i use_idf
    -m max_df

`tf_bias` is the term-frequency bias, `num_epochs` is the number of epochs to train logistic regression for, `use_idf` is whether or not to use inverse document frequency in tf-TfidfVectorizer, `max_df` is used to control for corpus specific words