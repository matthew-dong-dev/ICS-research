Fill in knowledge gaps, reconcile all these moving parts, what's the next action item? 

# What Data-Askoski should be

1. what UCBD2 used to be but with all its misc files  cleaned & organized such that it only includes non-student data like classes information and hashed data? 
1. want to be able to rollback our data, have both ingested and collected data organized and versioned
1. Collected data = from APIs, Ingested data = from data dumps
    - Collected data streams should also be incorporated in the data pipeline and 
    - Ingested data piepline should be run 3x a semester and collected data should be run more frequently during enrollment periods

# Current Data pipeline

1. Data dump (snapshots) 3 times a semester, after every term
    - includes updated enrollment history, grades, majors, entry type, APR data
    - enrollment records used for C2V (expore feature) & RNN (requirements)
1. What data comes from the APIs?  this needs to be standardized
    - new semester courses, ...? 
    - currently outputted in Classes_2011_2018? 
    - different versions of Run's & Chris' APIs?  

## Relevant directories

/home/askoski/ --> where everything is launhced from as the askoski user
/research/UCBDATA --> where the snapshots are located
/research/UCBD2 --> hashed / anonymized data
/research/askoski_common/ --> contains misc items
/research/askoski --> deleted

# Data-AskOski

1. Overview of the repo & pipeline
1. Example responsibilities.  E.g. 
    - what happens with a new data dump 
    - what does the semester changeover entail?
    - what does debugging usually involve?
1. look into hashing data
1. look at yuhong's debugging regarding look into course_lookup that's causing the indexing errors
1. look at lawrence's PR

30000 feet overview

1. raw files from data dump --> hashing & preprocessing 
1. Then refresh.py generates the master lookup_dict & dumps timestamped directory in UCB2/edw_data 
1. Generates more lookup tables + pickles & working files to run service
    - e.g. pathways in `env.json` updated & 
1. Runs Models-Askoski `retrain.sh`

- biggest pain point is the lookup_dict (anon to SID) because if this is wrong then everything else is wrong in terms of the other lookup tables for majors / coursses because then you pull from class API in service, among others things