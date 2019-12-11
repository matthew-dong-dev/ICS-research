# how to run pipeline

1. Replace /home/askoski/Models-AskOski with local version /home/matthew/Models-AskOski to test changes
1. chmod -R 777 Data-AskOski & Models-AskOski if necessary - what is this command doing? 
1. Run refresh.py in screen 
1. how long does entire retraining take? 
    - Hashing - 5mins 
    - Models retraining - currently like 10 hours 
    - refresh api - 1 hour ish
1. *Don't delete the encrypted files o/w you have to wait for the next data dump*
1. Verify pipeline has successfully by copying env.json to service and results are as expected

## [Data-Pipeline] Deep dive

1. look into refresh.md & env.sh - these files are outdated, but tells a lot about how things work
1. look at imported functions in refresh.py
1. how does the main sid to anon lookup work and how does that affect the course indexing?
1. get familiar with how to do a semester changeover
1.  What's the difference between Models API scripts and Data API scripts?  
    - dumped into pickle folders, etc..
    - refresh.sh is dumping outputs into timestamped `salt` - why? SAlt stands for serendipitous alternatives
1. hashed vs encrypted data - which one is the anonymized using the lookup dict?  hashed?  Yes
    - Encryption is a two-way function where information is scrambled in such a way that it can be unscrambled later.
    - "Hashing, one-way function where data is mapped to a fixed-length value. Hashing is primarily used for authentication. With a properly designed algorithm, there is no way to reverse the hashing process to reveal the original password."  So if there's a lookup dict that maps original sids to anons, is it really hashed?
    - Salting is an additional step during hashing, typically seen in association to hashed passwords, that adds an additional value to the end of the password that changes the hash value produced. This adds a layer of security to the hashing process, specifically against brute force attacks. A brute force attack is where a computer or botnet attempt every possible combination of letters and numbers and characters until the password is found.  They can also attempt to hash every possible combination of letters and numbers and characters (companies use well known hashing functions?) until your pw is found, don't even have to know the actual password.  Adding creates unique pw's and therefore unique hashes so if a hacker finds one, he doesn't find another.    

--- 

## Where things live

Files: https://docs.google.com/spreadsheets/d/1wEH1HqMnRr3dg5l-ggrPHLZKDScZuL4pSqs4bkL1WeA/edit#gid=0

/home/askoski --> where everything is launched from as the askoski user
/research/UCBDATA --> where the snapshots are exported from campus
/research/UCBD2/edw_data --> hashed / anonymized data
/research/UCBD2 --> unknown misc items
/research/askoski_common --> contains misc items

## Data pipeline high level overview

1. Get EDW snapshots from university + pull course API info each semester --> feeds into models --> displayed on FE.  
1. EDW Data dump (snapshots) 3 times a semester, after every term into /research/UCBDATA
    - includes updated enrollment history, grades, majors, entry type, APR data
    - enrollment records used for C2V (expore feature) & RNN (requirements)
1. Ingested data = from data dumps, Collected data = from APIs
    - Collected data streams should also be incorporated in the data pipeline  
    - Ingested data pipeline should be run 3x a semester and collected data should be run more frequently during enrollment periods

## What Data-AskOski should be / should have

1. what UCBD2 used to be but with all its misc files cleaned & organized such that it only includes non-student data like classes information 
    - non student data will live on github in data-askoski
    - what about hashed data?  Yes but gitignored?
1. want to be able to rollback our data, have both ingested and collected data organized and versioned
1. What data comes from the APIs needs to be standardized
    - new semester courses, ...? 
    - currently outputted in Classes_2011_2018? 
    - different versions of Run's & Chris' APIs?  
1. Course API - keep credit restriction and prerequisite course information when querying Course API - save to two tsvs and make available to researchers via data repo (zach wants to incorporate the API scripts into the pipeline)
1. Update the models code to use pipeline Classes data instead of Classes_2011_2018 data

---

## Current state of Data-AskOski

### what happens with a new data dump 

1. Raw EDW data --> hashing & preprocessing by `refresh.py`, which generates the master lookup_dict & generates a timestamped directory in UCB2/edw_data 
    - what are each of the individual dirs?: apr  classAPI  flat  hashed  logs  model  pickle
    - lookup tables + pickles & working files to run service sourced through `env.json` which is loaded through `scripts/refresh/global_vars.py`) 
    - some flat files here are just copied over like abbrev.tsv
    - your search.pkl would not be here because that's only produced when models retrain pipeline is run. 
    - data pipeline --> models retrain --> restart service to get updated search file
1. Runs Models-Askoski `retrain.sh`

### what does debugging usually involve?

- biggest pain point is the lookup_dict (anon to SID) because if this is wrong then everything else is wrong in terms of the other lookup tables for majors / courses because then you pull from class API in service, among others things
    - Clarify how this lookup works
- how to get a sandbox testing environment - just clone the repo to your directory and change output pathways?
    - how to test individual parts of the pipeline?  create dummy repos w/ same name and then run that part of the pipeline

---

## [Data] Deep dive

1. clean hashed-archive
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

edw_askoski_apr_supplementary_course_lists --> exists inside APR folder of timestamped directory
edw_2018.tsv --> hashed grades old file
data.dict --> meta data