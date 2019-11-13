
# Data-AskOski

1. Overview of the repo & pipeline
1. Example responsibilities.  E.g. 
    - what happens with a new data dump 
    - what does the semester changeover entail?
    - what does debugging usually involve?
1. look into hashing data
1. look into UCBD2/edw_data
1. look at yuhong's debugging & lawrence's PR

30000 feet overview

1. raw files from data dump --> hashing & preprocessing 
1. Then refresh.py generates the master lookup_dict & dumps timestamped directory in UCB2/edw_data 
1. Generates more lookup tables + pickles & working files to run service
    - e.g. pathways in `env.json` updated & 
1. Runs Models-Askoski `retrain.sh`

- biggest pain point is the lookup_dict (anon to SID) because if this is wrong then everything else is wrong in terms of the other lookup tables for majors / coursses because then you pull from class API in service, among others things