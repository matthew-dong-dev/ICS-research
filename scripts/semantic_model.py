import os
import sys
import getopt
import subprocess
import time
import timeout_decorator
import pandas as pd
import numpy as np
from collections import Counter
from itertools import chain
import re
import string
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as stopwords
from keras.layers import Input, Dense
from keras.models import Model
from keras import backend as K
import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allocator_type = 'BFC'
config.gpu_options.allow_growth=True
sess = tf.Session(config=config)
K.set_session(sess)
pd.options.mode.chained_assignment = None 

vectorfile = ''
infofile = ''
outputfile = ''
write_directory = './outputted_keywords'

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hv:r:t:b:')
except getopt.GetoptError:
    print('\npython3 semantic_model.py -v <vectorfile> -r <infofile> -t <textcolumn> -b <tf_bias>')
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print('\npython3 semantic_model.py -v <vectorfile> -r <infofile> -t <textcolumn> -b <tf_bias>')
        print('<vectorfile> is the high dimensional vector\n<infofile> is the original input data')
        print('<textcolumn> is a column in raw file that needs nltk processing')
        print('<tf_bias> is the bias constant for term-frequency')
        sys.exit()
    if opt in ("-v"):
        print('[INFO] setting -v vectorfile')
        vectorfile = arg
    if opt in ("-r"):
        print('[INFO] setting -r infofile')
        infofile = arg
    if opt in ("-t"):
        print('[INFO] setting -t textcolumn')
        textcolumn = arg
    if opt in ("-b"):
        print('[INFO] setting -b tf-bias: ' + arg)
        tf_bias = float(arg)
if vectorfile == '':
    print('[DEBUG] option [-v] must be set\n')
    sys.exit()
if infofile == '':
    print('[DEBUG] option [-r] must be set\n')
    sys.exit()

@timeout_decorator.timeout(60, exception_message='timeout occured at get_vocab')
def get_vocab(dataframe, column, max_df=0.057611, use_idf=True):
    """Gets the vocab labels to be used as inferred keywords. 
    Args:
        Dataframe with column name (string) to parse vocab from.
        Max_df (float): max document frequency for sklearn's vectorizer.
        Use_idf (boolean): Use tf-idf to get top feature labels vs just using tf.
    Returns:
        Array of vocab labels.
    """
    print("[INFO] Getting vocab...")
    
    dataframe[column] = dataframe[column].fillna('')
    
    description_with_title = dataframe.course_title.fillna('') + ' ' + dataframe.course_description.fillna('')

    vectorizer = TfidfVectorizer(max_df=max_df, stop_words='english', ngram_range=(1,2), use_idf=use_idf, max_features=25000)
    X = vectorizer.fit_transform(description_with_title)
    vocab = vectorizer.get_feature_names()
    print('[INFO] Number vocab labels: %d' % (len(vocab)))
    
    vocab_list = list(vocab)
    removed_numbers_list = [word for word in vocab_list if not any(char.isdigit() for char in word)]
    vocab = np.array(removed_numbers_list)
    return vocab

@timeout_decorator.timeout(60, exception_message='timeout occured at to_bag_of_words')
def to_bag_of_words(dataframe, column, vocab, use_idf=True, tf_bias=None):
    """Converts text corpus into its BOW representation using predefined vocab.
    Fit tokenizes the strings / extracts the vocab & Transform converts each description into 
    a BOW vector / DTM
    BOW representation either uses: tf_idf (if use_idf = True), tf (if use_idf=False), binary counts (if tf-bias=0), tf-bias values otherwise 
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

@timeout_decorator.timeout(180, exception_message='timeout occured at logistic_regression')
def logistic_regression(X, Y, use_hidden_layer=False, hidden_layer_size=200, num_epochs=5, num_words_per_course=10):
    """Perform multinomial logistic regression from BOW vector space (Y) onto course vector space (X) and predict inferred keywords for each course. 
    Args: 
        X (numpy array): matrix of course vectors.
        Y (numpy array): corresponding descriptions as BOW encodings.
        number of epochs (int).
        num_words_per_course (int): Number of words to predict per course.
    Returns:
        Course description dataframe with a new column for every predicted word.
    """
    print('[INFO] Performing logistic regression...')

    inputs = Input(shape=(X.shape[1],)) # course vec
    if use_hidden_layer:
        hidden_layer = Dense(hidden_layer_size, activation='sigmoid')(inputs)
        predictions = Dense(vocabsize, activation='softmax')(hidden_layer)
    else:
        predictions = Dense(vocabsize, activation='softmax')(inputs)
    model = Model(inputs=inputs, outputs=predictions)
    model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
    model.fit(X, Y, epochs=num_epochs)

    # Obtain the softmax predictions for all instances 
    softmax_frame = pd.DataFrame(model.predict(X))
    
    # From the softmax predictions, save the top 10 predicted words for each data point
    print('[INFO] Sorting classification results...')
    sorted_frame = np.argsort(softmax_frame,axis=1).iloc[:, ::-1]
    
    return sorted_frame

def get_production_predictions(sorted_frame, num_words_per_course=10):
    """
    """
    print('[PRODUCTION] Predicting top k inferred keywords for each course...')
    df_with_keywords_production = filtered_info_frame.copy() # filtered_info_frame is global
    
    for i in range(num_words_per_course): # vocab_frame also global
        new_col = vocab_frame.iloc[sorted_frame.iloc[:,i],0] # get the ith top vocab word for each entry
        df_with_keywords_production['predicted_word_' + str(i+1)] = new_col.values
        
    return df_with_keywords_production

def generate_research_file(sorted_frame, num_words_per_course_research=3000):
    """
    """
    print('[RESEARCH] Predicting top k inferred keywords for each course...')
    df_with_keywords_research = filtered_info_frame.copy()
    
    # get enough predicted words such that 5 of those words in the description
    for i in range(num_words_per_course_research): 
        new_col = vocab_frame.iloc[sorted_frame.iloc[:,i],0] 
        df_with_keywords_research['predicted_word_' + str(i+1)] = new_col.values
        
    return df_with_keywords_research
    
def get_sorted_descriptions_words(course_description, predicted_words, k):
    """Top k words predicted by the model that are in the description.
    Args:
        course_description (series): description of course.
        predicted_words (series): Predicted words in the order they were ranked by the model.
        k (int): Number of words to return.
    Returns:
        List of k strings.
    """
    description_words = course_description.replace(',','').replace('.','').lower().split()
    predicted_words_list = list(predicted_words)
    predicted_words = pd.Series(range(0, len(predicted_words_list)), index=predicted_words_list)
    predicted_words = predicted_words[~predicted_words.index.duplicated()]
    sorted_description = predicted_words.reindex(description_words).dropna().sort_values()
    sorted_description_list = pd.Series(sorted_description.index).unique()[:k]
    return list(sorted_description_list) 

def get_top_non_description_words(course_description, predicted_words, k):
    """Top k words predicted by the model that are not in the description.
    Remark: Convert to a list comp / rewrite without for loops to increase efficiency. 
    Args:
        course_description (series): description of course.
        predicted_words (series): Predicted words in the order they were ranked by the model.
        k (int): Number of words to return.
    Returns:
        List of k strings.
    """ 
    description_words = course_description.replace(',','').replace('.','').lower().split()
    predicted_words_list = list(predicted_words)
    top_k_non_description_words = []
    for word in predicted_words_list:
        if word not in description_words and len(top_k_non_description_words) < k:
            top_k_non_description_words.append(word)
    return top_k_non_description_words  

def get_random_description_words(course_description, k):
    """Get k random words from a course's description. 
    Args:
        course_description (series): description of course.
        k (int): Number of words to return.
    Returns:
        List of k strings.
    """ 
    course_description_list = course_description.replace(',','').replace('.','').lower().split()
    course_description_no_stopwords = ' '.join([word for word in course_description_list if word not in (stopwords)])
    course_description_no_numbers = re.sub('[^\/A-Za-z\s-]','', course_description_no_stopwords) # [^\w\s]
    course_description_no_short_words = ' '.join([word for word in course_description_no_numbers.split() if len(str(word)) > 2])
    if len(course_description_no_short_words.split()) < k:
        return course_description_no_short_words.split()
    random_description_words = random.sample(course_description_no_short_words.split(), k)
    return random_description_words

def get_random_words(vocab, k):
    """Get k random words from all unigrams and bigrams from feature extraction phase.
    Args:
        Vocab (series): Collection of words to select from.   
        k (int): Number of words to return.
    Returns:
        List of k strings.
    """ 
    random_words = random.sample(list(vocab), k)
    return random_words

#manually setting model parameters, remove later
use_idf=False 
num_epochs=10
max_df=0.03
tf_bias=.5
use_hidden_layer=False

# MAIN
timebf = time.time()
print('[INFO] Start time: ' + str(timebf))

# get data
time_get_data_bf = time.time()
vec_frame = pd.read_csv(vectorfile, sep = '\t') # Vector space representation of each user, all numeric
info_frame = pd.read_csv(infofile, sep = '\t') # Course information
len_vec_frame = len(vec_frame.index)
len_info_frame = len(info_frame.index)
if (len_vec_frame != len_info_frame):
    print('[DEBUG] vector file and raw file entries do not line up: ' + str(len_vec_frame) + ' ' + str(len_info_frame))
    sys.exit()
nonempty_indices = np.where(info_frame[textcolumn].notnull() == True)[0]
filtered_vec_frame = vec_frame.iloc[nonempty_indices,:]
filtered_info_frame = info_frame.iloc[nonempty_indices,:]
time_get_data_af = time.time()
print('[INFO] Getting data took ' + str(time_get_data_af - time_get_data_bf))

# Get the vocab
time_get_vocab_and_bow_bf = time.time()
vocab = get_vocab(info_frame, textcolumn, use_idf=use_idf, max_df=max_df)
vocab_frame = pd.DataFrame(vocab)
vocabsize = len(vocab)
vocab_frame.to_csv(write_directory + '/complete-vocab.tsv', sep='\t', index=False)

# Convert the textcolumn of the raw dataframe into bag of words representation
filtered_bow_spmatrix = to_bag_of_words(filtered_info_frame, textcolumn, vocab, use_idf=use_idf, tf_bias=tf_bias)
filtered_bow_ndarray = filtered_bow_spmatrix.toarray()
time_get_vocab_and_bow_af = time.time()
print('[INFO] Getting vocab and BOW course representations took ' + str(time_get_vocab_and_bow_af - time_get_vocab_and_bow_bf))

# Train model and predict (Only train on course instances with non-empty texts)
time_train_model_bf = time.time()
sorted_frame = logistic_regression(filtered_vec_frame.iloc[:,1:], filtered_bow_ndarray, use_hidden_layer=use_hidden_layer, num_epochs=num_epochs)
df_with_keywords_production = get_production_predictions(sorted_frame) 
time_train_model_af = time.time()
print('[INFO] Training model took ' + str(time_train_model_af - time_train_model_bf))

print('[INFO] Writing results to file...')
time_writing_files_bf = time.time()
df_with_keywords_production.to_csv(outputfile+'.tsv', sep = '\t', index=False)
subprocess.call('mv '+outputfile+'.tsv'+' '+outputfile+'.txt', shell=True)
subprocess.call('mv '+outputfile+'.txt '+write_directory, shell=True)
time_writing_files_af = time.time()
print('[INFO] Writing files to file took ' + str(time_writing_files_af - time_writing_files_bf))

######### Generate research file
time_get_research_file_bf = time.time()
df_with_keywords_research = generate_research_file(sorted_frame)
info_columns = ['course_name', 'course_title', 'course_description', 'course_subject']
combined_cols = ['top_inferred_keywords', 'top_description_keywords', 
                'top_non_description_keywords', 'random_description_keywords', 'random_keywords', 
                'all_words', 'all_unique_words', 'num_total_words', 'num_unique_words']
description_words_cols = []
predicted_words_cols = []
top_non_description_cols = []
random_description_cols = []
random_words_cols = []

for i in range(1, 6): 
    description_words_cols.append('sorted_description_word_' + str(i))
    predicted_words_cols.append('predicted_word_' + str(i))
    top_non_description_cols.append('non_description_word_' + str(i))
    random_description_cols.append('random_description_word_' + str(i))
    random_words_cols.append('random_word_' + str(i))

final_cols = info_columns + combined_cols
word_cols = predicted_words_cols + description_words_cols + top_non_description_cols + random_description_cols + random_words_cols

# df_with_keywords_research.to_csv('/home/matthew/ICS-Research/intermediate0.csv', sep='\t', index=False)

k=5
df_with_keywords_research['top_inferred_keywords'] = df_with_keywords_research.filter(predicted_words_cols).apply(lambda x: ','.join(x).split(','), axis=1)
print('[RESEARCH] Getting sorted descriptions...')
df_with_keywords_research['top_description_keywords'] = df_with_keywords_research.apply(lambda x: get_sorted_descriptions_words(x['course_title'] + ' ' + x['course_description'], x.filter(regex=r'predicted_word_.*'), k), axis=1)
print('[RESEARCH] Getting top non description keywords...')
df_with_keywords_research['top_non_description_keywords'] = df_with_keywords_research.apply(lambda x: get_top_non_description_words(x['course_title'] + ' ' + x['course_description'], x.filter(regex=r'predicted_word_.*'), k), axis=1)
print('[RESEARCH] Getting random description keywords...')
df_with_keywords_research['random_description_keywords'] = df_with_keywords_research.apply(lambda x: get_random_description_words(x['course_title'] + ' ' + x['course_description'], k), axis=1)
print('[RESEARCH] Getting random keywords...')
df_with_keywords_research['random_keywords'] = df_with_keywords_research.apply(lambda x: get_random_words(vocab, k), axis=1)
df_with_keywords_research.reset_index(drop=True, inplace=True) # reset index is CRITICAL

# df_with_keywords_research.to_csv('/home/matthew/ICS-Research/intermediate1.csv', sep='\t', index=False)

print('[DEBUG] Running sanity check on research keywords.')
df_with_keywords_research['sorted_descriptions_set'] = df_with_keywords_research.top_description_keywords.apply(set)
df_with_keywords_research['non_description_keywords_set'] = df_with_keywords_research.top_non_description_keywords.apply(set)

def intersection(row):
    """Get number of words that appear in both the sorted description keywords and the non-description keywords
    Args: Row.
    Returns: Int.
    """ 
    return len(row['sorted_descriptions_set'] & row['non_description_keywords_set'])

assert(all(df_with_keywords_research.apply(intersection, axis=1)) == False)

print('[RESEARCH] Generating research file...')
user_study_df = df_with_keywords_research.copy()
sorted_description_df = pd.DataFrame(df_with_keywords_research.top_description_keywords.values.tolist(), columns=description_words_cols)
top_non_description_df = pd.DataFrame(df_with_keywords_research.top_non_description_keywords.values.tolist(), columns=top_non_description_cols)
random_description_words_df = pd.DataFrame(df_with_keywords_research.random_description_keywords.values.tolist(), columns=random_description_cols)
random_words_df = pd.DataFrame(df_with_keywords_research.random_keywords.values.tolist(), columns=random_words_cols)
user_study_df = pd.concat([user_study_df, sorted_description_df, top_non_description_df, random_description_words_df, random_words_df], axis=1)

all_words_df = user_study_df.filter(word_cols)
all_words_df.fillna('', inplace=True)
all_words = all_words_df.apply(lambda x: list(filter(None, ','.join(x).split(','))), axis=1)
user_study_df['all_words'] = all_words
user_study_df['all_unique_words'] = all_words.apply(lambda x: list(set(x)))
user_study_df['num_total_words'] = user_study_df.all_words.apply(len)
user_study_df['num_unique_words'] = user_study_df.all_unique_words.apply(len)
user_study_df = user_study_df.filter(final_cols)

RESEARCH_DIR = '/home/matthew/ICS-Research'
search_study_file_path = os.path.join(RESEARCH_DIR, 'search_study_file.tsv')
user_study_df.to_csv(search_study_file_path, sep='\t', index=False)

time_get_research_file_af = time.time()
print('[INFO] Getting research file took ' + str((time_get_research_file_af - time_get_research_file_bf)/60) + ' minutes.')

timeaf = time.time()
print('[INFO] End time: ' + str(timeaf))
print('[INFO] TOTAL time to run semantic_model.py:', (timeaf-timebf) / 60, 'minutes.')

