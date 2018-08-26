import pandas as pd
import numpy as np
import sys
import os
import string
import pickle

KEYWORDS_OUTPUT_DIR = '../outputted_keywords' # os.getcwd()
VEC_TEXT_DIR = '../input_data/'
df_list = []
grouped_keywords_path = '../outputted_keywords/keywords_descrip_title.tsv'
unique_keywords_path = '../outputted_keywords/unique_keywords_df.tsv'
# grouped_keywords_df = pd.DataFrame()
# unique_keywords_df = pd.DataFrame()
# titles_file_path = os.path.join(VEC_TEXT_DIR, 'vector_text.tsv') 

'''
Inferred keywords data to be used for production
'''
def get_production_keywords():
    print('[INFO] Writing keywords to production...')
    unique_keywords_df = pd.read_csv(unique_keywords_path, sep = '\t')
    production_keywords = unique_keywords_df[['course_number', 'course_title', 'description', 'keywords']]
    output_pkl_path = os.path.join(KEYWORDS_OUTPUT_DIR, 'production_keywords.p') # cannot have leading backslash
    pickle_out = open(output_pkl_path,"wb")
    pickle.dump(production_keywords, pickle_out)
    pickle_out.close()
    print('[INFO] Write complete, output file at production_keywords.p')
    
'''
After outputting the trained keywords and grouping them together, get the unique ones not in the description
@param
@return
'''
def get_unique_keywords():
    print('[INFO] Getting unique keywords...')
    keywords_df = pd.read_csv(grouped_keywords_path, sep = '\t')
    keywords_df['keywords_set'] = keywords_df['keywords'].apply(lambda keywords: (set([word.strip() for word in keywords.split(',')])))
    keywords_df['descrip_title'] = keywords_df['course_title'] + ' ' + keywords_df['description']
    keywords_df['description_set'] = keywords_df.apply(clean_descrip_title, axis = 1)
    keywords_df['unique_keywords_set'] = keywords_df.apply(find_unique_keywords_set, axis = 1)
    keywords_df['num_uniq_keywords'] = keywords_df['unique_keywords_set'].apply(lambda keyword_set: len(list(keyword_set)))
    keywords_df['unique_keywords'] = keywords_df.apply(find_unique_keywords, axis = 1)
    
    print('[INFO] average number of unique keywords per course %f' % np.mean(keywords_df['num_uniq_keywords'])) 
    keywords_df.to_csv(KEYWORDS_OUTPUT_DIR + '/unique_keywords_df.tsv', sep = '\t', index = False)
    print('[INFO] Getting unique keywords done, output file at unique_keywords_df.tsv')
    
'''
Pandas manipulation to be able to collect the keywords for each bias level and aggregate them into a single group
@param
@return
'''
def group_keywords(df_list):
    read_files_to_df()
    print('[INFO] Grouping keywords...')
#     print(pd.concat(df_list).shape)
    joined_df = pd.concat(df_list)
    joined_df.to_csv(KEYWORDS_OUTPUT_DIR + '/joined_df.tsv', sep = '\t', index = False)
    keyword_df = joined_df.groupby(list(joined_df.columns)).count().reset_index()
#     print(keyword_df.iloc[:,:3].head(5))
#     print(keyword_df.columns)
    predicted_keywords = keyword_df[keyword_df.columns.difference(['course_number', 'course_title', 'description', 'tf_bias'])]
    keyword_df['keywords'] = predicted_keywords.iloc[:,:].apply(lambda x: ', '.join(x), axis=1)
    keyword_df = keyword_df[['course_number', 'course_title', 'description', 'keywords']]
    descript_keywords = keyword_df.groupby(['course_number', 'course_title', 'description'])['keywords'].apply(', '.join).reset_index()
#     print(descript_keywords['keywords'])
    descript_keywords['keywords'] = descript_keywords['keywords'].apply(lambda keywords: ', '.join(sorted(set([word.strip() for word in keywords.split(',')]))))
    descript_keywords.to_csv(KEYWORDS_OUTPUT_DIR + '/descript_keywords.tsv', sep = '\t', index = False)
#     print(descript_keywords['keywords'])
#     print(titles_file_path)
#     course_titles = pd.read_csv(titles_file_path, sep = '\t')
#     df_with_titles = pd.merge(descript_keywords, course_titles, how = 'right', on = 'course_number')
#     df_with_titles = df_with_titles[['course_number', 'course_title', 'description_x', 'keywords']]
#     df_with_titles.rename(columns = {'description_x': 'description'}, inplace = True)
#     df_with_titles = df_with_titles.fillna('')
#     print(df_with_titles.head(5))
    descript_keywords.to_csv(KEYWORDS_OUTPUT_DIR + '/keywords_descrip_title.tsv', sep = '\t', index = False)
    grouped_keywords_df = descript_keywords
    print('[INFO] Grouping keywords done, all keywords at keywords_descrip_title.tsv')
    
'''
Helper function Read each file in the directory to a pandas dataframe, extract the bias value, 
and add a column with that value for all the courses
@return
'''
def read_files_to_df():
    print('[INFO] Converting files to pandas dataframes...')
    for file in os.listdir(KEYWORDS_OUTPUT_DIR):
        if file.endswith(".txt"):
            file_path = os.path.join(KEYWORDS_OUTPUT_DIR, os.path.basename(file))
            tf_bias_value = float(os.path.basename(file)[-7:-4])

            # read to df and insert bias value
            df_with_keywords = pd.read_csv(file_path, sep = '\t')
            num_rows = df_with_keywords.shape[0]
            # print(num_rows)
            df_with_keywords.insert(loc = 3, column= 'tf_bias', value = [tf_bias_value] * num_rows) 
            df_list.append(df_with_keywords)
            os.remove(os.path.join(KEYWORDS_OUTPUT_DIR, os.path.basename(file)))
        # print(df_list)
    print('[INFO] Files converted to pandas dataframes...')
    
'''
Helper function that creates a set for each course description by removing punctuation, converting to lower case, and splitting on space
@param
@return
'''
def clean_descrip_title(row):
    punc_remover = str.maketrans('', '', string.punctuation)
    lowered = row['descrip_title'].lower()
    lowered_removed_punc = lowered.translate(punc_remover)
    cleaned_set = set(lowered_removed_punc.split())
    return cleaned_set
  
'''
Helper function returns the set difference between the keywords and the description 
(the words in keywords but not in the description)
@param
@return
'''
def find_unique_keywords_set(row):
    return row['keywords_set'] - row['description_set']

'''
Helper function returns the string version of the set difference between the keywords and the description 
(the words in keywords but not in the description)
@param
@return
'''
def find_unique_keywords(row):
    set_diff = row['keywords_set'] - row['description_set']
    return ', '.join(sorted(list(set_diff)))


def main():
    try:
        group_keywords(df_list)
        get_unique_keywords()
        get_production_keywords()
    except:
        sys.exit('ERROR: failed to get keywords')

if __name__ == "__main__": main()


