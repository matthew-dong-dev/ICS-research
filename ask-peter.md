## High level guidelines

1. Do the UCI people want their own UI or just our ML algo predictions like access to an API?  
1. If they want a UI, have the UCI contacts seen the universal search mockups?
1. are we definitely moving ahead with the universal search approach for askoski?
    - how do we distinguish / order requirements, explore, search results?
1. is the UCI variables spreadsheet still valid?
1. explore feature - just BOW predictions?
1. search feature - 

## Low level implementation

1. What would be the appropriate abstraction level for school?  UCI would have its own pipeline (using our algorithms), separate FE & BE repo?  But right now we don't have to worry about the pipeline or models - just FE / BE
    - definitely need a separate BE repo with its own endpoints.  still use Flask?
    - SQL DB - touch base w/ Jeff 
    - we can just have a separate branch for the FE for now.  how to customize FE theme / colors for each institution - touch base w/ Sher

---

Don't bootstrap things together, take time to focus on getting the architecture right, from data pipeline down to clean code (lack of abstraction, nested logic, duplicate logic, naming convention, there's a lot of tech debt in the askoski system that slows development down the line because we have to go back and refactor code or update the tools we use.  There's no master course file bc each feature was built independently, we're 20% in mysql DB and 80% in flat files 

Internal workflow - if you're going to do this you should do it right

- what data storage system are you going to use?  how to theme different institutions?  
   - you should use table relationships where you have course level data (title, id, description, credit restrictions etc.) and then department level data (majors, abbreviations)
- separate FE/BE branches? 
- customize the FE for each institution