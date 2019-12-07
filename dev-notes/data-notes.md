## Questions

1. Clarify how the main lookup dict works
1. hashed vs encrypted data - which one is the anonymized using the lookup dict?  hashed? 
    - Encryption is a two-way function where information is scrambled in such a way that it can be unscrambled later.
    - "Hashing, one-way function where data is mapped to a fixed-length value. Hashing is primarily used for authentication. With a properly designed algorithm, there is no way to reverse the hashing process to reveal the original password."  So if there's a lookup dict that maps original sids to anons, is it really hashed?
    - Salting is an additional step during hashing, typically seen in association to hashed passwords, that adds an additional value to the end of the password that changes the hash value produced. This adds a layer of security to the hashing process, specifically against brute force attacks. A brute force attack is where a computer or botnet attempt every possible combination of letters and numbers and characters until the password is found.  They can also attempt to hash every possible combination of letters and numbers and characters (companies use well known hashing functions?) until your pw is found, don't even have to know the actual password.  Adding creates unique pw's and therefore unique hashes so if a hacker finds one, he doesn't find another.    

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

### Types of tasks / debugging

- Requirements - not displaying unmet requirement bubble interface for some students.  This would be dealing with the APR object?
- Explore re-training is broken - currently uses old research data
- Revisit open seats daily poll of classes api in thread
- Creating a new filter in AskOski that will filter a user's suggested courses based on whether their majors fall within the class reservations. This filter will be applied automatically to the already existing Open Seats filter. This task is a two-step process:
1)  Modify Data-AskOski to include reserve capacity information with each class, which involves querying the reserved seats API and augmenting the next_sem_dict to include reserve capacity data.
2)  Modify Service-AskOski to filter classes shown based on the reserve capacity data and the student's own majors. This involves creating a mapping between majors as represented in AskOski to the requirement groups in the API, and then creating a filter with it.

### Indexing error that broke the system for entirety of F19 during the data-askoski transition:

- Service reads from the hashed majors, grades, etc. files which are in the top level of /research/UCBD2/edw_data 

These are older files from the end of summer. It’s decoding the student ids with /research/askoski_common/bins/sidHash_new.bin, which is being overwritten by the data pipeline with mappings calculated from newer data. (are all these things being mapped?)

- Service using old grade, majors, requirements tables + new sid lookup table -> indexing errors
- A really quick fix would be to run the pipeline on old data, which would revert the lookup table and fix the indexing errors on Service.
- I am in the process of pointing the data pipeline to write the lookups to a separate folder that wouldn’t mess with the current Service.

The problem was a combination of a couple issues:

1. some of the file names for campus data dumps were incorrect. not sure who was responsible for this but we should verify file names next time when writing stuff like this.
2. we were loading the ENV json and then rewriting it to disk, but it wasn't being reloaded in memory. we should have sanity checks next time in between stages of the pipeline to check things like this, or better yet, separate out each stage of the pipeline entirely.
3. importing modules caused the ENV json in each one to load at the start meaning it was stale after new json was created. again we should be using sanity checks at each stage to verify that assumptions made in the code are actually true.

## SQL DB Transition instead of pandas

- service-askoski will definitely have to change because it's will no longer load pickle files but make SQL queries?  possibly models-askoski will change
- keep data askoski pipeline to process data but load exports into mySQL to be used in production

### Move all scripts and post-processed data out of UCBDATA & UCBD2
    - *Don't delete the encrypted files o/w you have to wait for the next data dump*
    - verify data is encrypted before moving out of UCBDATA - actually just keep here according to Zach
    - which are the files to not delete - don't delete the raw files

1. [x] archive files in UCBD2
1. [x] remove folders manually from UCBD2 - check if they can be deleted
    - pycache is just machine optimized code created every time python script is run, can be ignored - or deleted in this case
    - models-askoski is deprecated, nothing in git log
    - dev is empty
1. [x] change default srcDir path in models and add search model retrain
1. [x] Double save hash in UCBD2 & remove hashed data from UCBDATA in refresh.py 
    - Double check `rm -r` works from `os.system`
1. Double check that models retrain still runs on the hashed data in UCBD2/edw_data/hashed
1. PR note: double save anonymized data to UCBD2/edw_data and remove hashed data from UCBDATA


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


