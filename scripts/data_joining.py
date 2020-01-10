import pandas as pd
import numpy as np
import pickle
import os
import json

OUT_DIR = os.environ["outDir"]
COURSE_VECTOR_DIR = OUT_DIR
COURSE_INFO_DIR = '../shared/course_api/outputs'
INTERMEDIATE_DATA_DIR = './data'
vectors_path = COURSE_VECTOR_DIR + '/course2vec.npy'
vec2course_path = COURSE_VECTOR_DIR + '/idx2course.json'
course_info_path = COURSE_INFO_DIR + '/course_description_init.tsv'

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
vect_df.insert(loc = 1, column = 'vector_course_identifier', value = course_identifier_list)

print('[INFO] Transforming vectors done.')

print('[INFO] Reading in course descriptions...')

descript_df = pd.read_csv(course_info_path, sep = '\t', )[['abbr_cid', 'course_num', 'course_subject', 'course_description', 'course_title']]

descript_df['course_name'] = descript_df['abbr_cid'].str.replace('_', ' ').str.lower().str.capitalize()
descript_df['course_alternative_names'] = descript_df['course_subject'] + ' ' + descript_df['course_num']
descript_df['course_alternative_names'] = descript_df['course_alternative_names'] + ' ' + descript_df['abbr_cid'].str.replace('_', '')
# add custom abbreviations here
descript_df['vector_course_identifier'] = descript_df['course_subject'] + '_' + descript_df['course_num']
descript_df.drop(['course_num', 'abbr_cid'], axis = 1 ,inplace = True)

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
descript_df = descript_df[~descript_df.course_title.str.contains('seminar', case=False)]
descript_df = descript_df[~descript_df.course_subject.str.contains('FPF', case=True)]

print('[INFO] Removing courses with generic descriptions done.')

print('[INFO] Merging vectors and descriptions...')

vector_course_text_df = pd.merge(vect_df, descript_df, on = 'vector_course_identifier', how = 'left')
vector_course_text_df.drop('vector_course_identifier', axis = 1, inplace = True)
vector_course_text_df = vector_course_text_df[vector_course_text_df['course_name'].notnull()]

print('[INFO] Extract raw course vectors...')

raw_vectors = vector_course_text_df[vector_course_text_df.columns.difference(['course_name', 'course_title', 'course_description', 'course_subject', 'course_alternative_names', 'vector_id'])]

print('[INFO] Extract corresponding course information...')
vector_text = vector_course_text_df[['course_name', 'course_title', 'course_description', 'course_subject', 'course_alternative_names']]

print('[INFO] Writing to tsv files...')

vector_text.to_csv(INTERMEDIATE_DATA_DIR+'/aligned_course_info.tsv', sep='\t', index = False)
raw_vectors.to_csv(INTERMEDIATE_DATA_DIR+'/aligned_course_vecs.tsv', sep='\t', index = False)

print('[INFO] Data preprocessing complete.')
