# how to run pipeline

1. `chmod -R 777` Data-AskOski & Models-AskOski if necessary - what is this command doing? 
1. Run `refresh.py` in screen 
1. how long does entire retraining take? 
    - Hashing - 5mins 
    - Models retraining - currently like 10 hours 
    - refresh api - 1 hour ish
1. Verify pipeline has successfully by copying env.json to service and results are as expected `cp /home/matthew/Data-AskOski/env.json /home/matthew/Service-AskOski/service`
1. Currently fixed / hardcoded folders needed for pipeline to run
    - `hashed`, `encypted`, `decrypted` folders in UCBDATA
    - `classAPI` in UCBD2
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
    - how to test individual parts of the pipeline? Just run the individual scripts 

---

## [Data-Pipeline] Deep dive

1. look into refresh.md & env.sh - these files are outdated, but tells a lot about how things work
1. look at imported functions in refresh.py - what is refresh user, enrollments, grade_info, etc... doing
1. biggest pain point is the lookup_dict (anon to SID) because if this is wrong then everything else is wrong in terms of the other lookup tables for majors / courses.  how does the main sid to anon lookup work and how does that affect the course indexing?  
    - look at the indexing error action item in data-action-items.md
1. hashed vs encrypted data - which one is the anonymized using the lookup dict?  hashed?  Yes
    - Encryption is a two-way function where information is scrambled in such a way that it can be unscrambled later.
    - "Hashing, one-way function where data is mapped to a fixed-length value. Hashing is primarily used for authentication. With a properly designed algorithm, there is no way to reverse the hashing process to reveal the original password."  So if there's a lookup dict that maps original sids to anons, is it really hashed?
    - Salting is an additional step during hashing, typically seen in association to hashed passwords, that adds an additional value to the end of the password that changes the hash value produced. This adds a layer of security to the hashing process, specifically against brute force attacks. A brute force attack is where a computer or botnet attempt every possible combination of letters and numbers and characters until the password is found.  They can also attempt to hash every possible combination of letters and numbers and characters (companies use well known hashing functions?) until your pw is found, don't even have to know the actual password.  Adding salt creates unique pw's and therefore unique hashes so if a hacker finds one, he doesn't find another.    
    - how does it work? "The lookup table will be stored in /research/UCBD2/edw_data/TIMESTAMP"
    - what is sidHashBin file?  what are .bin files?
    - what is sid_to_hash.txt? (is this the actual lookup file?)  the file is being removed in utils.py

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
1. Run Models-AskOski `refresh.sh` which does...
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
