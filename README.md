# SEARCH MACHINE LEARNING

What are the keywords:

- What makes this search “intelligent” is that a query will not only be matched against course titles and descriptions, but also to an additional search metric known as “inferred keywords.” Inferred keywords are a generalized course description produced through machine learning that potentially capture a semantic portrayal of courses beyond surface level descriptions.  
- produced from an embedded space of courses learned through historic enrollments, gaining a semantic portrayal of courses capturing details beyond surface level course descriptions. 

Why keywords?

- Access to enrollment data is what distingiushes it from other information systems
- obtain a level of abstraction beyond pure keyword match
- use case is not knowing what the user would search to look up a specific course, possibly translate discipline specific jargon (e.g. course about money but has money nowhere in the dsescription)

Where do the keywords come from?

ANALOGY: 
- courses that are similar e.g. from the same department would be clustered together and have similar descriptions 
- if a course was interdisciplinary, then it might have predicted words that reflect the two departments depending on the enrollment behaviors of the students 

- Basic response: Model takes historic enrollments and course descriptions and infers what each course is about based on that information
- Intermediate: Model takes in behaviorally informed course vectors and produces keywords that can be used as another search metric.  Inferred keywords are a ML model's guess as to what the essence of a course is in terms of the collective descriptions.  Hopefully captures semantic meaning not explicitly found in the course descriptions through the course vectors which capture behavioral data through enrollment networks. 
- Advanced: Keywords are a mapping from behaviorally informed course vector space to literal description BOW vector space. Fit a multinomial logistic regression model from each course vector to its description vector (BOW) and then for each course tell it to predict the top k words that describe it. The model is regularized to prevent overfitting, allowing it to pull words from other course descriptions in its attempt to generalize. 
- tooltip v1: Keywords are produced through topic modeling of a course and offer both abstract and specific characterizations. 
- tooltip v2: Keywords are inferred using historic enrollment data and course descriptions. 
- tooltip v3: Inferred keywords are predicted from course descriptions and student enrollment patterns.  Words may characterize a course beyond the course description
- Disclaimer: May be inaccurate / not representative of the actual course or are not sponsored by faculty... 

How to make recommendations?

- similar course sequences "courses students similar to you have taken"
- enrolling in a course is considered implicit feedback

## ML: Improving the intelligence of the intelligent search
1. `Tune the model`:
	- remark: choose bias levels that augment course description & title
	- regression: try adding Dense layer with different activation function? 

1. BOW space
	- After fitting the multinomial regression model and predicting the keywords for each course, where does the randomness appear? It is not unique up to ordering, there are new words sometimes
	
1. `Improve the data`:
	- train improved models with class descriptions (over course descriptions)
	- class description different for each semester, year

1. inputs
	- *higher tf-bias = more specific, lower tf-bias = more general*
	- *equivalencies use tf-idf, while analogies use zero/one representation*
	- look at paper again for the difference between equivalency & analogy vectors; what is the validation set used for analogy vecs? 
	- what is the loss function and where is the train/test split

1. ask Jenny / Zach for explanations of course vectors
	- what would be a good analogy? 
	- courses that are similar e.g. from the same department would be clustered together and have similar descriptions
	- if a course was cross disciplinary, then it might have predicted words that mirror the two departmenst 
	- if a word `vertebrate` shows up for happiness advantage, can I say this implies more bio majors have take the course...? 
	- relevant words are from courses that are related; weird words are from course descriptions that are not related 

1. how can we have word predictions on courses that don't have descriptions? 
	- keywords produced from regressing vectors on BOW space, which uses the entire description corpus as a dictionary
	- L&S 124 description is incorrect?? http://guide.berkeley.edu/courses/l_s/ 
		- it's the course not class description

1. Course results could be shown that neither match to the keywords nor the description if the query was cosine similar to words in the description or keywords as determined by a google pre-trained word vector model. 
	- **Since the relationships between words expressed in news articles are not necessarily specialized to a domain (as per Mansi), we could fine-tune the embedding by using the google vector values as starting values for the weights, and iterating the fit to the course description corpus.**

1. _Validation ideas_
	- Potential outcome to track (as per Alessandra) would be if a student eventually enrolled in a course found via model keyword matching (since this would mean the student likely did some additional vetting of the relevance of the course and found that it was in fact relvant to their interests, expressed by their query)

1. https://github.com/CAHLR/semantic_model

--- 

## SANDBOX

COMMAND TO RUN SCRIPT: `time bash batch_training.sh -b 2 -v ../input_data/analogy_vecs.tsv`

1. If encounter `ResourceExhaustedError` run gpu_who and kill your existing jobs

1. `screen`
	- run `screen -S name` 
	- run the script / start up the backend / open jupyter notebook
	- When you use screen you need to detach with `CTRL+A+D` before you exit ssh.
	Misc:
		- `screen -r` will resume the current screen or return a list to resume
		- `screen -xS name-to-resume` 
		- `screen -ls` will list all current screens (ls = list)
		- `screen -d` will detach you from the screen and back into original session
		- screen must be detached for you to go back into original terminal session
		- run `echo $STY` to check if you are in a screen which is a variable set by the screen command
		- `control + d` just terminates screen
	- `lsof -i :1371`, `kill PID` if necessary


1. To transfer between servers: `ssh -A -t user1@remote1 scp srcpath user2@remote2:destpath` 
	- `ssh -A -t matthew@askoski.berkeley.edu scp /home/matthew/data/course_shortname_title.pkl matthew@cahl.berkeley.edu:~/askoski/data`

	- `ssh -A -t matthew@cahl.berkeley.edu scp /home/matthew/askoski/data/course_subject_long_to_short.csv matthew@askoski.berkeley.edu:/home/matthew/data`
1. ssh matthew@askoski.berkeley.edu
1. jupyter notebook --ip 169.229.192.179 --port 1332
1. http://maxwell.ischool.berkeley.edu:1332/ 

	```
	[optional] jupyter notebook --generate-config
	[optional] jupyter notebook password
	screen
	jupyter notebook --ip maxwell.ischool.berkeley.edu --port 1332
	(replace X with an integer)
	(then navigate your web browser to: http://maxwell.ischool.berkeley.edu:1332)
	(you can now close the terminal session, screen will keep jupyter running) 
	```

1. jupyter notebook --certfile=/etc/jupn-cert.pem --keyfile /etc/jupn-key.key --ip cahl.berkeley.edu --port 1338 
1. https://cahl.berkeley.edu:1338/
	- issue with server persistently running, port is always open: https://stackoverflow.com/questions/38511673/cannot-quit-jupyter-notebook-server-running 
	- what does screen do? https://www.rackaid.com/blog/linux-screen-tutorial-and-how-to/ 
1. don't fork repos

	```
	with open(pickled_path, 'rb') as f:
    	vectors = pickle.load(f)
    # equivalent to: 
	my_file = open("example.txt", "r")
	text = my_file.read() # my_file = pickle.load()? 
	my_file.close()
    ```

--------------------------------------------------

# SEARCH WEB DEVELOPMENT

## Remark: Why the autograder was useful
- **Pseudo-coding**:changing random things and hoping they'll work 
- Pseudo-coding will give you headaches later when debugging you must be systematic in your approach, diagramming things out by hand will give you a clearer pictures of where things might be going wrong
- sometimes slow internet connection is good - don't be in such a rush to test things, make sure everything is implemented as close to correctly as possible first 

---

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
1. Elucidate instructions:
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

## Next Steps: WebDev

1. tests for **3 cases: live search, filter search, live search with filters**
	- [ ] same queries in different order should return same results in same order? 
	- live search
		- [x] user types "asdf", then deletes "asdf", assert display default courses
		- [x] type in biology, -plant, -computational and assert after each subsequent term that the proper courses are included / excluded 
		- [x] after deleting the search expression, assert default courses displayed
	- filter search:
		- [x] add linear algebra (1st term), assert valid subset of courses
		- [x] add probability (2nd term), assert valid subset of courses
		- [x] add data science (3rd term), assert valid subset of courses
		- [x] delete one at a time, assert same subset of courses
		- [ ] **delete one at a time, assert subset of courses in same order**
		- [x] delete all 3, check that default courses appear
		- [ ] delete probability last, should course results be same order as inputting probability first? 
		- [x] delete probability last, assert that relevant courses appear
		- [x] add linear algebra, probability, and exclude compsci using `exclude` button
		- [x] click clear all button assert default courses displayed
	- live search with filters
		- [x] add 1st term linear algebra (astronomy), assert valid subset of courses 
		- [x] start adding 2nd term, then delete the term and check the filter defaults back to 1st term courses
		- [ ] add 2nd term: probability (cosmology), assert valid subset of courses THAT DOES NOT CHANGE ORDER when adding the filter after live search
		- [x] add 3rd term: data science (physics), assert valid subset of courses
		THAT DOES NOT CHANGE ORDER when adding the filter after live search
		- [x] assert that all relevant queries are highlighted
		- [x] add linear algebra, probability, and exclude compsci using **live search** 
		- [ ] edge case where removing term x will still have x highlighted until you continue searching 
	- highlighting
		- [x] add psychology, experiment; assert readMore component doesn't default back to initial snippet
	-live search to filter search
		- [x] assert adding psychology, experiment in one shot returns a proper subset of courses
		- [x] assert after adding "research" via live search works
		- [x] assert after adding "experiment" via filter search proper subset is returned
		- [ ] assert adding multiple terms a second time in one shot works

--- 

## SANDBOX

1. CalCentral Test Account
	- username: test-300934
	- password: f1$hNch1p$

Versioning number is arbitrary but good guidelines: [major release].[minor release].[hotfix]

**How to use devTools**
1. Network tab:
	- hit preserve log to record the time it takes for processes to work
1. Can use as IDE in sources tab 
	- access component properties in the console using `this`
	- establish breakpoint using `debugger` command

How to get backend running:
1. From service folder: `source ../scripts/env.sh`
1. `python service.py -np`

Input 	      | Output
------		  | -------
string query  | list of courses + id

master = ground truth <- staging server (PORT = 13XX) <- dev one feature at a time

`ports_used` to check which ports are available
`gpu_who` to check gpu 

```# ports used by user
netstat -tlnpe | awk '{print $7 " " $4}' | sed s/:/\ /g | grep -E '0.0.0.0|169.229.192.179' | awk '{if ($3 >= 1300 && $3 <=1399 ) print $3" "$1;}'| sort | awk '{ print "id -u -n " $2}' | sh | sort | uniq -c | sort
```

stackblitzes:

- [Course table](https://stackblitz.com/edit/angular-course-filter-pipe-gm2vhu?file=src%2Fapp%2Fapp.component.html)
- [without pipes](https://stackblitz.com/edit/angular-course-filter-pipe-bszsae?file=src%2Fapp%2Fapp.component.ts) (yours)
- [without pipes](https://stackblitz.com/edit/angular-course-filter-pipe-vnjhq9) (monty)
- [using debounce](https://stackblitz.com/edit/angular-course-filter-pipe-jqok8a)

----

## Miscelleanous

PRESENTATION NOTES:

- Personalization vs Adaptivity: I'd say any system allowing for the user to express preference is a system that allows for personalization. What the systems on campus don't have is any adaptivity, where the system customizes some aspect of the experience based on inferences. 
- When showing the plot figure, it's customary to include some reference text below it, like (Pardos, Fang, & Jiang, under-review)
- I think the use of that figure was good for the purposes of your talk. Technically, however, the figure was generated from the embedding in an RNN, not a word2vec model. We have another paper where the depiction of courses was generated from word2vec, which you could use.

Technical vocab: 

- proof of concept, MVP, technical debt, ship to production, push for production, QA (quality assurance), bells & whistles, parity with master, ground truth, upkeep, contract
- flat file: A flat file database is a database that stores data in a plain text file. Each line of the text file holds one record, with fields separated by delimiters, such as commas or tabs. While it uses a simple structure, a flat file database cannot contain multiple tables like a relational database can.
- Code hygiene, maintenance, cleanliness, pruning
- upshot, value proposition, grok
- Priority 0 (P0)
- cost, quality, speed

How to describe CAHL
- a lot of data is generated from MOOCs (online courses) such as clickthrough rate, student participation, engagement... and using methodologies from other fields can you infer anything about student motivations, student engagement, and can you use your models to better personalize learning or improve a course experience... 
