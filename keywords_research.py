import time
import os
import pandas as pd
import numpy as np
from collections import Counter
from itertools import chain
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from scipy.spatial.distance import cosine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import KFold
from keras.layers import Input, Dense
from keras.models import Model
from keras import backend as K
import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.Session(config=config)
K.set_session(sess)
pd.options.mode.chained_assignment = None 

TRAINING_DIR = os.getcwd()
vectorfile = os.path.join(TRAINING_DIR, 'course_vecs.tsv')
infofile = os.path.join(TRAINING_DIR, 'course_info.tsv')
textcolumn = 'course_description'

# @timeout_decorator.timeout(600, exception_message='timeout occured at get_vocab')
def get_vocab(dataframe, column):
    print("[INFO] Getting vocab...")

    dataframe[column] = dataframe[column].fillna('')
    
    # max_df_param = 0.0028  # 1.0 # 0.0036544883

    vectorizer = TfidfVectorizer(max_df = max_df, stop_words='english', ngram_range=(1,1), use_idf=use_idf)
    X = vectorizer.fit_transform(dataframe[column])
    unigrams = vectorizer.get_feature_names()
    print('[INFO] Number of unigrams: %d' % (len(unigrams)))
    
    vectorizer = TfidfVectorizer(max_df = max_df, stop_words='english', ngram_range=(2,2), max_features=max(1, int(len(unigrams)/10)), use_idf=use_idf)
    X = vectorizer.fit_transform(dataframe[column])
    bigrams = vectorizer.get_feature_names()
    print('[INFO] Number of bigrams: %d' % (len(bigrams)))

    vectorizer = TfidfVectorizer(max_df = max_df, stop_words='english', ngram_range=(3,3), max_features=max(1, int(len(unigrams)/10)), use_idf=use_idf)
    X = vectorizer.fit_transform(dataframe[column])
    trigrams = vectorizer.get_feature_names()
    print('[INFO] Number of trigrams: %d' % (len(trigrams)))

    vocab = np.concatenate((unigrams, bigrams, trigrams))
    vocab_list = list(vocab)
    removed_numbers_list = [word for word in vocab_list if not any(char.isdigit() for char in word)]
    vocab = np.array(removed_numbers_list)
#     pd.DataFrame(vocab).to_csv(outputfile+'_vocab.tsv', sep = '\t', encoding='utf-8', index = False)
    return vocab

# @timeout_decorator.timeout(600, exception_message='timeout occured at to_bag_of_words')
def to_bag_of_words(dataframe, column, vocab):
    """Input: raw dataframe, text column, and vocabulary.
    Returns a sparse matrix of the bag of words representation of the column."""
    vectorizer = TfidfVectorizer(stop_words='english', vocabulary=vocab, use_idf=use_idf)
    X = vectorizer.fit_transform(dataframe[column].values.astype('U'))
    if tf_bias == -999:
        return X
    return (X.multiply(1/X.count_nonzero())).power(-tf_bias)

# @timeout_decorator.timeout(3600, exception_message='timeout occured at logistic_regression')
def logistic_regression(X, Y):
    print('[INFO] Performing logistic regression...')

    inputs = Input(shape=(X.shape[1],))
#     print('input shape: ', X.shape[1])  # 300 = number of cols in the feature matrix?
#     print('vocab size: ', vocabsize) # 2400 = len(get_vocab(raw_frame, textcolumn)) = num words parsed from description corpus
#     x = Dense(30, activation='sigmoid')(inputs)
#     predictions = Dense(vocabsize, activation='softmax')(x)
    predictions = Dense(vocabsize, activation='softmax')(inputs)
    model = Model(inputs=inputs, outputs=predictions)
    model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
    model.fit(X, Y, epochs=num_epochs)
    weights = model.layers[1].get_weights()[0]
    biases = model.layers[1].get_weights()[1]
    weights_frame = pd.DataFrame(weights)
    biases_frame = pd.DataFrame(biases)
#     weights_frame.to_csv(outputfile+'_weights.tsv', sep = '\t', index = False)
#     biases_frame.to_csv(outputfile+'_biases.tsv', sep = '\t', index = False)
    return(weights_frame, biases)

def predict(course_vecs, course_descipts, trained_weights, trained_biases, num_words_per_course):
    """
    lalalal
    
    """
    df_with_keywords = course_descipts.copy()
    softmax_frame = course_vecs.iloc[:,1:].dot(trained_weights.values) + trained_biases # make predictions

    # From the softmax predictions, save the top 10 predicted words for each data point
    print('[INFO] Sorting classification results...')
    sorted_frame = np.argsort(softmax_frame,axis=1).iloc[:,-num_words_per_course:]

    print('[INFO] Predicting top k inferred keywords for each course...')
    for i in range(num_words_per_course):
        new_col = vocab_frame.iloc[sorted_frame.iloc[:,i],0] # get the ith top vocab word for each entry
        df_with_keywords['predicted_word_' + str(num_words_per_course-i)] = new_col.values
        
    return df_with_keywords

def calculate_metric(df_with_keywords, metric):
    """
    metrics: {r: recall, p: precision}
    """
    def clean_descrip_title(row):
        punc_remover = str.maketrans('', '', string.punctuation)
        lowered = row['descrip_title'].lower()
        lowered_removed_punc = lowered.translate(punc_remover)
        cleaned_set = set(lowered_removed_punc.split())
        return cleaned_set

    def recall_keywords(row):
        return row['description_title_set'].intersection(row['course_keywords_set'])
    
    prediction_df = df_with_keywords.copy()
    only_predicted_keywords_df = prediction_df[prediction_df.columns.difference(['course_name', 'course_title', 'course_description', 'tf_bias', 'course_alternative_names'])]
    num_keywords_predicted = only_predicted_keywords_df.shape[1]
    prediction_df['course_keywords'] = only_predicted_keywords_df.iloc[:,:].apply(lambda x: ', '.join(x), axis=1)
    prediction_df = prediction_df[['course_name', 'course_title', 'course_description', 'course_keywords', 'course_alternative_names']]
    prediction_df['course_keywords'] = prediction_df['course_keywords'].apply(lambda keywords: ', '.join(sorted(set([word.strip() for word in keywords.split(',')]))))
    prediction_df['course_keywords_set'] = prediction_df['course_keywords'].apply(lambda keywords: (set([word.strip() for word in keywords.split(',')])))
    prediction_df['descrip_title'] = prediction_df['course_title'] + ' ' + prediction_df['course_description']
    prediction_df['description_title_set'] = prediction_df.apply(clean_descrip_title, axis = 1)
    prediction_df['shared_words'] = prediction_df.apply(recall_keywords, axis = 1)
    
    if metric == 'r':
        print('[INFO] Calculating Recall...')
        assert num_keywords_predicted == max_descript_len, 'Number of keywords predicted should equal longest description length'
        prediction_df['recall'] = prediction_df['shared_words'].apply(lambda words: len(list(words)) / max_descript_len)
        average_recall = np.mean(prediction_df['recall'])
        return average_recall
    if metric == 'p':
        print('[INFO] Calculating Precision...')
        assert num_keywords_predicted == num_top_words, 'Number of keywords predicted should equal number of predicted words per course'
        prediction_df['precision'] = prediction_df['shared_words'].apply(lambda words: len(list(words)) / num_top_words)
        average_precision = np.mean(prediction_df['precision'])
        return average_precision
    if metric == 'c':
        print('[INFO] Calculating Cosine Similarity Between Keyword Distributions...')
        predicted_keyword_list = only_predicted_keywords_df.values.tolist()
        predicted_keyword_list = list(chain.from_iterable(predicted_keyword_list))
        keyword_counter = Counter(predicted_keyword_list)
        
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

def cosine_similarity(x, y):
    return 1 - cosine(x,y)

vec_frame = pd.read_csv(vectorfile, sep = '\t') # Vector space representation of each user, all numeric
info_frame = pd.read_csv(infofile, sep = '\t') # Course information

nonempty_indices = np.where(info_frame[textcolumn].notnull())[0]
filtered_vec_df = vec_frame.iloc[nonempty_indices,:].reset_index(drop = True)
filtered_descript_df = info_frame.iloc[nonempty_indices,:].reset_index(drop = True)

max_descript_len = max(filtered_descript_df.course_description.str.split().str.len())

hyperparams_cols = ['tf-bias', 'max_df', 'num_epochs', 'recall', 'precision', 'distribution_diff']
grid_search_df = pd.DataFrame(columns=hyperparams_cols)

num_top_words = 10
use_idf = True
tf_bias = .5
num_epochs = 5
max_df = 0.0028

print('[INFO] Running cross validation...')

recall_validation_scores = []
precision_validation_scores = []
distribution_validation_scores = []
fold_num = 1
# X = vectors, Y = descriptions
kf = KFold(n_splits = 5, random_state = 42)
for train_idx, valid_idx in kf.split(filtered_vec_df):
    print('[INFO] ****** Fold %d ******' % (fold_num))
    
    split_X_train, split_X_valid = filtered_vec_df.iloc[train_idx], filtered_vec_df.iloc[valid_idx]
    split_Y_train, split_Y_valid = filtered_descript_df.iloc[train_idx], filtered_descript_df.iloc[valid_idx]
    
    vocab = get_vocab(split_Y_train, textcolumn) 
    vocab_frame = pd.DataFrame(vocab)
    vocabsize = len(vocab)

    # Convert the textcolumn of the raw dataframe into bag of words representation
    split_Y_train_BOW = to_bag_of_words(split_Y_train, textcolumn, vocab)
    split_Y_train_BOW = split_Y_train_BOW.toarray()
    
    (weights_frame, biases) = logistic_regression(split_X_train.iloc[:,1:], split_Y_train_BOW)
    
    print('[INFO] Predicting on validation set...')
    df_with_keywords = predict(split_X_valid, split_Y_valid, weights_frame, biases, max_descript_len)
    
    print('[INFO] Calculating Recall...')
    fold_i_average_recall = calculate_metric(df_with_keywords, 'r')
    recall_validation_scores.append(fold_i_average_recall)
    print('[INFO] Fold %d recall: %f.' % (fold_num, fold_i_average_recall))
    
    print('[INFO] Calculating Precision...')
    df_with_keywords = predict(split_X_valid, split_Y_valid, weights_frame, biases, num_top_words)
    fold_i_average_precision = calculate_metric(df_with_keywords, 'p')
    precision_validation_scores.append(fold_i_average_precision)
    print('[INFO] Fold %d precision: %f.' % (fold_num, fold_i_average_precision))
    
    fold_i_distribution_diff = calculate_metric(df_with_keywords, 'c')
    distribution_validation_scores.append(fold_i_distribution_diff)
    print('[INFO] Fold %d cosine similarity: %f.' % (fold_num, fold_i_distribution_diff))
    
    fold_num += 1
    
recall_i = np.mean(recall_validation_scores)
precision_i = np.mean(precision_validation_scores)
distribution_diff_i = np.mean(distribution_validation_scores)

model_i_params = [tf_bias, max_df, num_epochs, recall_i, precision_i, distribution_diff_i]
model_i_params = pd.DataFrame([model_i_params], columns=hyperparams_cols)
hyperparams_df = hyperparams_df.append(model_i_params, sort = False)

# print('recall scores:', recall_validation_scores)
# print('precision scores:', precision_validation_scores)
# print('distribution scores:', distribution_validation_scores)
print(hyperparams_df)