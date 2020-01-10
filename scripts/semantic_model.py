import os
import sys
import getopt
import time
import pickle
import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from nltk.corpus import stopwords 
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras import backend as K
import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
K.set_session(sess)
OUT_DIR = os.environ["outDir"]
DISPLAYED_COLUMNS = ['course_id', 'course_title', 'course_description', 'course_keywords', 'course_alternative_names']

# manually setting model parameters
use_idf=True
max_df=0.03
tf_bias=-999
use_MLP=False
num_epochs=10
batch_size=16

try:
    opts, args = getopt.getopt(sys.argv[1:], 'hv:i:')
except getopt.GetoptError:
    print('\npython3 semantic_model.py -v <vectorfile> -i <infofile>')
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print('\npython3 semantic_model.py -v <vectorfile> -i <infofile> -t <textcolumn> -b <tf_bias>')
        print('<vectorfile> location of word embeddings you would like to perform semantic analysis on')
        print('<infofile> location of text-valued data corresponding to word embeddings')
        sys.exit()
    if opt in ("-v"):
        print('[INFO] setting -v vectorfile')
        vectorfile = arg
    if opt in ("-i"):
        print('[INFO] setting -i infofile')
        infofile = arg
        textcolumn = arg
if vectorfile == '':
    print('[DEBUG] option [-v] must be set\n')
    sys.exit()
if infofile == '':
    print('[DEBUG] option [-i] must be set\n')
    sys.exit()
    
def get_vocab(descript_frame, max_df, use_idf):
    """Gets the vocab labels to be used as inferred keywords. 
    Args:
        Dataframe with column name (string) to parse vocab from.
        Max_df (float): max document frequency for sklearn's vectorizer, filters out common words.
        Use_idf (boolean): Use tf-idf to get top feature labels vs just using tf.
    Returns:
        Array of vocab labels.
    """

    stop_words = set(stopwords.words('english'))
    description_with_title = descript_frame.course_title + ' ' + descript_frame.course_description
    
    unigram_vectorizer = TfidfVectorizer(max_df=max_df, stop_words=stop_words, ngram_range=(1,1), 
                             token_pattern=r'(?u)\b[A-Za-z]+\b',
                             use_idf=use_idf, lowercase=True, max_features=None)
    unigram_vectorizer.fit_transform(description_with_title)
    unigrams = unigram_vectorizer.get_feature_names()
    print('[INFO] Number unigrams: %d' % (len(unigrams)))
    
    bigram_vectorizer = TfidfVectorizer(stop_words=stop_words, ngram_range=(2,2), 
                             token_pattern=r'(?u)\b[A-Za-z]+\b',
                             use_idf=use_idf, lowercase=True, max_features=int(len(unigrams)/10))
    
    bigram_vectorizer.fit_transform(description_with_title)
    bigrams = bigram_vectorizer.get_feature_names()
    print('[INFO] Number bigrams: %d' % (len(bigrams)))
    
    vocab = list(np.concatenate((unigrams, bigrams)))
    vocab = [topic for topic in vocab if len(topic) > 3]
    
    print('[INFO] Number vocab labels: %d' % (len(vocab)))
    return vocab

def generate_labels(course_description, vocab):
    
    # Remove punctuations and numbers
    course_description = re.sub('[^a-zA-Z]', ' ', course_description)

    # Removing multiple spaces
    course_description = re.sub(r'\s+', ' ', course_description)

    # Convert to lowercases
    course_description = course_description.lower()
    
    description_bigrams = generate_ngrams(course_description, 2)
    bigram_labels = [bigram for bigram in description_bigrams if bigram in vocab]
    bigram_label_string = ' '.join(bigram_labels)

    description_unigrams = course_description.split()
    unigram_labels = [word for word in description_unigrams if word in vocab and word not in bigram_label_string]
    
    labels = unigram_labels + bigram_labels

    return set(labels)

def generate_ngrams(course_description, n):
    
    # Remove punctuations and numbers
    course_description = re.sub(r'[^a-zA-Z]', ' ', course_description)
    
    # Removing multiple spaces
    course_description = re.sub(r'\s+', ' ', course_description)
    
    # Convert to lowercases
    course_description = course_description.lower()
    
    # Break course_description in the token, remove empty tokens
    tokens = [token for token in course_description.split(" ") if token != ""]
    
    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]

def to_bag_of_words(descript_frame, vocab, tf_bias):
    """Converts text corpus into its BOW representation using predefined vocab.
    Fit tokenizes the strings / extracts the vocab & Transform converts each description into 
    a BOW vector / DTM
    BOW representation either uses: tf_idf (if use_idf = True), tf (if use_idf=False), binary counts (if tf-bias=0), tf-bias values otherwise 
    Args:
        raw dataframe, text column, and vocabulary.
    Returns:
        A sparse matrix of the bag of words representation of the column.
    """
    
    description_with_title = descript_frame.course_title + ' ' + descript_frame.course_description
    mlb = MultiLabelBinarizer()
    description_with_title_labels = description_with_title.apply(lambda description: generate_labels(description, vocab))
    description_bow = mlb.fit_transform(description_with_title_labels)
    
    if tf_bias == -999:
        print('[INFO] Not using tf-bias')
        return mlb, description_bow
    else:
        print('[INFO] Using tf-bias value: ' + str(tf_bias))
        return mlb, (description_bow.multiply(1/description_bow.count_nonzero())).power(-tf_bias)

def logistic_regression(X, Y, use_MLP, num_epochs, batch_size):
    """Perform multinomial logistic regression from BOW vector space (Y) onto course vector space (X) and predict inferred keywords for each course. 
    Args: 
        X (numpy array): matrix of course vectors.
        Y (numpy array): corresponding descriptions as BOW encodings.
        number of epochs (int).
        num_words_per_course (int): Number of words to predict per course.
    Returns:
        softmax frame - each row is a probability distribution over all words for each course, to be sorted later
    """
    input_dim = X.shape[1]
    output_dim = Y.shape[1]
    model = Sequential()
    
    if use_MLP:
        model.add(Dense(hidden_layer_size=200, input_dim=input_dim, activation='relu'))
        model.add(Dropout(0.4))
        model.add(Dense(output_dim, activation='softmax'))
    else:
        model.add(Dense(output_dim, input_dim=input_dim, activation='softmax'))
        
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X, Y, epochs=num_epochs, batch_size=batch_size)
    prob_ndarray = model.predict(X) # Obtain the probability scores for all topics for each course 
    return prob_ndarray

def get_production_predictions(prob_ndarray, descript_frame, label_vocab, num_words_per_course=10):
    """Given the sorted probability distributions for each course, get the top k words for each course
    Args: 
        sorted_frame (numpy array): matrix of indices
        num_words_per_course (int): number of inferred keywords to predict for every course
    Returns:
        Course description dataframe with a new column for every predicted word.
    """
        
    print('[INFO] Sorting classification results...')
    sorted_indices = np.argsort(prob_ndarray,axis=1)[:, ::-1]
    
    print('[INFO] Predicting top k inferred keywords for each course...')
    df_with_keywords = descript_frame.copy()
    predicted_words_cols = []
    for i in range(num_words_per_course): 
        predicted_words_cols.append('predicted_word_' + str(i+1))
        df_with_keywords['predicted_word_' + str(i+1)] = label_vocab[sorted_indices[:,i]]  # get the ith top vocab word for each entry
    df_with_keywords['course_keywords'] = df_with_keywords.filter(predicted_words_cols).apply(lambda x: ', '.join(x), axis=1)
    return df_with_keywords
        
def output_production_keywords(df, OUT_DIR):
    """Pickle inferred keywords data."""
    print('[INFO] Pickling keywords...')
    output_pkl_path = os.path.join(OUT_DIR, 'search_keywords.pkl')
    pickle_out = open(output_pkl_path, "wb")
    pickle.dump(df, pickle_out)
    pickle_out.close()
    print('[INFO] Pickled file at ' + output_pkl_path)

def main():
    timebf = time.time()
    
    print("[INFO] Loading data...")
    vec_df = pd.read_csv(vectorfile, sep = '\t') # Vector space representation of each user, all numeric
    descript_df = pd.read_csv(infofile, sep = '\t') # Course information
    print("[INFO] Getting vocab...")
    vocab = get_vocab(descript_df, use_idf=use_idf, max_df=max_df)
    print("[INFO] Convert the textcolumn of the raw dataframe to bag of words...")
    mlb, bow_ndarray = to_bag_of_words(descript_df, vocab, tf_bias)
    print('[INFO] Performing logistic regression...')
    prob_ndarray = logistic_regression(vec_df.values, bow_ndarray, use_MLP, num_epochs, batch_size)
    df_with_keywords = get_production_predictions(prob_ndarray, descript_df, mlb.classes_, num_words_per_course=5)
    
    df_with_keywords.rename(columns={'course_name': 'course_id'}, inplace=True)
    df_with_keywords = df_with_keywords[DISPLAYED_COLUMNS]
    df_with_keywords.course_id = df_with_keywords.course_id.str.replace(',', '').str.upper()
    df_with_keywords = df_with_keywords.sort_values('course_id')
    output_production_keywords(df_with_keywords, OUT_DIR)
    
    timeaf = time.time()
    print('[INFO] TOTAL time to run semantic_model.py:', (timeaf-timebf) / 60, 'minutes.')

if __name__== "__main__":
    main()
    