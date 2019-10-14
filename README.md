# Semantic Model

Scripts in this repository are used to generate inferred keywords and optimize model hyperparameters. 

Input: 

    - A text-valued column you would like to perform semantic analysis on.
    - A Word2vec Vectorfile.

## Synopsis

	sh retrain.sh [options]

calls three scripts

	semantic_model.py
	group_keywords.py
	data_joining.py

In particular, `semantic_model.py` will create bag of words representations for the text-valued column, and train a logistic regression model using the full vector space to predict those bag of words.  Note: we do not train with the empty bag of words.

### Options

    -v vectorfile_path
    -r rawfile_path
    -t textcolumn

### Hyperparameter Arguments

    -b tf_bias
    -e num_epochs
    -i use_idf
    -m max_df

`tf_bias` is the term-frequency bias, `num_epochs` is the number of epochs to train logistic regression for, `use_idf` is whether or not to use inverse document frequency in tf-TfidfVectorizer, `max_df` is used to control for corpus specific words