Get an overview of the repo & pipeline.  Where does everything live, what comes directly from campus registrar and what comes from the APIs?  Then fill in knowledge gaps & reconcile all the moving parts to determine what the the next action item is. 

## Where things live

Files: https://docs.google.com/spreadsheets/d/1wEH1HqMnRr3dg5l-ggrPHLZKDScZuL4pSqs4bkL1WeA/edit#gid=0

/home/askoski/ --> where everything is launhced from as the askoski user
/research/UCBDATA --> where the snapshots are located
/research/UCBD2 --> hashed / anonymized data
/research/askoski_common/ --> contains misc items

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

1. Raw EDW data --> hashing & preprocessing 
1. Then refresh.py generates the master lookup_dict & dumps timestamped directory in UCB2/edw_data 
1. Generates more lookup tables + pickles & working files to run service
    - e.g. pathways in `env.json` updated & 
1. Runs Models-Askoski `retrain.sh`

### what does debugging usually involve?

- biggest pain point is the lookup_dict (anon to SID) because if this is wrong then everything else is wrong in terms of the other lookup tables for majors / coursses because then you pull from class API in service, among others things

### What does the semester changeover entail?