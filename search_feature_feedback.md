## Beta Tests / Trial Runs Feedback

Script:

- introduce system if not already familiar
- when you want to find a course what search resources do you usually use? and in what context? (to look up course info or to discover new courses) 
- askoski is for course discovery but do not mention
- this test run is to determine how to make it more user friendly?  share what do you expect to happen and does it meet those expectations? 
- literally just monologue as you use the feature and I'll be taking notes
- ask any questions
- how would you prefer to see the feature integrated into the current system?
- @end: top 3 things that you liked, top 3 things would like improvements

General feeling from trial runs:

1. Current form is only a minimal viable product, the foundation is there but there is a lack of functionality 
1. question whether or not to put into production yet 
1. Pros over Berkeley guide is cleaner & more user friendly
1. Cons: See recurring requests

Recurring requests:
1. **filter for lower / upper div / graduate courses**
1. UPDATE TO MOST RECENT COURSES
	- with option to filter by available this semester? 
1. not sure what info keywords provide

Oscar
1. usually use: berkeley guide (major reqs), ninja courses (course reviews), cal central course catalog (enrollment), schedule planner (visualize schedule & enrollment details like how many enrolled), berkeley time (enrollment history & options to filter)
1. Clarify instructions:
	- change header to say: add `MULTIPLE` topics
	- heads up: for search UI "Exclude them by using a dash (e.g. history, -art, -american)" the history is missing dash
	- make it clear that only searches on keywords instead of phrases (matches based on string match)
1. Change tooltip info again 
1. query examples:
	- probability should return **stat** courses first?  
	- `61b` should return cs61B first
	- `social justice` + `china` vs `chinese social justice`
	- `pandas`, `ml`
	- `machine learning` does not show IEOR 142
1. **add courses to favorites** 
1. make more obvious the terms is excluded instead of only using dash 
1. personalized search vs similar to course catalog? 
	- benefits to both

Zachary
1. usually use: berkeley guide (mainly to check enrollment info)
1. [x] change `add term` to `add subject`
1. [x] make it obvious it's keyword search based on content of course (why different vs course catalog)
	- not obvious that keywords user types in are matches on course description and title
	- more explicit examples & directions in the header
1. [x] change tooltip description (see top)
1. not obvious what the shortened course subjects are
1. click course title should go to new page (link to CCN)
	- expect professors to show up
	- expect fall 2018 courses
1. word stemming: e.g. seminars should exclude seminar 
1. course catalog: option to search and then filter by breadths
	- get recommendations and then search? 
	- does not make sense to personalize search
1. the data table does not return to first page! 
1. power user: have && and || operators
