# Paths
export commonPath='/research/askoski_common' # Path to all the common files for the system
export dataPath='/research/UCBDATA' # Path to unhashed EDW data
export decryptedPath='/research/UCBDATA/decrypted' # Path to decrypted EDW data
export hashedPath='/research/UCBD2/edw_data' # Path to hashed EDW data
export classAPIPath='/research/UCBD2/classAPI' # Path to class api data
export modelPath='/home/askoski/Models-AskOski/outputs' # Path to where models alternatives
export localFilesPath='/home/askoski/Service-AskOski/not_public_data'
export jsonPath=$localFilesPath'/json'
export picklesPath=$localFilesPath'/pickles' # Path to relevant pickles
export flatFilesPath=$localFilesPath'/flat-files' # Path to relevant flat files
export logPath=$localFilesPath'/logs' # Path to relevant logs
export serendipitousPath='/research/salternatives' # Path to serendipitous alternatives

# Unhashed Files
export majorsFile=$dataPath'/edw_askoski_student_majors.txt' # EDW student majors file, used to get majors
export gradesFile=$dataPath'/edw_askoski_student_grades.txt' # EDW student grades file, used to get enrollment history
export cohortsFile=$dataPath'/edw_askoski_student_cohorts.txt' # EDW student cohorts file, used to get entry status
export reqsFile=$dataPath'/edw_askoski_apr_student_requirements.txt' # EDW student requirements file, used to create APR feature
export aprCourseFile=$dataPath'/edw_askoski_apr_course_lists.txt'

# Decrypted Files
export decryptedMajorsFile=$decryptedPath'/edw_askoski_student_majors_decrypted.txt' # EDW student majors file, used to get majors
export decryptedGradesFile=$decryptedPath'/edw_askoski_student_grades_decrypted.txt' # EDW student grades file, used to get enrollment history
export decryptedCohortsFile=$decryptedPath'/edw_askoski_student_cohorts_decrypted.txt' # EDW student cohorts file, used to get entry status
export decryptedReqsFile=$decryptedPath'/edw_askoski_apr_student_requirements_decrypted.txt' # EDW student requirements file, used to create APR feature
export decryptedAprCourseFile=$decryptedPath'/edw_askoski_apr_course_lists_decrypted.txt'

# Hashed Files
export hashedMajorsFile=$hashedPath'/edw_askoski_student_majors_hashed.txt'
export hashedGradesFile=$hashedPath'/edw_askoski_student_grades_hashed.txt'
export hashedCohortsFile=$hashedPath'/edw_askoski_student_cohorts_hashed.txt'
export hashedReqsFile=$hashedPath'/edw_askoski_apr_student_requirements_hashed.txt'

# APR Files
export academicPlanFile='/research/UCBD2/ACADEMIC_PLAN_HIERARCHY_D.txt'
export requirementsFile='/research/UCBD2/edw_data/edw_askoski_apr_student_requirements_hashed.txt'
export courseListFile='/research/UCBD2/edw_data/edw_askoski_apr_course_lists.txt'
export supplementaryCourseListFile='/research/UCBD2/edw_data/edw_askoski_apr_supplementary_course_lists.txt'
export subjectAbbreviationsFile='/research/UCBD2/Classes_2011_2018/class_outputs/abbreviations.tsv'

# Lookup Tables
export idx2courseFile=$modelPath'/idx2course.json' # RNN mapping of idx to cid
export course2idxFile=$modelPath'/course2idx.json' # RNN mapping of cid to idx
export idx2majorFile=$modelPath'/idx2major.json' # RNN mapping of idx to major
export entry2idxFile=$modelPath'/entry2idx.json' # RNN mapping of entry status to idx

# Model Files
export rnnModelFile=$modelPath'/askoski.json' # RNN architecture
export rnnWeightsFile=$modelPath'/askoski' # RNN weights
export bestC2V=$modelPath'/course2vec.npy' # C2V model, numpy array (300 or # of courses, 6359 or # of features)
export searchPick=$modelPath'/search_keywords.p' # inferred keywords output from semantic model

# Password Protected Bin Files
export sidHashBin=$commonPath'/bins/sidHash_new.bin'
export seedBin=$commonPath'/bins/seed.bin'
export readBin=$commonPath'/bins/read.bin'
export writeBin=$commonPath'/bins/write.bin'
export classesIdBin=$commonPath'/bins/classesId.bin'
export classesKeyBin=$commonPath'/bins/classesKey.bin'

# SSL Files
export key=$commonPath'/ssl/askoski.berkeley.key'
export crt=$commonPath'/ssl/oski.crt'

# Flat Files
export userEnrollmentsFile=$hashedPath'/userEnrollments_new.csv'
export majorLookupFile=$flatFilesPath'/majors.txt'
export subjConvFile=$flatFilesPath'/subj_abbrev.csv'
export subjDeptColDivFile=$flatFilesPath"/subject-dept-college-division.txt"
export crossListFile=$flatFilesPath"/crosslistings.csv"
export creditRestFile=$flatFilesPath"/creditrestrictions.csv"

# Pickle Files
export subjDeptColDivPick=$picklesPath"/subj_college_dict_new.p"
export crossListPick=$picklesPath"/crosslistings_new.p"
export creditRestPick=$picklesPath"/new_restrictions_new.p"
export subjConvPick=$picklesPath"/subj_conv_new.p"
export coursesPick=$picklesPath"/courses_new.p"
export nextSemDictPick=$classAPIPath"/next_sem_dict_new.p"
export nextSemClassesPick=$classAPIPath"/next_sem_classes_new.p"
export subjectCtrsPick=$picklesPath"/subjectCtrs_new.p"

export collegesPick=$picklesPath"/static/colleges.p"
export deptsPick=$picklesPath"/static/depts.p"
export divsPick=$picklesPath"/static/divs.p"
export majorsPick=$picklesPath"/static/otherMajors.p"

export registrarPick=$picklesPath"/registrar_recommended_CCNs.p"
export subjectCtrsPick=$picklesPath"/subjectCtrs.p"

# Serendipitous Alternatives Files
export bowCourseIdFile=$serendipitousPath'/BOW/course_id.pkl'
export bestModelFile=$serendipitousPath'/best_course2vec_BOW/best_course2vec.pkl'
export bowRelationMatrix=$serendipitousPath'/BOW/relation_matrix.npy'
export course2vectorBOWEquivalencyMatrix=$serendipitousPath'/best_course2vec_BOW/relation_matrix_equivalency.npy'
export courseDescriptionFile=$serendipitousPath'/BOW/course_description_final.csv'
export subjectIdFile='/research/jenny/course2vec/enroll_preprocess/subject_id.pkl'
export courseShortnameTitleFile='/research/jenny/course2vec/course_preprocess/course_shortname_title.pkl'
export courseFullnameTitleFile='/research/UCBD2/Classes_2011_2018/course_fullname_title.tsv'

# Log Files
export suggLog=$logPath'/suggestions_log.tsv'
export altLog=$logPath'/alternatives_log.tsv'
export reviewLog=$logPath'/reviews_log.tsv'

# Important Env Variables
export ENV='1341'
export getData='false' # true or false
export testID='24397735'
export termID='2198'
export semCode='3A851'
export currentYear='Fall 19'
export enrolledSem='Fall'
export enrolledYear='2018'
export contact1="chrisvle@berkeley.edu"
export contact2="pardos@berkeley.edu"
export guide2='?f[0]=im_field_term_name%'$semCode'&retain-filters=1'
export guide1='http://classes.berkeley.edu/search/site/'
export guide0='http://classes.berkeley.edu/search/class/'
export registrarList='https://spreadsheets.google.com/feeds/cells/1zCH0uf2xH8UVouA0kmMKD-SwEkM19ngcMjkHBAilfTE/1/public/values'
export degreePrograms="http://guide.berkeley.edu/undergraduate/degree-programs/"
export classAPI="https://apis.berkeley.edu/sis/v1/classes?term-id="
export classReservedSeatsAPI = 'https://apis.berkeley.edu/uat/sis/v1/classes/sections/'
export availableSeats = '/enrollment?seat-reservations=available'
export mailgunURL="https://api.mailgun.net/v3/sandbox76804c9965674d70aa186801c11a401e.mailgun.org/messages"
export rollbarServerToken='715774114cbe4f3aa8f0e083a97a8628'

export dateUpdated=2019-04-16
