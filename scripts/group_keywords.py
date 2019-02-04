import pandas as pd
import numpy as np
import sys
import os
import string
import pickle

KEYWORDS_OUTPUT_DIR = './outputted_keywords'
df_list = []
grouped_keywords_path = './outputted_keywords/keywords_descrip_title.tsv'
unique_keywords_path = './outputted_keywords/unique_keywords_df.tsv'
# grouped_keywords_df = pd.DataFrame()
# unique_keywords_df = pd.DataFrame()

def get_production_keywords():
    """Pickle inferred keywords data."""
    print('[INFO] Pickling keywords...')
    unique_keywords_df = pd.read_csv(unique_keywords_path, sep = '\t')
    production_keywords = unique_keywords_df[['course_name', 'course_title', 'course_description', 'course_keywords', 'course_alternative_names']]
    output_pkl_path = os.path.join(KEYWORDS_OUTPUT_DIR, 'new_version_keywords.p') # cannot have leading backslash
    pickle_out = open(output_pkl_path, "wb")
    pickle.dump(production_keywords, pickle_out)
    pickle_out.close()
    print('[INFO] Pickle file at ' + output_pkl_path)
    
def get_unique_keywords():
    """After outputting the trained keywords and grouping them together, get the unique ones not in the description."""
    print('[INFO] Getting unique keywords...')
    keywords_df = pd.read_csv(grouped_keywords_path, sep = '\t')
    keywords_df['keywords_set'] = keywords_df['course_keywords'].apply(lambda keywords: (set([word.strip() for word in keywords.split(',')])))
    keywords_df['descrip_title'] = keywords_df['course_title'] + ' ' + keywords_df['course_description']
    keywords_df['description_set'] = keywords_df.apply(clean_descrip_title, axis=1)
    keywords_df['unique_keywords_set'] = keywords_df.apply(find_unique_keywords_set, axis=1)
    keywords_df['num_uniq_keywords'] = keywords_df['unique_keywords_set'].apply(lambda keyword_set: len(list(keyword_set)))
    keywords_df['unique_keywords'] = keywords_df.apply(find_unique_keywords, axis=1)
    
    print('[INFO] average number of unique keywords per course %f' % np.mean(keywords_df['num_uniq_keywords'])) 
    keywords_df.to_csv(KEYWORDS_OUTPUT_DIR + '/unique_keywords_df.tsv', sep = '\t', index = False)
    print('[INFO] Getting unique keywords done, output file at unique_keywords_df.tsv')

def group_keywords(df_list):
    """Collect the keywords predicted at each bias level and aggregate them into a single dataframe.
    Args:
        df_list (list): List of dataframes with predicted keywords
    """
    read_files_to_df()
    print('[INFO] Grouping keywords...')
#     print(pd.concat(df_list).shape)
    joined_df = pd.concat(df_list)
    joined_df.to_csv(KEYWORDS_OUTPUT_DIR + '/joined_df.tsv', sep = '\t', index = False)
    keyword_df = joined_df.groupby(list(joined_df.columns)).count().reset_index() # removes courses with no description
#     keyword_df.to_csv(KEYWORDS_OUTPUT_DIR + '/user_study_file.tsv',sep='\t', index=False)
    predicted_keywords = keyword_df[keyword_df.columns.difference(['course_name', 'course_title', 'course_description', 'tf_bias', 'course_alternative_names', 'course_subject'])]
    keyword_df['course_keywords'] = predicted_keywords.iloc[:,:].apply(lambda x: ', '.join(x), axis=1)
    keyword_df = keyword_df[['course_name', 'course_title', 'course_description', 'course_keywords', 'course_alternative_names', 'course_subject']]
    descript_keywords = keyword_df.groupby(['course_name', 'course_title', 'course_description', 'course_alternative_names', 'course_subject'])['course_keywords'].apply(', '.join).reset_index()
    descript_keywords['course_keywords'] = descript_keywords['course_keywords'].apply(lambda keywords: ', '.join(sorted(set([word.strip() for word in keywords.split(',')]))))
    descript_keywords.to_csv(KEYWORDS_OUTPUT_DIR + '/keywords_descrip_title.tsv', sep='\t', index=False)
    grouped_keywords_df = descript_keywords
    print('[INFO] Grouping keywords done, all keywords at keywords_descrip_title.tsv')
    
def read_files_to_df():
    """Helper function to read each file in the directory to a pandas dataframe, extract the bias value, 
    and add a column with that value for all the courses
    """
    print('[INFO] Converting files to pandas dataframes...')
    for file in os.listdir(KEYWORDS_OUTPUT_DIR):
        if file.endswith(".txt"):
            file_path = os.path.join(KEYWORDS_OUTPUT_DIR, os.path.basename(file))
            try:
                tf_bias_value = float(os.path.basename(file)[-7:-4])
            except:
                tf_bias_value = -999

            # read to df and insert bias value
            df_with_keywords = pd.read_csv(file_path, sep = '\t')
            num_rows = df_with_keywords.shape[0]
            # print(num_rows)
            df_with_keywords.insert(loc = 3, column= 'tf_bias', value = [tf_bias_value] * num_rows) 
            df_list.append(df_with_keywords)
            os.remove(os.path.join(KEYWORDS_OUTPUT_DIR, os.path.basename(file)))
#         print(df_list)
    print('[INFO] Files converted to pandas dataframes...')

def clean_descrip_title(row):
    """Helper function that creates a set for each course description + title by removing punctuation, converting to lower case, and splitting on space
    Args:
        row of a dataframe
    Returns:
        Set of words for a particular course description 
    """
    punc_remover = str.maketrans('', '', string.punctuation)
    lowered = row['descrip_title'].lower()
    lowered_removed_punc = lowered.translate(punc_remover)
    cleaned_set = set(lowered_removed_punc.split())
    return cleaned_set
  
def find_unique_keywords_set(row):
    """Helper function returns the set difference between the keywords and the description (the words in keywords but not in the description)
    Args:
        row of dataframe
    Returns: 
        Set difference between keywords_set and description_set
    """
    return row['keywords_set'] - row['description_set']

def find_unique_keywords(row):
    """Helper function returns the string version of the set difference between the keywords and the description 
    Cannot be condensed with find_unique_keywords_set because used as an apply function
    Args:
        row
    Returns:
        ...
    """
    set_diff = row['keywords_set'] - row['description_set']
    return ', '.join(sorted(list(set_diff)))

def main():
    try:
        group_keywords(df_list)
        get_unique_keywords()
        get_production_keywords()
    except Exception as ex:
        print(ex)
#         template = "An exception of type {0} occurred. Arguments:\n{1!r}"
#         message = template.format(type(ex).__name__, ex.args)
#         print(message)

if __name__ == "__main__": main()
