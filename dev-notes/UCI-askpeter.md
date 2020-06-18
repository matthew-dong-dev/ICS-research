## High level guidelines

1. Do the UCI people want their own UI or just our ML algo predictions e.g. an open API access?  
1. If they want a UI, have the UCI contacts seen the universal search mockups?
1. are we definitely moving ahead with the universal search approach for askoski?
    - how do we distinguish / rank requirements, explore, search results?
1. is the UCI variables spreadsheet still valid?
1. explore feature - just BOW predictions?
1. search feature - 

## Low level implementation

There's a lot of tech debt in the askoski system that slows development down the line because we have to go back and reconsider design / implementation choices so we should take more time in the beginning to put more thought into design decisions.

1. Internal workflow: What would be the appropriate abstraction level for a school?  UCI would have its own pipeline (Airflow DAG) using our ML algorithms, and separate FE & BE repo?  Right now just have to worry about FE / BE
    - Service - Separate BE with its own endpoints.  still use Flask?
    - Storage - SQL DB? touch base w/ Jeff.  
    - UI - We can probably just have a separate branch off askoski-anglular for the UCI FE for now.  how to customize FE theme / colors (sass) for each institution? touch base w/ Sher
1. Cleaner code
-  there should be a course representation that's well defined between all the features.  we should have at least a unique course id, a table for course information (id, subject, title, description, credits), a department level table (sbj, abbreviation, division), credit restriction table?, etc.
- decide on next steps...

---

If you're going to do this you should do it right.  Don't bootstrap things together, take time to focus on getting the architecture right, from data pipeline down to clean code there's a lot of tech debt in the askoski system that slows development down the line because we have to go back and refactor code or update the tools we use (like using mysql) 

#### Internal workflow

- what data storage system are you going to use? 
   - you should use table relationships where you have course level data (title, id, description, credit restrictions etc.) and then department level data (majors, abbreviations)
   - askoski = 20% in mysql DB and 80% in flat files 
- how to theme different institutions i.e. customize the FE for each school
- separate FE/BE branches or repos? 

#### Cleaner code 

- Lack of abstraction 
    - course obj / student obj? that's well defined between all the features i.e. There's no master course file / course representation bc each feature was built independently and gets data in their own ways and there's no naming convention consistency
    - duplicate logic in service i.e. Plan reuses a lot of code
- nested logic (API scripts)