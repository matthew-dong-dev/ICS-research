# how to run pipeline

1. `chmod -R 777` Data-AskOski & Models-AskOski if necessary - what is this command doing? 
1. make sure both Data & Models are on the right branch and have pulled most recent changes
1. Run `refresh.py` in screen
1. how long does entire retraining take? 
    - Hashing - 5mins 
    - Models retraining - currently like 10 hours 
    - refresh api - 1 hour ish
1. Verify pipeline has successfully by copying env.json to service and results are as expected `cp /home/matthew/Data-AskOski/env.json /home/matthew/Service-AskOski/service`
1. Currently fixed / hardcoded folders needed for pipeline to run
    - `hashed`, `encypted`, `decrypted` folders in UCBDATA
    - `classAPI` in UCBD2
    - some static files in Jeff's local directory
1. NLTK Dependencies
    >>> import nltk
    >>> nltk.download('stopwords')
    >>> nltk.download('punkt')
    >>> nltk.download('wordnet')
    move to: 
    - '/usr/nltk_data'
    - '/usr/share/nltk_data'
    - '/usr/lib/nltk_data'
    - '/usr/share/nltk_data'
    - '/usr/local/share/nltk_data'
    - '/usr/lib/nltk_data'
    - '/usr/local/lib/nltk_data'
1. Sandbox testing environment 
    - To test changes just clone the repo to your directory & replace `/home/askoski/Models-AskOski` pathways with local version `/home/matthew/Models-AskOski`
    - Change output pathways? No just delete the timestamped output 
1. can you run pipeline parts in isolation?  Yes, just run the individual retrain scripts but should not do this during full run through even if RNN retraining is completed because all the models all need to write their outputs referencing the same timestamped directory 

---

## [Data-Pipeline] Deep dive

1. look into refresh.md & env.sh - these files are outdated, but tells a lot about how things work
1. look into how the hashing works
    - "The lookup table will be stored in /research/UCBD2/edw_data/TIMESTAMP"
    - what is sidHashBin file?  what are .bin files?
    - what is sid_to_hash.txt? (is this the actual lookup file?)  the file is being removed in utils.py
    - look at the indexing error action item in data-action-items.md
    - "biggest pain point is the lookup_dict (anon to SID) because if this is wrong then everything else is wrong in terms of the other lookup tables for majors / courses.  how does the main sid to anon lookup work and how does that affect the course indexing?"
    - hashed vs encrypted data - which one is the anonymized using the lookup dict?  hashed?  Yes
    - Encryption is a two-way function where information is scrambled in such a way that it can be unscrambled later.
    - "Hashing, one-way function where data is mapped to a fixed-length value. Hashing is primarily used for authentication. With a properly designed algorithm, there is no way to reverse the hashing process to reveal the original password."  So if there's a lookup dict that maps original sids to anons, is it really hashed?
    - Salting is an additional step during hashing, typically seen in association to hashed passwords, that adds an additional value to the end of the password that changes the hash value produced. This adds a layer of security to the hashing process, specifically against brute force attacks. A brute force attack is where a computer or botnet attempt every possible combination of letters and numbers and characters until the password is found.  They can also attempt to hash every possible combination of letters and numbers and characters (companies use well known hashing functions?) until your pw is found, don't even have to know the actual password.  Adding salt creates unique pw's and therefore unique hashes so if a hacker finds one, he doesn't find another.    

    
1. look at imported functions in refresh.py - what is refresh user, enrollments, grade_info, etc... doing

--- 


## [Data] Deep dive

1. clean ucbd2-archive & update spreadsheet, check what each file does and where it already exists in the system before deleting
    - start with hashed-archive
        - edw_askoski_apr_supplementary_course_lists --> exists inside APR folder of timestamped directory
        - edw_2018.tsv --> hashed grades old file
        - data.dict --> meta data
    - *Don't delete the encrypted files o/w you have to wait for the next data dump*
1. what is the size of the data being used - how many records, how far back - see the research paper
    - 100K students, 2M enrollment records, since 2008
1. incorporate Zihao's updated dictionaries and RNN model (found in /research/UCBD2) into staging. His RNN model weights are in a binary file called "askoski", the topology of the model is in "askoski.json" and "askoski.desc" just describes the hyper parameters that were used. The dictionary file "course2idx.json" can be used to translate between "Subject CourseNum" and the one-hot index for the model and "major2idx.json" can be used to translate the major to major one-hot index. Jenny's word2vec model is called "w2v_300_15_20_3.model" and uses the same indices as course2idx.
1. look at the structure of the files

/research/UCBD2/pipeline-test/hashed
edw_askoski_apr_student_requirements_hashed.txt  edw_askoski_student_grades_hashed.txt
edw_askoski_student_cohorts_hashed.txt           edw_askoski_student_majors_hashed.txt

> edw_askoski_apr_student_requirements_hashed.txt 

REQUIREMENT|EFFDT|ACAD_PLAN|ACAD_SUB_PLAN|SAA_DESCR80_MAIN_TBL|RQ_LINE_NBR|SAA_DESCR80_RQ_LINE_TBL|REQ_LINE_TYPE|COURSE_LIST|ITEM_R_STATUS|LOAD_DATE|`ANON_ID`

> edw_askoski_apr_student_requirements.txt (unhashed)

#STUDENT_ID|REQUIREMENT|EFFDT|ACAD_PLAN|ACAD_SUB_PLAN|SAA_DESCR80_MAIN_TBL|RQ_LINE_NBR|SAA_DESCR80_RQ_LINE_TBL|REQ_LINE_TYPE|COURSE_LIST|ITEM_R_STATUS|LOAD_DATE

> edw_askoski_student_grades_hashed.txt

#SEMESTER_YEAR_NAME_CONCAT|STUDENT_CREDIT_HRS_NBR|COURSE_CONTROL_NBR|INSTR_NAME_CONCAT|OFFERING_TYPE_DESC|ROOM_SHARE_BUNDLE_NBR|SECTION_NBR|COURSE_SUBJECT_NAME_NUMBER|UNDERGRAD_GRAD_STATUS|COURSE_NUMBER|COURSE_SUBJECT_SHORT_NM|COURSE_TITLE_NM|CRS_ACADEMIC_DEPT_SHORT_NM|GRADE_NM|GRADE_POINTS_NBR|GRADE_SORT_NBR|GRADE_SUBTYPE_DESC|GRADE_TYPE_DESC|SEMESTER_YEAR|SEMESTER_NAME|SNAPSHOT_CODE|LOAD_DATE|`ANON_ID`

## Unhashed

#SEMESTER_YEAR_NAME_CONCAT|STUDENT_ID|STUDENT_CREDIT_HRS_NBR|PERSON_PARTY_SK|COURSE_CONTROL_NBR|INSTR_NAME_CONCAT|OFFERING_TYPE_DESC|ROOM_SHARE_BUNDLE_NBR|SECTION_NBR|COURSE_SUBJECT_NAME_NUMBER|UNDERGRAD_GRAD_STATUS|COURSE_NUMBER|COURSE_SUBJECT_SHORT_NM|COURSE_TITLE_NM|CRS_ACADEMIC_DEPT_SHORT_NM|GRADE_NM|GRADE_POINTS_NBR|GRADE_SORT_NBR|GRADE_SUBTYPE_DESC|GRADE_TYPE_DESC|SEMESTER_YEAR|SEMESTER_NAME|SNAPSHOT_CODE|LOAD_DATE

>  edw_askoski_student_cohorts_hashed.txt 

#SEMESTER_YEAR_NAME_CONCAT|RETENTION_FLAG_AFTER_1_YEARS|RETENTION_FLAG_AFTER_2_YEARS|RETENTION_FLAG_AFTER_3_YEARS|RETENTION_FLAG_AFTER_4_YEARS|RETENTION_FLAG_AFTER_5_YEARS|RETENTION_FLAG_AFTER_6_YEARS|YEARS_TO_GRADUATION|PROBATION_FIRST_YR_FLAG|APPLICATION_ENTRY_TYPE|SEMESTER_YEAR|SEMESTER_NAME|LOAD_DATE|ANON_ID

1. edw_askoski_student_majors_hashed.txt

#SEMESTER_YEAR_NAME_CONCAT|STUDENT_COUNT|UNGRAD_GRAD_CODE|EXAM_UNITS_NO|ACADEMIC_DEPARTMENT_NAME|ACADEMIC_DIVISION_NAME|MAJOR_NAME|COLLEGE_NAME|SEMESTER_YEAR|SEMESTER_NAME|SNAPSHOT_CODE|LOAD_DATE|ANON_ID

2019-10-12-11-04
05_05PM-July-30-2019 --> 2019-07-30-17-05

---

## Data pipeline overview

1. 30,000 feet: Get EDW snapshots from university + pull course API info each semester --> feeds into models --> loaded by service --> displayed on FE.  
1. EDW Data dump (snapshots) 3 times a semester after every term into /research/UCBDATA
    - includes updated enrollment history, grades, majors, entry type, APR data
    - enrollment records used for C2V (expore feature) & RNN (requirements)
    - data pipeline --> models retrain --> restart service to get updated search file
    - search.pkl would not be here because that's only produced when models retrain pipeline is run. 
1. Raw EDW data --> run `refresh.py`, which generates the master lookup_dict & generates a timestamped directory in UCBD2/edw_data with
    - apr  classAPI  flat  hashed  logs  model  pickle
    - some flat files here are just copied over from timestamped directories like abbrev.tsv?
    - lookup tables + pickles & working files to run service sourced through `env.json` which is loaded through `scripts/refresh/refresh_env.py`) 
1. Runs Models-Askoski `retrain.sh` which create all lookup pickles for enrollments, requirements, offered classes, etc.
1. Run Models-AskOski `refresh.sh` which does... (removed)
1. Move all files outputted from Models into timestamped directory

*Where things live*

- Files: https://docs.google.com/spreadsheets/d/1wEH1HqMnRr3dg5l-ggrPHLZKDScZuL4pSqs4bkL1WeA/edit#gid=0
- `/home/askoski` --> where everything is launched from as the askoski user
- `/research/UCBDATA` --> where the snapshots are exported from campus
- `/research/UCBD2/edw_data` --> hashed / anonymized data & versioned snapshots of data
- `/research/askoski_common` --> contains misc items

*What Data-AskOski should be / should have*

> what UCBD2 used to be but with all its misc files cleaned & organized such that it only includes non-student data like classes information.  want to be able to rollback our data, have both ingested and collected data organized and versioned
    - non student data will live on github in data-askoski
    - what about hashed data?  Yes but gitignored
    - Ingested data = from data dumps, Collected data = from APIs
    - Collected data streams should also be incorporated in the data pipeline  
> what it actually is: timestamped directories

---

## env.sh

```
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
export mailgunKey="key-32232600888e04931773e38650963a0e"
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
```
