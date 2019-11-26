## Where things live

Files: https://docs.google.com/spreadsheets/d/1wEH1HqMnRr3dg5l-ggrPHLZKDScZuL4pSqs4bkL1WeA/edit#gid=0

/home/askoski --> where everything is launched from as the askoski user
/research/UCBDATA --> where the snapshots are exported from campus
/research/UCBD2/edw_data --> hashed / anonymized data
/research/UCBD2 --> unknown misc items
/research/askoski_common --> contains misc items

## Data pipeline high level overview

1. Get EDW snapshots from university + pull course API info each semester --> feeds into models --> displayed on FE.  
1. EDW Data dump (snapshots) 3 times a semester, after every term
    - includes updated enrollment history, grades, majors, entry type, APR data
    - enrollment records used for C2V (expore feature) & RNN (requirements)
1. Ingested data = from data dumps, Collected data = from APIs
    - Collected data streams should also be incorporated in the data pipeline  
    - Ingested data pipeline should be run 3x a semester and collected data should be run more frequently during enrollment periods

## What Data-AskOski should be / should have

1. what UCBD2 used to be but with all its misc files cleaned & organized such that it only includes non-student data like classes information 
    - non student data will live on github in data-askoski
    - what about hashed data?  Yes
1. want to be able to rollback our data, have both ingested and collected data organized and versioned
1. What data comes from the APIs needs to be standardized
    - new semester courses, ...? 
    - currently outputted in Classes_2011_2018? 
    - different versions of Run's & Chris' APIs?  
1. Course API - keep credit restriction and prerequisite course information when querying Course API - save to two tsvs and make available to researchers via data repo (zach wants to incorporate the API scripts into the pipeline)
1. Update the models code to use pipeline Classes data instead of fixed Classes_2011_2018 data

## Current state of Data-AskOski

### what happens with a new data dump 

1. Raw EDW data --> hashing & preprocessing by `refresh.py`, which generates the master lookup_dict & generates a timestamped directory in UCB2/edw_data 
    - what are each of the individual dirs?: apr  classAPI  flat  hashed  logs  model  pickle
    - lookup tables + pickles & working files to run service sourced through `env.json` which is loaded through `scripts/refresh/global_vars.py`) 
    - some flat files here are just copied over like abrev.tsv
    - your search.pkl would not be here because that's only produced when models retrain pipeline is run. 
    - data pipeline --> models retrain --> restart service to get updated search file
1. Runs Models-Askoski `retrain.sh` - 

### what does debugging usually involve?

- biggest pain point is the lookup_dict (anon to SID) because if this is wrong then everything else is wrong in terms of the other lookup tables for majors / courses because then you pull from class API in service, among others things
    - Clarify how this lookup works
- how to get a sandbox testing environment - just clone the repo to your directory and change output pathways?
    - how to test individual parts of the pipeline?  create dummy repos w/ same name and then run that part of the pipeline

### Types of tasks / debugging

- Requirements - not displaying unmet requirement bubble interface for some students.  This would be dealing with the APR object?
- Explore re-training is broken - currently uses old research data
- Revisit open seats daily poll of classes api in thread
- What does the semester changeover entail?
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

### Move all scripts and post-processed data out of UCBDATA. This directory should be reserved exclusively for campus exports
    - Double save hash to UCBD2/ (top level or a separate directory called hashed) and timestamped directory
    - *Don't delete the encrypted file o/w you have to wait for the next data dump*


## SQL DB Transition instead of pandas

- service-askoski will definitely have to change because it's will no longer load pickle files but make SQL queries?  possibly models-askoski will change
- keep data askoski pipeline to process data but load exports into mySQL to be used in production
