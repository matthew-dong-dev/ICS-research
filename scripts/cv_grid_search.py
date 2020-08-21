#!/usr/bin/python 
import time
import os
import pandas as pd
import numpy as np
from collections import Counter, defaultdict
from itertools import chain
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from scipy.spatial.distance import cosine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import KFold
from sklearn.model_selection import ParameterGrid
from keras.layers import Input, Dense
from keras.models import Model
from keras import backend as K
import tensorflow as tf
config = tf.ConfigProto(
    device_count = {'GPU': 0}
)
# config.gpu_options.allocator_type = 'BFC'
# config.gpu_options.allow_growth=True
sess = tf.Session(config=config)
K.set_session(sess)
pd.options.mode.chained_assignment = None 

TRAINING_DIR = '/home/matthew/ICS-Research' # os.getcwd()
DATA_DIR = '/home/matthew/ICS-Research/data'
OUTPUT_DIR = '/home/matthew/ICS-Research/scores'
vectorfile = os.path.join(DATA_DIR, 'course_vecs.tsv')
infofile = os.path.join(DATA_DIR, 'course_info.tsv')
scorefile_path = os.path.join(OUTPUT_DIR, 'new_cv_scores.tsv')
textcolumn = 'course_description'

def get_vocab(dataframe, column, max_df=0.057611, use_idf=True):
    """Gets the vocab labels to be used as inferred keywords. 
    Args:
        Dataframe with column name (string) to parse vocab from.
        Max_df (float): max document frequency for sklearn's vectorizer
        Use_idf (boolean): Use tf-idf to get top feature labels vs just using tf
    Returns:
        Array of vocab labels.
    """
    print("[INFO] Getting vocab...")
    
    dataframe[column] = dataframe[column].fillna('')
    description_with_title = dataframe.course_title.fillna('') + ' ' + dataframe.course_description.fillna('')

    vectorizer = TfidfVectorizer(max_df=max_df, stop_words='english', ngram_range=(1,2), use_idf=use_idf, max_features=20000)
    X = vectorizer.fit_transform(description_with_title)
    vocab = vectorizer.get_feature_names()
#     print('[INFO] Number vocab labels: %d' % (len(vocab)))
    print('[INFO] Getting top 20000 vocab labels.')
    
    vocab_list = list(vocab)
    removed_numbers_list = [word for word in vocab_list if not any(char.isdigit() for char in word)]
    vocab = np.array(removed_numbers_list)
    return vocab

def to_bag_of_words(dataframe, column, vocab, use_idf=True, tf_bias=.5):
    """Converts text corpus into its BOW representation using predefined vocab.
    Args:
        raw dataframe, text column, and vocabulary.
    Returns:
        A sparse matrix of the bag of words representation of the column.
    """
    vectorizer = TfidfVectorizer(stop_words='english', vocabulary=vocab, use_idf=use_idf)
    X = vectorizer.fit_transform(dataframe[column].values.astype('U'))
    if tf_bias == -999:
        print('[INFO] Not using tf-bias')
        return X
    return (X.multiply(1/X.count_nonzero())).power(-tf_bias)

def logistic_regression(X, Y, X_val, Y_val, validation_vocab, use_hidden_layer=False, hidden_layer_size=200, num_epochs=5, num_words_per_course=10):
    """Perform multinomial logistic regression from BOW vector space (Y) onto course vector space (X) and predict inferred keywords for each course. 
    Args: 
        X (numpy array): matrix of course vectors  
        Y (numpy array): corresponding descriptions as BOW encodings  
        number of epochs (int) 
        num_words_per_course (int): Number of words to predict per course
    Returns:
        Course description dataframe with a new column for every predicted word 
    """
    print('[INFO] Performing logistic regression...')

    inputs = Input(shape=(X.shape[1],)) # course vec
    if use_hidden_layer:
        hidden_layer = Dense(hidden_layer_size, activation='sigmoid')(inputs)
        predictions = Dense(vocabsize, activation='softmax')(hidden_layer) # vocabsize also global
    else:
        predictions = Dense(vocabsize, activation='softmax')(inputs)
    model = Model(inputs=inputs, outputs=predictions)
    model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
    model.fit(X, Y, epochs=num_epochs)

    # Obtain the softmax predictions for all instances 
    softmax_frame = pd.DataFrame(model.predict(X_val))
    
    # From the softmax predictions, save the top 10 predicted words for each data point
    print('[INFO] Sorting classification results...')
    sorted_frame = np.argsort(softmax_frame,axis=1).iloc[:, ::-1]
    
    print('[INFO] Predicting top k inferred keywords for each course...')
    df_with_keywords = Y_val.copy() # filtered_info_frame is global
    
    for i in range(num_words_per_course): # vocab_frame also global
        new_col = validation_vocab.iloc[sorted_frame.iloc[:,i],0] # get the ith top vocab word for each entry
        df_with_keywords['predicted_word_' + str(i+1)] = new_col.values
        
    return df_with_keywords

def calculate_metric(df_with_keywords, metric):
    """Calculate metric evaluating quality of inferred keywords with respect to its true course description
    Args: 
        df_with_keywords: dataframe with predicted keywords for every course for every columns
        metrics (string): {r: recall, p: precision, c: cosine similarity, 
        df: document frequency of inferred keywords using course subject as documents}
    Returns
        Desired Metric
    """
    def clean_descrip_title(row):
        punc_remover = str.maketrans('', '', string.punctuation)
        lowered = row['descrip_title'].lower()
        lowered_removed_punc = lowered.translate(punc_remover)
        cleaned_set = set(lowered_removed_punc.split())
        return cleaned_set

    def recall_keywords(row):
        return row['description_title_set'].intersection(row['course_keywords_set'])
    
    def cosine_similarity(x, y):
        return 1 - cosine(x,y)
    
    prediction_df = df_with_keywords.copy()
    only_predicted_keywords_df = prediction_df[prediction_df.columns.difference(['course_name', 'course_title', 'course_description', 'course_subject', 'course_alternative_names'])]
    num_keywords_predicted_per_course = only_predicted_keywords_df.shape[1]
    prediction_df['course_keywords'] = only_predicted_keywords_df.iloc[:,:].apply(lambda x: ', '.join(x), axis=1)
    prediction_df = prediction_df[['course_name', 'course_title', 'course_description', 'course_keywords', 'course_alternative_names']]
    prediction_df['course_keywords'] = prediction_df['course_keywords'].apply(lambda keywords: ', '.join(sorted(set([word.strip() for word in keywords.split(',')]))))
    prediction_df['course_keywords_set'] = prediction_df['course_keywords'].apply(lambda keywords: (set([word.strip() for word in keywords.split(',')])))
    prediction_df['descrip_title'] = prediction_df['course_title'] + ' ' + prediction_df['course_description']
    prediction_df['description_title_set'] = prediction_df.apply(clean_descrip_title, axis = 1)
    prediction_df['shared_words'] = prediction_df.apply(recall_keywords, axis = 1)
    
    if metric == 'r':
        print('[INFO] Calculating Recall...')
        assert num_keywords_predicted_per_course == max_descript_len, 'Number of keywords predicted should equal longest description length'
        prediction_df['recall'] = prediction_df['shared_words'].apply(lambda words: len(list(words)) / max_descript_len)
        average_recall = np.mean(prediction_df['recall'])
        return average_recall
    if metric == 'p':
        print('[INFO] Calculating Precision...')
        assert num_keywords_predicted_per_course == num_top_words, 'Number of keywords predicted should equal number of predicted words per course'
        prediction_df['precision'] = prediction_df['shared_words'].apply(lambda words: len(list(words)) / num_top_words)
        average_precision = np.mean(prediction_df['precision'])
        return average_precision
    if metric == 'c':
        print('[INFO] Calculating Cosine Similarity Between Keyword Distributions...')
        predicted_keyword_list = only_predicted_keywords_df.values.tolist()
        predicted_keyword_list = list(chain.from_iterable(predicted_keyword_list))
        keyword_counter = Counter(predicted_keyword_list)
        print('[INFO] Most common keywords by count: ', keyword_counter.most_common(10))
        
        num_possible_keywords = df_with_keywords.shape[0] * num_top_words
        num_predicted_keywords = len(keyword_counter.keys())
        assert sum(keyword_counter.values()) == split_Y_valid.shape[0] * num_top_words,\
        'Total number of predicted keywords should equal number of courses * number of predicted keywords per course.'
        unif_keyword_vector = np.repeat(num_possible_keywords / num_predicted_keywords, num_predicted_keywords)
        predicted_keyword_vector = np.array(list(keyword_counter.values()))
        assert unif_keyword_vector.shape == predicted_keyword_vector.shape,\
        'Uniform keyword frequency vector should have same dimension as predicted keywords frequency vector.'
    
        cos_sim = cosine_similarity(predicted_keyword_vector, unif_keyword_vector)
        return cos_sim
    if metric == 'df':
        print('[INFO] Calculating Document Frequency of Predicted Keywords across Course Subjects...')
        document_df_cols = df_with_keywords.columns.difference(['course_title', 'course_description', 'course_name', 'course_alternative_names'])
        document_df = df_with_keywords.loc[:,document_df_cols]
        document_df.set_index('course_subject', inplace=True)
        
        document_dict = defaultdict(list)
        terms = set()
        for index, row in document_df.iterrows():
            document_dict[index].extend(row.values)
            terms.update(row.values)

        doc_freq_dict = defaultdict()
        num_docs = len(document_dict.keys())
        for term in terms:
            doc_freq_i = 0
            for key in document_dict.keys():
                if term in document_dict.get(key):
                    doc_freq_i += 1
            doc_freq_dict[term] = doc_freq_i / (num_docs)
            
        print('[INFO] Most common keywords by document frequencies: ', Counter(doc_freq_dict).most_common(10)) 
        average_document_frequency_score = np.mean(list(doc_freq_dict.values()))
        return average_document_frequency_score

if __name__== "__main__":
    vec_frame = pd.read_csv(vectorfile, sep = '\t') # Vector space representation of each user, all numeric
    info_frame = pd.read_csv(infofile, sep = '\t') # Course information

    nonempty_indices = np.where(info_frame[textcolumn].notnull())[0]
    filtered_vec_frame = vec_frame.iloc[nonempty_indices,:].reset_index(drop = True)
    filtered_info_frame = info_frame.iloc[nonempty_indices,:].reset_index(drop = True)
    max_descript_len = max(filtered_info_frame.course_description.str.split().str.len())
    num_top_words = 10

    hyperparams_cols = ['use_idf', 'max_df','tf-bias', 'use_hidden_layer', 'num_epochs', 'recall@max_len', 'precision@10', 'distribution_diff', 'document_frequency']

    param_grid = {'use_idf': [True, False],
                'max_df': np.arange(.02, .06, .01),
                'tf_bias': np.append(np.arange(0, 2, .5), -999),
                'num_epochs': [10], 
                'use_hidden_layer': [False, True]} 

    grid = ParameterGrid(param_grid)

    recall_validation_scores = []
    precision_validation_scores = []
    distribution_validation_scores = []
    document_frequency_validation_scores = []
    grid_search_data = []

    for params in grid:
        print("***[INFO] Evaluating cross-validated model with hyperparams use_idf: %r, max_df: %f, tf_bias: %f, use_hidden_layer: %r, num_epochs: %d***" % 
            (params['use_idf'], params['max_df'], params['tf_bias'], params['use_hidden_layer'], params['num_epochs']))

        fold_num = 1
        kf = KFold(n_splits=4, random_state=42) # DO NOT FIX RANDOM STATE WHEN RUNNING THE ACTUAL EXPERIMENT - NVM, should be fixed for reproducibility
        for train_idx, valid_idx in kf.split(filtered_vec_frame):
            print('======== [INFO] Fold %d' % (fold_num))
            # X = vectors, Y = descriptions
            split_X_train, split_X_valid = filtered_vec_frame.iloc[train_idx], filtered_vec_frame.iloc[valid_idx]
            split_Y_train, split_Y_valid = filtered_info_frame.iloc[train_idx], filtered_info_frame.iloc[valid_idx]

            vocab = get_vocab(split_Y_train, textcolumn, max_df=params['max_df'], use_idf=params['use_idf']) 
            vocab_frame = pd.DataFrame(vocab)
            vocabsize = len(vocab)

            # Convert the textcolumn of the raw dataframe into bag of words representation
            split_Y_train_BOW = to_bag_of_words(split_Y_train, textcolumn, vocab, tf_bias=params['tf_bias'], use_idf=params['use_idf'])
            split_Y_train_BOW = split_Y_train_BOW.toarray()

    #         (weights_frame, biases) = logistic_regression(split_X_train.iloc[:,1:], split_Y_train_BOW, 
    #                                                       use_hidden_layer=params['use_hidden_layer'], num_epochs=params['num_epochs'])

            print('[INFO] Calculating recall@max_length...')
            df_with_keywords = logistic_regression(split_X_train.iloc[:,1:], split_Y_train_BOW, split_X_valid.iloc[:,1:], split_Y_valid, validation_vocab=vocab_frame, use_hidden_layer=params['use_hidden_layer'], num_epochs=params['num_epochs'], num_words_per_course=max_descript_len)
    #         df_with_keywords = predict(split_X_valid, split_Y_valid, weights_frame, biases, vocab_frame, max_descript_len)
            fold_i_average_recall = calculate_metric(df_with_keywords, 'r')
            recall_validation_scores.append(fold_i_average_recall)
            print('[INFO] Fold %d recall: %f.' % (fold_num, fold_i_average_recall))
            
            print('[INFO] Predicting on validation set for precision...')
            df_with_keywords = logistic_regression(split_X_train.iloc[:,1:], split_Y_train_BOW,  split_X_valid.iloc[:,1:], split_Y_valid, validation_vocab=vocab_frame, use_hidden_layer=params['use_hidden_layer'], num_epochs=params['num_epochs'], num_words_per_course=num_top_words)
    #         df_with_keywords = predict(split_X_valid, split_Y_valid, weights_frame, biases, vocab_frame, num_top_words)
            fold_i_average_precision = calculate_metric(df_with_keywords, 'p')
            precision_validation_scores.append(fold_i_average_precision)
            print('[INFO] Fold %d precision: %f.' % (fold_num, fold_i_average_precision))
            
            fold_i_distribution_diff = calculate_metric(df_with_keywords, 'c')
            distribution_validation_scores.append(fold_i_distribution_diff)
            print('[INFO] Fold %d cosine similarity: %f.' % (fold_num, fold_i_distribution_diff))
            
            fold_i_document_frequency = calculate_metric(df_with_keywords, 'df')
            document_frequency_validation_scores.append(fold_i_document_frequency)
            print('[INFO] Fold %d document frequency: %f.' % (fold_num, fold_i_document_frequency))

            fold_num += 1

        recall_i = np.mean(recall_validation_scores)
        precision_i = np.mean(precision_validation_scores)
        distribution_diff_i = np.mean(distribution_validation_scores)
        document_frequency_i = np.mean(document_frequency_validation_scores)

        model_i_params = [params['use_idf'], params['max_df'], params['tf_bias'], params['use_hidden_layer'],
                        params['num_epochs'], recall_i, precision_i, distribution_diff_i, document_frequency_i]

        grid_search_data.append(dict(zip(hyperparams_cols, model_i_params)))
        grid_search_df = pd.DataFrame(grid_search_data, columns=hyperparams_cols) 
        print(grid_search_df)
        grid_search_df.to_csv(scorefile_path, sep='\t', index=False)