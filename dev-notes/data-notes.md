Get an overview of the repo & pipeline.  Where does everything live, what comes directly from campus registrar and what comes from the APIs?  Then fill in knowledge gaps & reconcile all the moving parts to determine what the the next action item is.  Things are pretty organic, Zach doesn't exactly know what's going around here and you have free reign for what direction you want to pursue.  Still trying to figure out what you don't know.  You're willing to be the main point person for this pipeline so you're trying to absorb as much information so you can start working on actions items.

## Where things live

Files: https://docs.google.com/spreadsheets/d/1wEH1HqMnRr3dg5l-ggrPHLZKDScZuL4pSqs4bkL1WeA/edit#gid=0

/home/askoski --> where everything is launhced from as the askoski user
/research/UCBDATA --> where the snapshots are exported from campus
/research/UCBD2/edw_data --> hashed / anonymized data
/research/UCBD2 --> unknown misc items
/research/askoski_common --> contains misc items

## Current Data pipeline

1. Get EDW snapshots from university + pull course API info each semester --> feeds into models --> displayed on FE.  
1. EDW Data dump (snapshots) 3 times a semester, after every term
    - includes updated enrollment history, grades, majors, entry type, APR data
    - enrollment records used for C2V (expore feature) & RNN (requirements)
1. Ingested data = from data dumps, Collected data = from APIs
    - Collected data streams should also be incorporated in the data pipeline  
    - Ingested data piepline should be run 3x a semester and collected data should be run more frequently during enrollment periods

## What Data-AskOski should be

1. what UCBD2 used to be but with all its misc files cleaned & organized such that it only includes non-student data like classes information and hashed data? 
1. want to be able to rollback our data, have both ingested and collected data organized and versioned
1. What data comes from the APIs needs to be standardized
    - new semester courses, ...? 
    - currently outputted in Classes_2011_2018? 
    - different versions of Run's & Chris' APIs?  

## Current state of Data-AskOski

### what happens with a new data dump 

1. Raw EDW data --> hashing & preprocessing by refresh.py, which generates the master lookup_dict & dumps timestamped directory in UCB2/edw_data 
    - what is in this directory?
1. Generates more lookup tables + pickles & working files to run service
    - e.g. pathways in `env.json` updated 
1. Runs Models-Askoski `retrain.sh`

### what does debugging usually involve?

- biggest pain point is the lookup_dict (anon to SID) because if this is wrong then everything else is wrong in terms of the other lookup tables for majors / courses because then you pull from class API in service, among others things
    - Clarify how this lookup works

### Just so everyone is clear on what’s causing the indexing errors:

- Service reads from the hashed majors, grades, etc. files which are in the top level of /research/UCBD2/edw_data (through env.json which is loaded through `scripts/refresh/global_vars.py`) 

These are older files from the end of summer. It’s decoding the student ids with /research/askoski_common/bins/sidHash_new.bin, which is being overwritten by the data pipeline with mappings calculated from newer data. (are all these things being mapped?)

- Service using old grade, majors, requirements tables + new sid lookup table -> indexing errors
- A really quick fix would be to run the pipeline on old data, which would revert the lookup table and fix the indexing errors on Service.
- I am in the process of pointing the data pipeline to write the lookups to a separate folder that wouldn’t mess with the current Service.

The problem was a combination of a couple issues:

1. some of the file names for campus data dumps were incorrect. not sure who was responsible for this but we should verify file names next time when writing stuff like this.
2. we were loading the ENV json and then rewriting it to disk, but it wasn't being reloaded in memory. we should have sanity checks next time in between stages of the pipeline to check things like this, or better yet, separate out each stage of the pipeline entirely.
3. importing modules caused the ENV json in each one to load at the start meaning it was stale after new json was created. again we should be using sanity checks at each stage to verify that assumptions made in the code are actually true.

### Future tasks

- Explore re-training is broken - currently uses old research data
- Create a system level cron job that monitors data pipeline for new edw files and initiates the pipeline.
- Revisit open seats daily poll of classes api in thread
- Course API - keep credit restriction and prerequisite course information when querying Course API - save to two tsvs and make available to researchers via data repo (zach wants to incorporate the API scripts into the pipeline)
- Saved hashed files to a directory called Hashed inside UCD2, as well as a timestamped directory within edw_data
- Update the models code to use pipeline Classes data instead of fixed Classes_2011_2018 data

### What does the semester changeover entail?