# Data Pipeline

1. Point `PATH_TO_MODELS` in `refresh.py` to Models-AskOski directory with most recent changes.  Make sure both Data & Models are on the correct branch and most recent changes have been pulled.  
Export course, class, class section API credentials.
1. Run `refresh.py` in screen.
1. Copy over any modified files into Service dummy-data to verify Service runs locally.  
1. Copy generated `env.json` pointing to the most recent timestamped directory into Service before making PR. 
1. Sandbox testing environment 
    - Change output pathways? No just delete the timestamped output 
    - can you run pipeline parts in isolation?  Yes, just run the individual retrain scripts but should not do this during full run through even if RNN retraining is completed because all the models all need to write their outputs referencing the same timestamped directory 
1. `chmod -R 777` Data-AskOski & Models-AskOski if necessary
1. *Don't delete the encrypted UCBDATA files o/w you have to wait for the next data dump*

---

## Data-AskOski Deep dive

1. update master file spreadsheet
    - look into refresh.md & env.sh & inputs.md - these files are outdated, but tells a lot about how things work
    - clean ucbd2-archive & update spreadsheet, check what each file does and where it already exists in the system before deleting
        - start with hashed-archive
        - edw_askoski_apr_supplementary_course_lists --> exists inside APR folder of timestamped directory
        - edw_2018.tsv --> hashed grades old file
        - data.dict --> meta data
1. look at imported functions in refresh.py - what is refresh user, enrollments, grade_info, etc... doing
1. incorporate Zihao's updated dictionaries and RNN model (found in /research/UCBD2) into staging. His RNN model weights are in a binary file called "askoski", the topology of the model is in "askoski.json" and "askoski.desc" just describes the hyper parameters that were used. The dictionary file "course2idx.json" can be used to translate between "Subject CourseNum" and the one-hot index for the model and "major2idx.json" can be used to translate the major to major one-hot index. Jenny's word2vec model is called "w2v_300_15_20_3.model" and uses the same indices as course2idx.

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

How the pipeline should work in your head

1. generate class & course API data
1. Retrain models

How does RNN already have course data?  from the data dumps... This is what Data-AskOski refresh_classes_from_api.py and Model's add_new_courses.sh is building on. So really it's: 

1. train RNN --> get course2idx
1. add_new_courses.sh = augment model and course2idx from pulled class & course API data
1. refresh_classes_from_api.py should be augment classes with CCN data. There is model's class_api.py - do we ever use its output class_info.tsv?   We should replace this script with the data scripts

1. Why do we need next_sem_classes, it seems to have the same information as next_sem_dict + idx2course? 


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