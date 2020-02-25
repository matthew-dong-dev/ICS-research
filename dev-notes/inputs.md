## List of Inputs for AskOski

### Service-AskOski

#### `env.sh`

| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| dateUpdated | Date of last refresh | N/A | 123 in `env.sh` |
| getData | | N/A | 104 in `env.sh` |
| key | SSL key | `$commonPath'/ssl/askoski.berkeley.key'`| 54 in `env.sh` |
| crt | SSL certificate | `$commonPath'/ssl/oski.crt'` | 55 in `env.sh` |
| idx2courseFile | JSON file path for idx2course | `$modelPath'/idx2course.json'` | 34 in `env.sh` |
| course2idxFile | JSON file path for course2idx | `$modelPath'/course2idx.json'` | 35 in `env.sh` |
| idx2majorFile | JSON file path for idx2major | `$modelPath'/idx2major.json'` | 36 in in `env.sh` |
| entry2idxFile | JSON file path for entry2idx | `$modelPath'/entry2idx.json'` | 37 in `env.sh` |
| rnnModelFile | file path for LSTM model architecture (JSON)| `$modelPath'/askoski.json'` | 40 in `env.sh` |
| rnnWeightsFile | file path for LSTM weights | `$modelPath'/askoski'` | 41 in `env.sh` |
| sidHashBin | | `$commonPath'/bins/sidHash_new.bin'` | 46 in `env.sh` |
| readBin | encrypted read password for MySQL database | `$commonPath'/bins/read.bin'` | 48 in `env.sh` |
| writeBin | encrypted write password for MySQL database | `$commonPath'/bins/write.bin'` | 49 in `env.sh` |
| userEnrollmentsFile | hashed enrollments csv file | `$hashedPath'/userEnrollments_new.csv'` | 59 in `env.sh` |
| subjConvPick | pickle file for TODO | `$picklesPath"/subj_conv_new.p"` | 70 in `env.sh` |
| subjDeptColDivPick | pickle file for TODO | `$picklesPath"/subj_college_dict_new.p"` | 67 in `env.sh` |
| crossListPick | pickle file for crosslisted courses | `$picklesPath"/crosslistings_new.p"` | 68 in `env.sh` |
| creditRestPick | pickle file for TODO | `$picklesPath"/new_restrictions_new.p"` | 69 in `env.sh` |
| nextSemDictPick | pickle file for TODO | `$classAPIPath"/next_sem_dict_new.p"` | 72 in `env.sh` |
| nextSemClassesPick | pickle file for TODO | `$classAPIPath"/next_sem_classes_new.p"` | 73 in `env.sh` |

##### Directory Paths

| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| commonPath | Path to all the common files for the system | `'/research/askoski_common'` | 3 in `env.sh` |
| dataPath | Path to unhashed EDW data | `'/research/UCBDATA'` | 4 in `env.sh` |
| hashedPath | Path to hashed EDW data | `'/research/UCBD2/edw_data'` | 5 in `env.sh` |
| classAPIPath | Path to class api data | `'/research/UCBD2/classAPI'` | 6 in `env.sh` |
| modelPath | Path to where models alternatives | `'/home/askoski/Models-AskOski/outputs'` | 7 in `env.sh` |
| localFilesPath | Path to confidential files | `'/home/askoski/Service-AskOski/not_public_data'` | 8 in `env.sh` |
| jsonPath | Path to all json files | `$localFilesPath'/json'` | 9 in `env.sh` |
| picklesPath | Path to relevant pickles | `$localFilesPath'/pickles'` | 10 in `env.sh` |
| flatFilesPath | Path to relevant flat files | `$localFilesPath'/flat-files'` | 11 in `env.sh` |
| logPath | Path to relevant logs | `$localFilesPath'/logs'` | 12 in `env.sh` |
| serendipitousPath | Path to serendipitous alternatives | `'/research/salternatives'` | 13 in `env.sh` |

##### Unhashed Files

| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| majorsFile | EDW student majors file, used to get majors | `$dataPath'/edw_askoski_student_majors.txt'` | 16 in `env.sh` |
| gradesFile | EDW student grades file, used to get enrollment history | `$dataPath'/edw_askoski_student_grades.txt'` | 17 in `env.sh` |
| cohortsFile | EDW student cohorts file, used to get entry status | `$dataPath'/edw_askoski_student_cohorts.txt'` | 18 in `env.sh` |
| reqsFile | EDW student requirements file, used to create APR feature | `$dataPath'/edw_askoski_apr_student_requirements.txt'` | 19 in `env.sh` |

##### Hashed Files

| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| hashedMajorsFile |  | `$hashedPath'/edw_askoski_student_majors_hashed.txt'` | 22 in `env.sh` |
| hashedGradesFile |  | `$hashedPath'/edw_askoski_student_grades_hashed.txt'` | 23 in `env.sh` |
| hashedCohortsFile |  | `$hashedPath'/edw_askoski_student_cohorts_hashed.txt'` | 24 in `env.sh` |
| hashedReqsFile |  | `$hashedPath'/edw_askoski_apr_student_requirements_hashed.txt'` | 25 in `env.sh` |

##### APR (Academic Progress Report) Files

| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| academicPlanFile |  | `'/research/UCBD2/ACADEMIC_PLAN_HIERARCHY_D.txt'` | 28 in `env.sh` |
| requirementsFile |  | `'/research/UCBD2/edw_data/edw_askoski_apr_student_requirements_hashed.txt'` | 29 in `env.sh` |
| courseListFile |  | `'/research/UCBD2/edw_data/edw_askoski_apr_course_lists.txt'` | 30 in `env.sh` |
| supplementaryCourseListFile |  | `'/research/UCBD2/edw_data/edw_askoski_apr_supplementary_course_lists.txt'` | 31 in `env.sh` |
| subjectAbbreviationsFile |  | `'/research/UCBD2/Classes_2011_2018/class_outputs/abbreviations.tsv'` | 32 in `env.sh` |

##### Lookup Tables

| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| idx2courseFile |  | `$modelPath'/idx2course.json' # RNN mapping of idx to cid` | 35 in `env.sh` |
| course2idxFile |  | `$modelPath'/course2idx.json' # RNN mapping of cid to idx` | 36 in `env.sh` |
| idx2majorFile |  | `$modelPath'/idx2major.json' # RNN mapping of idx to major` | 37 in `env.sh` |
| entry2idxFile |  | `$modelPath'/entry2idx.json' # RNN mapping of entry status to idx` | 38 in `env.sh` |

##### Model Files
| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| rnnModelFile |  | `$modelPath'/askoski.json' # RNN architecture` | 41 in `env.sh` |
| rnnWeightsFile |  | `$modelPath'/askoski' # RNN weights` | 42 in `env.sh` |
| bestC2V |  | `$modelPath'/course2vec.npy' # C2V model, numpy array (300 or # of courses, 6359 or # of features)` | 43 in `env.sh` |
| searchPick |  | `$modelPath'/search_keywords.pkl' # inferred keywords output from semantic model` | 44 in `env.sh` |
​
##### Password Protected Bin Files
| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| sidHashBin |  | `$commonPath'/bins/sidHash_new.bin'` | 47 in `env.sh` |
| seedBin |  | `$commonPath'/bins/seed.bin'` | 48 in `env.sh` |
| readBin |  | `$commonPath'/bins/read.bin'` | 49 in `env.sh` |
| writeBin |  | `$commonPath'/bins/write.bin'` | 50 in `env.sh` |
| classesIdBin |  | `$commonPath'/bins/classesId.bin'` | 51 in `env.sh` |
| classesKeyBin |  | `$commonPath'/bins/classesKey.bin'` | 52 in `env.sh` |

##### SSL Files
| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| key | SSL key | `$commonPath'/ssl/askoski.berkeley.key'` | 55 in `env.sh` |
| crt | SSL certificate | `$commonPath'/ssl/oski.crt'` | 56 in `env.sh` |

##### Flat Files
| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| userEnrollmentsFile |  | `$hashedPath'/userEnrollments_new.csv'` | 59 in `env.sh` |
| majorLookupFile |  | `$flatFilesPath'/majors.txt'` | 60 in `env.sh` |
| subjConvFile |  | `$flatFilesPath'/subj_abbrev.csv'` | 61 in `env.sh` |
| subjDeptColDivFile |  | `$flatFilesPath"/subject-dept-college-division.txt"` | 62 in `env.sh` |
| crossListFile |  | `$flatFilesPath"/crosslistings.csv"` | 63 in `env.sh` |
| creditRestFile |  | `$flatFilesPath'/creditrestrictions.csv'` | 64 in `env.sh` |

##### Pickle Files
| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| subjDeptColDivPick |  | `$picklesPath'/subj_college_dict_new.p'` | 67 in `env.sh` |
| crossListPick |  | `$picklesPath'/crosslistings_new.p'` | 68 in `env.sh` |
| creditRestPick |  | `$picklesPath'/new_restrictions_new.p'` | 69 in `env.sh` |
| subjConvPick |  | `$picklesPath'/subj_conv_new.p'` | 70 in `env.sh` |
| coursesPick |  | `$picklesPath'/courses_new.p'` | 71 in `env.sh` |
| nextSemDictPick |  | `$classAPIPath'/next_sem_dict_new.p'` | 72 in `env.sh` |
| nextSemClassesPick |  | `$classAPIPath'/next_sem_classes_new.p'` | 73 in `env.sh` |
| subjectCtrsPick |  | `$picklesPath'/subjectCtrs_new.p'` | 74 in `env.sh` |
| collegesPick |  | `$picklesPath'/static/colleges.p'` | 76 in `env.sh` |
| deptsPick |  | `$picklesPath'/static/depts.p'` | 77 in `env.sh` |
| divsPick |  | `$picklesPath'/static/divs.p'` | 78 in `env.sh` |
| majorsPick |  | `$picklesPath'/static/otherMajors.p'` | 79 in `env.sh` |
| registrarPick |  | `$picklesPath'/registrar_recommended_CCNs.p'` | 81 in `env.sh` |
| subjectCtrsPick |  | `$picklesPath'/subjectCtrs.p'` | 82 in `env.sh` |

##### Serendipitous Alternatives Files
| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| bowCourseIdFile |  | `$serendipitousPath'/BOW/course_id.pkl'` | 85 in `env.sh` |
| bestModelFile |  | `$serendipitousPath'/best_course2vec_BOW/best_course2vec.pkl'` | 86 in `env.sh` |
| bowRelationMatrix |  | `$serendipitousPath'/BOW/relation_matrix.npy'` | 87 in `env.sh` |
| course2vectorBOWEquivalencyMatrix |  | `$serendipitousPath'/best_course2vec_BOW/relation_matrix_equivalency.npy'` | 88 in `env.sh` |
| courseDescriptionFile |  | `$serendipitousPath'/BOW/course_description_final.csv'` | 89 in `env.sh` |
| subjectIdFile |  | `'/research/jenny/course2vec/enroll_preprocess/subject_id.pkl'` | 90 in `env.sh` |
| courseShortnameTitleFile |  | `'/research/jenny/course2vec/course_preprocess/course_shortname_title.pkl'` | 91 in `env.sh` |
| courseFullnameTitleFile |  | `'/research/UCBD2/Classes_2011_2018/course_fullname_title.tsv'` | 92 in `env.sh` |

##### Four Year Plan
| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| coursePredictionFile |  | `'/research/UCBD2/course_prediction_baseline.tsv'` | 95 in `env.sh` |
| classSectionFile |  | `'/research/UCBD2/Class_section_data/outputs/class_section.tsv'` | 96 in `env.sh` |

##### Log Files
| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| suggLog |  | `$logPath'/suggestions_log.tsv'` | 99 in `env.sh` |
| altLog |  | `$logPath'/alternatives_log.tsv'` | 100 in `env.sh` |
| reviewLog |  | `$logPath'/reviews_log.tsv'` | 101 in `env.sh` |

##### Other Environment Variables
| Name | Description | Value | Define Location |
|-----|-----| -----| -----|
| ENV |  | `'1341'` | 104 in `env.sh` |
| getData |  | `'false'` | 105 in `env.sh` |
| testID |  | `'24397735'` | 106 in `env.sh` |
| termID |  | `'2198'` | 107 in `env.sh` |
| semCode |  | `'3A851'` | 108 in `env.sh` |
| currentYear |  | `'Fall 19'` | 109 in `env.sh` |
| enrolledSem |  | `'Fall'` | 110 in `env.sh` |
| enrolledYear |  | `'2018'` | 111 in `env.sh` |
| mailgunKey |  | `'key-32232600888e04931773e38650963a0e'` | 112 in `env.sh` |
| contact1 |  | `'chrisvle@berkeley.edu'` | 113 in `env.sh` |
| contact2 |  | `'pardos@berkeley.edu'` | 114 in `env.sh` |
| guide2 |  | `'?f[0]im_field_term_name%'$semCode'&retain-filters1'` | 115 in `env.sh` |
| guide1 |  | `'http://classes.berkeley.edu/search/site/'` | 116 in `env.sh` |
| guide0 |  | `'http://classes.berkeley.edu/search/class/'` | 117 in `env.sh` |
| registrarList |  | `'https://spreadsheets.google.com/feeds/cells/1zCH0uf2xH8UVouA0kmMKD-SwEkM19ngcMjkHBAilfTE/1/public/values'` | 118 in `env.sh` |
| degreePrograms |  | `'http://guide.berkeley.edu/undergraduate/degree-programs/'` | 119 in `env.sh` |
| classAPI |  | `'https://apis.berkeley.edu/sis/v1/classes?term-id'` | 120 in `env.sh` |
| mailgunURL |  | `'https://api.mailgun.net/v3/sandbox76804c9965674d70aa186801c11a401e.mailgun.org/messages'` | 121 in `env.sh` |
| rollbarServerToken |  | `'715774114cbe4f3aa8f0e083a97a8628'` | 122 in `env.sh` |
| dateUpdated |  | `2019-04-16` | 123 in `env.sh` |

#### `load.py`

| Name | Description | Location | Read From |
|-----|-----|-----|-----|
| idx2course | dictionary that maps indices to course names | 73 in `load.py` | idx2courseFile |
| course2idx | dictionary that maps course names to indices | 74 in `load.py` | course2idxFile |
| read | read password for MySQL database | 103-104 in `load.py` | readBin |
| write | write password for MySQL database | 108-109 in `load.py` | writeBin |
| enrollments | enrollment data (could be actual data and dummy data) | 90-92, 123 in `load.py` | userEnrollmentsFile/dummy_enrollments |
| lookup_dict | TODO | 99, 124 in `load.py` | sidHashBin/dummy_lookup_dict |
| status_dict | TODO | 120, 125 in `load.py` | dummy_status_dict |
| subj_conv | dictionary of Subject Names to Abbreviations | 162 in `load.py` | subjConvPick |
| subj_college_lookup | comprehensive list of all subjects, departments, divisions and colleges | 164 in `load.py` | subjDeptColDivPick |
| crosslistings | dictionary of crosslistings | 168 in `load.py` | crossListPick |
| new_restrictions | dictionary of course restrictions | 171 in `load.py` | creditRestPick |

#### `refresh`

TODO

#### `service.py`

| Name | Description | Location | Read From |
|-----|-----|-----|-----|
| idx2major | RNN mapping of idx to major | 51-52 in `service.py` | idx2majorFile |
| idx2course | RNN mapping of idx to cid | 53-54 in `service.py` | idx2courseFile |

##### APR files

| Name | Description | Location | Read From |
|-----|-----|-----|-----|
| academic_plans |  | 84 in `service.py` | academic_plan_file |
| student_requirements |  | 85 in `service.py` | requirements_file |
| course_list |  | 86 in `service.py` | course_list_file |
| supplementary_course_list |  | 87 in `service.py` | supplementary_course_list_file |
| subject_abbreviations |  | 89 in `service.py` | subject_abbreviations_file |

##### Serendipitous

| Name | Description | Location | Read From |
|-----|-----|-----|-----|
| bow_course_id |  | 108 in `service.py` | bow_course_id_file |
| best_model |  | 109 in `service.py` | best_model_file |
| course_subject |  | 110 in `service.py` | subject_id_file |
| course_description |  | 111 in `service.py` | course_description_file |
| course_shortname_title |  | 112 in `service.py` | course_shortname_title_file |
| course_fullname_title |  | 113 in `service.py` | course_fullname_title_file |
| bow_relation_matrix |  | 114 in `service.py` | bow_relation_matrix_file |
| c2v_bow_equivalency_matrix |  | 115 in `service.py` | c2v_bow_equivalency_matrix_file |

##### Plan
| Name | Description | Location | Read From |
|-----|-----|-----|-----|
| course_prediction | | 125 in `service.py` | course_prediction_file |
| class_section | | 126-127 in `service.py` | class_section_file |
| major_dict | | 131 in `service.py` | idx2majorFile |
| c2v_model | | 134 in `service.py` | bestC2V |

##### Flask

###### `nextcourse()`
`@app.route('/nextcourse/predict', methods=['POST'])`

178-303 in `service.py`

| Name | Description | Location | Read From |
|-----|-----|-----|-----|
| sid | | 181 in `service.py` | `request.form['sid']` |
| status | | 182 in `service.py` | `request.form['status']` |
| filter_subj | | 183 in `service.py` | `request.form['filter_subj']` |
| filter_subj_drops | | 184 in `service.py` | `request.form['filter_subj_drops']` |
| filter_registrar | | 185 in `service.py` | `request.form['filter_registrar']` |
| filter_vacancy | | 186 in `service.py` | `request.form['filter_vacancy']` |
| filter_apr | | 187 in `service.py` | `request.form['filter_apr']` |
| filter_apr_requirements | | 188 in `service.py` | `request.form['filter_apr_requirements']` |
| bias_interest | | 189 in `service.py` | `request.form['bias_interest']` |
| bias_disinterest | | 190 in `service.py` | `request.form['bias_disinterest']` |
| bias_history | | 191 in `service.py` | `request.form['bias_history']` |
| token | | 192 in `service.py` | `request.form['token']` |

Uses `lookup_dict`, `db`, `major_dict`, `status_dict`, `enrollments`, `idx2course`, `idx2major`, `new_restrictions`, `crosslistings`, `next_sem_dict`

###### `similar_search()`
`@app.route('/similarcourse/search', methods=['POST'])`

305-373 in `service.py`

| Name | Description | Location | Read From |
|-----|-----|-----|-----|
| idx | | 308 in `service.py` | `request.form['idx']` |
| sid | | 309 in `service.py` | `request.form['sid']` |

Uses: `db`, `lookup_dict`, `course2idx`, `enrollments`, `idx2course`, `idx2major`, `new_restrictions`, `crosslistings` `next_sem_dict`

###### `serendipitous_search()`
`@app.route('/serendipitous/search', methods=['POST'])`

376-411 in `service.py`

| Name | Description | Location | Read From |
|-----|-----|-----|-----|
| idx | | 378 in `service.py` | `request.form['idx']` |
| include_graduate_courses | | 380 in `service.py` | `request.form['include_graduate_courses']` |

Uses: `best_c2v_bow`, `bow`

###### `auth()`
`@app.route('/auth', methods=['POST'])`

413-478 in `service.py`

| Name | Description | Location | Read From |
|-----|-----|-----|-----|
| url | | 416 in `service.py` | `request.form['url']` |
| ticket | | 417 in `service.py` | `request.form['ticket']` |

Uses: `db`

###### `authToken()`
`@app.route('/authToken', methods=['POST'])`

480-492 in `service.py`

| Name | Description | Location | Read From |
|-----|-----|-----|-----|
| token | | 482 in `service.py` | `request.form['token']` |
| sid | | 483 in `service.py` | `request.form['sid']` |

###### `get_apr_info()`
`@app.route('/getAprInfo', methods=['POST'])`

494-508 in `service.py`

| Name | Description | Location | Read From |
|-----|-----|-----|-----|
| sid | | 496 in `service.py` | `request.form['sid']` |

###### `get_plan_setting()`
`@app.route('/getPlanSetting', methods=['POST'])`

510-542 in `service.py`

| Name | Description | Location | Read From |
|-----|-----|-----|-----|
| sid | | 512 in `service.py` | `request.form['sid']` |

Uses: `db`

###### `get_plan()`
`@app.route('/getPlan', methods=['POST'])`

544-758 in `service.py`

| Name | Description | Location | Read From |
|-----|-----|-----|-----|
| sid | | 546 in `service.py` | `request.form['sid']` |
| status | | 547 in `service.py` | `request.form['status']` |
| is_regenerating | | 548 in `service.py` | `request.form['is_regenerating']` |
| include_summer_sessions | | 549 in `service.py` | `request.form['include_summer_sessions']` |
| current_major | | 550 in `service.py` | `request.form['current_major']` |
| max_credit_per_semester | | 551 in `service.py` | `request.form['max_credit_per_semester']` |
| last_semester | | 552 in `service.py` | `request.form['last_semester']` |

Uses: `lookup_dict`, `currentYear`, `db`, `enrollments`, `idx2course`

###### `selectOptions()`
`@app.route('/selectOptions', methods=['POST'])`

948-959 in `service.py`

| Name | Description | Location | Read From |
|-----|-----|-----|-----|
| select | | 950 in `service.py` | `request.form['select']` |

###### `getFullRows()`
`@app.route('/getFullRows', methods=['POST'])`

961-965 in `service.py`

| Name | Description | Location | Read From |
|-----|-----|-----|-----|
| select | | 950 in `service.py` | `request.form['select']` |

###### `rating()`
`@app.route('/rating', methods=['POST'])`

967-972 in `service.py`

| Name | Description | Location | Read From |
|-----|-----|-----|-----|
| sid | | 969 in `service.py` | `request.form['sid']` |
| version | | 970 in `service.py` | `request.form['version']` |
| rating | | 971 in `service.py` | `request.form['rating']` |

###### `email()`
`@app.route('/email', methods=['POST'])`

974-992 in `service.py`

| Name | Description | Location | Read From |
|-----|-----|-----|-----|
| name | | 976 in `service.py` | `request.form['name']` |
| email | | 977 in `service.py` | `request.form['email']` |
| subject | | 979 in `service.py` | `request.form['subject']` |
| message | | 980 in `service.py` | `request.form['message']` |

#### `refesh`

copies `/research/UCBDATA/edw_askoski_apr_course_lists.txt` to `/research/UCBD2/edw_data`
copies `/research/UCBDATA/hashed/*` to `/research/UCBD2/edw_data/`

Input Files:
| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| majorsFile |  | `$dataPath/edw_askoski_student_majors.txt` | 46 in `refresh.py` |
| gradesFile |  | `$dataPath/edw_askoski_student_grades.txt` | 47 in `refresh.py` |
| cohortsFile |  | `$dataPath/edw_askoski_student_cohorts.txt`| 48 in `refresh.py` |
| reqsFile |  | `$dataPath/edw_askoski_apr_student_requirements.txt` | 49 in `refresh.py` |


Variables:
| Name | Description | Location | Read From |
|-----|-----|-----|-----|
| myDict | dictionary containing passwords for startup | 40-43, 56 in `refresh.py` | `/research/askoski_common/bins/startup.bin` |
| courseListFile | | 65 in `refresh.py` | `/research/UCBDATA/edw_askoski_apr_course_lists.txt` |

### Models-AskOski

### RNN

#### `filepaths.json`

| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| grades | hashed student grades | `/research/UCBD2/edw_data/edw_askoski_student_grades_hashed.txt` | 2 in `filepaths.json` |
| majors | hashed student majors | `/research/UCBD2/edw_data/edw_askoski_student_majors_hashed.txt` | 3 in `filepaths.json` |
| entry | hashed student cohorts | `/research/UCBD2/edw_data/edw_askoski_student_cohorts_hashed.txt` | 4 in `filepaths.json` |

#### `preprocess.py`

Inputs:
`grades`, `majors`, `entry`

Outputs:

| Name | Description | File Path | Output Location |
|-----|-----| -----| -----|
| course2idx | | `/outputs/course2idx.json` | 90 in `preprocess.py` |
| idx2course | | `/outputs/idx2course.json` | 93 in `preprocess.py` |
| course_detail_dict | | `/outputs/course_detail_dict.json` | 96 in `preprocess.py` |
| major2idx | | `/outputs/major2idx.json` | 112 in `preprocess.py` |
| idx2major | | `/outputs/idx2major.json` | 115 in `preprocess.py` |
| undergrads_id | | `/outputs/undergrads_id.json` | 118 in `preprocess.py` |
| entry2idx | | `/outputs/entry2idx.json` | 129 in `preprocess.py` |
| enrollment_dict | | `/outputs/enrollment_dict.json` | 168 in `preprocess.py` |
| major_dict | | `/outputs/major_dict.json` | 193 in `preprocess.py` |
| entry_dict | | `/outputs/entry_dict.json` | 214 in `preprocess.py` |

#### `json2matrix.py`

Input Files:
| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| ENROLLMENT_JSON_DIR | | `/outputs/enrollment_dict.json` | 17 in `json2matrix.py` |
| ENTRY2IDX_DIR | | `/outputs/entry2idx.json` | 19 in `json2matrix.py` |
| ENTRY_DICT_DIR | | `/outputs/idx2course.json'` | 23 in `json2matrix.py` |
| MAJOR_DICT_DIR | | `/outputs/idx2major.json'` | 24 in `json2matrix.py` |
| MAJOR_DATA_DIR | | `/outputs/major_dict.json'` | 25 in `json2matrix.py` |
| COURSE_DETAIL_DIR | | `/outputs/course_detail_dict.json'` | 26 in `json2matrix.py` |
| UNDERGRADS_ID_DIR | | `/outputs/undergrads_id.json'` | 27 in `json2matrix.py` |
| GRADE_JSON_DIR | | `dummy.json` | 29 in `json2matrix.py` |
| GPA_JSON_DIR | | `dummy.json` | 30 in `json2matrix.py` |
| STUDENT_DETAIL_DIR | | `dummy.json` | 31 in `json2matrix.py` |

Variables:
| Name | Description | Location | Read From |
|-----|-----| -----| -----|
| course_dict | | 117 in `json2matrix.py` | COURSE_DICT_JSON_DIR |
| enrollment_dict | | 121 in `json2matrix.py` | ENROLLMENT_JSON_DIR |
| grade_dict | | 124 in `json2matrix.py` | GRADE_JSON_DIR |
| major_dict | | 127 in `json2matrix.py` | MAJOR_DICT_DIR |
| major_data | | 130 in `json2matrix.py` | MAJOR_DATA_DIR |
| student_detail_dict |  | 133 in `json2matrix.py` | STUDENT_DETAIL_DIR |
| course_detail_dict |  | 136 in `json2matrix.py` | COURSE_DETAIL_DIR |
| entry2idx |  | 139 in `json2matrix.py` | ENTRY2IDX_DIR |
| entry_dict |  | 142 in `json2matrix.py` | ENTRY_DICT_DIR |
| gpa_dict |  | 145 in `json2matrix.py` | GPA_JSON_DIR |
| undergrads_id |  | 148 in `json2matrix.py` | UNDERGRADS_ID_DIR |

Passes to `train.py`: `course_matrix`,  `major_matrix`, `grad_matrix`, `gpa_matrix`, `target_matrix`, `training_ppsk`, `evaluation_ppsk`

#### `train.py`

| Name | Description | File Path | Output Location |
|-----|-----| -----| -----|
| model | model architecture | `/outputs/askoski.json` | 97 in `train.py` |
| weights | model weights | `/outputs/askoski` | 98 in `train.py` |
| training logs | `askoski.log` | 121-125 in `train.py` |

#### `add_new_courses.py`

Input Files:
| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| NEXT_SEM_CLASSES_PATH | | `/research/UCBD2/classAPI/next_sem_classes_new.p` | 6 in `add_new_courses.py` |
| NEXT_SEM_DICT_PATH | | `/research/UCBD2/classAPI/next_sem_dict_new.p` | 7 in `add_new_courses.py` |
| COURSE2IDX_PATH | | `../outputs/course2idx.json` | 9 in `add_new_courses.py` |
| COURSE_DESCRIPTION_PATH | | `../shared/generate_descriptions/outputs/courses_with_description.tsv` | 14 in `add_new_courses.py` |

Variables:
| Name | Description | Location | Read From |
|-----|-----| -----| -----|
| des_df | course descriptions DataFrame | 21 in `add_new_courses.py` | COURSE_DESCRIPTION_PATH |
| course2idx | | 61 in `add_new_courses.py` | COURSE2IDX_PATH |
| new_sem_classes |  | 66 in `add_new_courses.py` | NEXT_SEM_CLASSES_PATH |

Outputs:

| Name | Description | File Path | Output Location |
|-----|-----| -----| -----|
| course2idx_new | | `../outputs/course2idx_new.json` | 87 in `add_new_courses.py` |
| idx2course_new | | `../outputs/idx2course_new.json` | 88 in `add_new_courses.py` |
| course2idx | | `../outputs/course2idx_all.json` | 89 in `add_new_courses.py` |
| idx2course | | `../outputs/idx2course_all.json` | 90 in `add_new_courses.py` |

#### `nearest_course.py`

Input Files:
| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| COURSE2IDX_PATH | | `../outputs/course2idx.json` | 9 in `add_new_courses.py` |
| COURSE2IDX_NEW_PATH | | `../outputs/course2idx_new.json` | 20 in `nearest_course.py` |

Variables:
| Name | Description | Location | Read From |
|-----|-----| -----| -----|
| course2idx | | 94 in `nearest_course.py` | COURSE2IDX_PATH |
| course2idx_new | | 95 in `nearest_course.py` | COURSE2IDX_NEW_PATH |

Outputs:

| Name | Description | File Path | Output Location |
|-----|-----| -----| -----|
| course2nb | | `../outputs/course2nb.json` | 101 in `nearest_course.py` |

#### `augment_model.py`

Input Files:
| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| COURSE2IDX_PATH | | `../outputs/course2idx.json` | 11 in `augment_model.py` |
| COURSE2NB_PATH | | `../outputs/course2nb.json` | 12 in `augment_model.py` |

Variables:
| Name | Description | Location | Read From |
|-----|-----| -----| -----|
| course2idx | | 69 in `augment_model.py` | COURSE2IDX_PATH |
| course2nb | | 71 in `augment_model.py` | COURSE2NB_PATH |

Outputs:

| Name | Description | File Path | Output Location |
|-----|-----| -----| -----|
| model_new | augmented model architecture |  `../outputs/askoski_new.json` (moved to `../outputs/askoski.json`) | 64 in `augment_model.py` |
| weights | augmented model weights | `../outputs/askoski_new` (moved to `../outputs/askoski`) | 65 in `augment_model.py`

### ICS

#### `data_joining.py`

Input Files:
| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| COURSE_VECTOR_DIR |  | `../outputs` | 7 in `data_joining.py` |
| COURSE_INFO_DIR |  | `../shared` | 8 in `data_joining.py` |
| vectors_path |  | `COURSE_VECTOR_DIR/course2vec.npy` | 11 in `data_joining.py` |
| vec2course_path |  | `COURSE_VECTOR_DIR/idx2course.json` | 12 in `data_joining.py` |
| course_info_path |  | `COURSE_INFO_DIR/course_info.tsv` | 13 in `data_joining.py` |

Variables:
| Name | Description | Location | Read From |
|-----|-----| -----| -----|
| vectors |  | 18 in `data_joining.py` | `vectors_path` |
| vec2course_map |  | 21 in `data_joining.py` | `vec2course_path` |
| descript_df |  | 38 in `data_joining.py` | `course_info_path` |
| vect_dict | `vectors` with indices shifted by 1 | 23-25 in `data_joining.py` | |
| vector_course_text_df | DataFrame merged from `descript_df` and `vect_dict` | 65-78 in `data_joining.py` | |

Outputs:

| Name | Description | File Path | Output Location |
|-----|-----| -----| -----|
| vector_text |  | `data/course_info.tsv` | 82 in `data_joining.py` |
| raw_vectors |  | `data/course_vecs.tsv` | 83 in `data_joining.py` |

#### `semantic_model.py`

Input Files: `./data/course_vecs.tsv`, `./data/course_info.tsv`

Variables:
| Name | Description | Location | Read From |
|-----|-----| -----| -----|
| vec_frame | Vector space representation of each user, all numeric | 257 in `semantic_model.py` | `./data/course_vecs.tsv` |
| info_frame | Course information | 258 in `semantic_model.py` | `./data/course_info.tsv` |

Outputs:
| Name | Description | File Path | Output Location |
|-----|-----| -----| -----|
| vocab_frame |  | `./outputted_keywords/complete-vocab.tsv` | 277 in `semantic_model.py` |
| user_study_df |  | `/home/matthew/ICS-Research/search_study_file.tsv` | 394 in `semantic_model.py` |
| course_softmax_map |  | `data/course_keyword_probabilites.pkl` | 318 in `data_joining.py` |

#### `threshold-keywords.py`

Input Files:
| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| user_study_file |  | `./data/user-study-ratings-with-probs.csv` | 32 in `threshold-keywords.py` |
| infofile |  | `./data/course_info.tsv` | 46 in `threshold-keywords.py` |


Variables:
| Name | Description | Location | Read From |
|-----|-----| -----| -----|
| ratings |  | 32 in `threshold-keywords.py` | `user_study_file` |
| info_frame |  | 48 in `threshold-keywords.py` | `infofile` |
| course_softmax_map |  | 51 in `threshold-keywords.py` | `data/course_keyword_probabilites.pkl` |
| filtered_info_frame | non-empty columns of `info_frame` | 73-82 in `threshold-keywords.py` | |

Outputs:
| Name | Description | File Path | Output Location |
|-----|-----| -----| -----|
| production_frame | `DISPLAYED_COLUMNS` of `filtered_info_frame` | `../outputs/search_keywords.pkl`| 83 in `threshold-keywords.py` |

### C2V

#### `preprocess.py`

Input Files:
| Name | Description | File Path | Define Location |
|-----|-----| -----| -----|
| PATH_CONFIG |  | `../shared` | 10 in `preprocess.py` |
| SRC_DIR |  | `/research/UCBD2/edw_data` | 11 in `preprocess.py` |
| RNN_DIR |  | `../outputs` | 12 in `preprocess.py` |
| C2V_DIR |  | `../outputs` | 13 in `preprocess.py` |

Variables:
| Name | Description | Location | Read From |
|-----|-----| -----| -----|
| course_id |  | 192 in `preprocess.py` | `../outputs/course2idx.json` |
| data |  | 25 in `preprocess.py` | `/research/UCBD2/edw_data/edw_askoski_student_grades_hashed.txt`

Outputs:
| Name | Description | File Path | Output Location |
|-----|-----| -----| -----|
| filter_course_id |  | `../outputs/filter_out_courseID.npy` | 41 in `preprocess.py` |
| instructor |  | `../outputs/instructor_id.pkl` | 113 in `preprocess.py` |
| subject |  | `../outputs/subject_id.pkl` | 134 in `preprocess.py` |
| mat_file |  | `../outputs/stu_sem_course&instructor&subject.pkl` | 178 in `preprocess.py` |

#### `data_sampling.py`

Input Files: `../outputs/stu_sem_course&instructor&subject.pkl`

Variables:
| Name | Description | Location | Read From |
|-----|-----| -----| -----|
| data |  | 17-18 in `data_sampling.py` | `../outputs/stu_sem_course&instructor&subject.pkl` |

Outputs:
| Name | Description | File Path | Output Location |
|-----|-----| -----| -----|
| all_data | sampled data | `../outputs/sampled_data_10.pkl` | 38 in `data_sampling.py` |
| samling log |  | `sampling.log` | |

#### `course_ins_sub_torch.py`

Variables:
| Name | Description | Location | Read From |
|-----|-----| -----| -----|
| course_id |  | 121 in `course_ins_sub_torch.py` | `../outputs/c../outputs/ourse2idx.json` |
| subject |  | 124 in `course_ins_sub_torch.py` | `../outputs/subject_id.pkl` |
| instructor |  | 128 in `course_ins_sub_torch.py` | `../outputs/instructor_id.pkl` |
| data | sampled data | 133 in `course_ins_sub_torch.py` | `../outputs/sampled_data_10.pkl` |

Outputs:
| Name | Description | File Path | Output Location |
|-----|-----| -----| -----|
| saved model |  | `../outputs/course2vec_ins_sub.pkl` | 162 in `course_ins_sub_torch.py` |
| course2vec |  | `../outputs/course2vec.npy` | 176 in `course_ins_sub_torch.py` |
| training log |  | `train.log` | |
