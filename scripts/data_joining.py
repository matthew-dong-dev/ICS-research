import pandas as pd
import numpy as np
import pickle
import os
import json

COURSE_VECTOR_DIR = '../outputs'
COURSE_INFO_DIR = '../shared'
INPUT_DIR = os.getcwd()
OUTPUT_DIR = './data'
vectors_path = os.path.join(COURSE_VECTOR_DIR, 'course2vec.npy')
vec2course_path = os.path.join(COURSE_VECTOR_DIR, 'idx2course.json')
course_info_path = os.path.join(COURSE_INFO_DIR, 'course_info.tsv')

print('[INFO] Begin data preprocessing stage...')
print('[INFO] Reading in course vectors...')

vectors = np.load(vectors_path)

with open(vec2course_path) as json_data:
    vec2course_map = json.load(json_data)

vect_dict = {}
for vector_id in vec2course_map.keys():
    vect_dict[int(vector_id)] = vectors[int(vector_id)-1]
    
vect_df = pd.DataFrame(vect_dict).T
vect_df.index.name = 'vector_id'
vect_df.reset_index(inplace = True)

course_identifier_list = [vec2course_map[str(vec_id)] for vec_id in vect_df['vector_id']]
vect_df.insert(loc = 1, column = 'course_identifier', value = course_identifier_list)

print('[INFO] Transforming vectors done.')

print('[INFO] Reading in course descriptions...')

descript_df = pd.read_csv(course_info_path, sep = '\t', ).drop(['Unnamed: 0', 'idx', 'updated_date'],axis=1)

descript_df['course_name'] = descript_df['abbr_cid'].str.replace('_', ' ').str.lower().str.capitalize()
descript_df['course_alternative_names'] = descript_df['course_subject'] + ' ' + descript_df['course_num']
descript_df['course_alternative_names'] = descript_df['course_alternative_names'] + ' ' + descript_df['abbr_cid'].str.replace('_', '')
descript_df['course_identifier'] = descript_df['course_subject'] + '_' + descript_df['course_num']
descript_df.drop(['course_num', 'abbr_cid'], axis = 1 ,inplace = True)
descript_df.rename(columns = {'title': 'course_title', 'description': 'course_description'}, inplace = True)

print('[INFO] Transforming course descriptions done.')

print('[INFO] Removing courses with generic descriptions.')
descript_df = descript_df[~descript_df.course_description.isna()]
courses_to_remove = ['Freshman Seminar', 'Freshman Seminars', 'Freshman/Sophomore Seminar', 'Sophomore Seminar', 'Sophomore Seminars', 'Berkeley Connect']
remove_regex = '|'.join(courses_to_remove)
descript_df = descript_df[~descript_df.course_title.str.contains(remove_regex, regex=True)]
descript_df = descript_df[~descript_df.course_name.str.contains('99')]
descript_df = descript_df[~descript_df.course_name.str.contains('98')]
descript_df = descript_df[~descript_df.course_name.str.contains('97')]
descript_df = descript_df[~descript_df.course_title.str.contains('special topics', case=False)]
descript_df = descript_df[~descript_df.course_identifier.str.contains('FPF', case=True)]

print('[INFO] Removing courses with generic descriptions done.')

print('[INFO] Merging vectors and descriptions...')

vector_course_text_df = pd.merge(vect_df, descript_df, on = 'course_identifier', how = 'left')
vector_course_text_df.drop('course_identifier', axis = 1, inplace = True)
vector_course_text_df = vector_course_text_df[vector_course_text_df['course_name'].notnull()]

print('[INFO] Extract raw course vectors...')

raw_vectors = vector_course_text_df[vector_course_text_df.columns.difference(['course_title', 'course_description', 'course_subject', 'course_alternative_names'])]
cols = list(raw_vectors.columns)
cols = [cols[-2]] + cols[:-2] 
raw_vectors = raw_vectors[cols]

print('[INFO] Extract corresponding course information...')

vector_text = vector_course_text_df[['course_name', 'course_title', 'course_description', 'course_subject', 'course_alternative_names']]

print('[INFO] Reading to tsv files...')

vector_text.to_csv(OUTPUT_DIR+'/course_info.tsv', sep='\t', index = False)
raw_vectors.to_csv(OUTPUT_DIR+'/course_vecs.tsv', sep='\t', index = False)

print('[INFO] Data preprocessing complete.')
