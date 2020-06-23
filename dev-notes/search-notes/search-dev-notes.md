# SEARCH MACHINE LEARNING

Overview:

- What makes this search “intelligent” is that a query will not only be matched against course titles and descriptions, but also to an additional search metric known as “inferred keywords.” Inferred keywords are a generalized course description produced through machine learning that potentially capture a semantic portrayal of courses beyond surface level descriptions.

Why keywords?

- Access to enrollment data is what distinguishes AskOski system from other information systems, allowing us to obtain a level of abstraction beyond pure course description match.  
- use case is not knowing what the user would search to look up a specific course, possibly translate discipline specific jargon (e.g. course about money but has money nowhere in the description).  Hopefully captures course topics not explicitly found in the course descriptions. 
- Personalization vs Adaptivity: I'd say any system allowing for the user to express preference is a system that allows for personalization. What the systems on campus don't have is any adaptivity, where the system customizes some aspect of the experience based on inferences. 

Where do the keywords come from?

ANALOGY: 

- You can determine a person's characteristic by the company he keeps, similarly you can say things about a course based on the "company" or context its found in.  Course2vec captures these similar courses and the translation model can generalize to find words that describe the course from neighboring course descriptions.  
- courses that are similar e.g. from the same department would be clustered together and have similar descriptions 
- if a course was interdisciplinary, then it might have predicted words that reflect the two departments depending on the enrollment behaviors of the students 
- There's a relationship between courses and descriptions and we're trying to determine what a class is about as determined by student behavior and that's what we're trying to surface with the inferred keywords.  

- Basic response: Inferred keywords are predicted from course descriptions and student enrollment patterns.  Model uses historic enrollment data and course descriptions to predicts what each course is about in terms of the collective descriptions.   Words may characterize a course beyond the course description.  

- Advanced: Keywords are a mapping from behaviorally informed course vector space to literal description BOW vector space. Mapping from course space to description space, where the course embedding are learned through enrollment sequences.  Fit a multinomial logistic regression model from each course vector to its description vector (BOW) and then for each course tell it to predict a probability distribution over the entire vocab and take the top 10. The model is regularized to prevent overfitting, allowing it to pull words from other course descriptions in its attempt to generalize. 


## ML: Improving the intelligence of the intelligent search

1. Remark: You should not be changing two parameters in your experiment at a time, because then you've introduced a confounding factor and you don't know how they interact with each other, and even if they are independent, you don't know which to attribute as the causal factor for the change

1. EDM observation: humanity majors have less formal ordering imposed in its major couse planning so this may influence the quality of keywords associated with STEM vs humanities courses

1. `Tune the model`:
	- remark: choose bias levels that augment course description & title
	- regression: try adding Dense layer with different activation function? 
	- After fitting the multinomial regression model and predicting the keywords for each course, where does the randomness appear? It is not unique up to ordering, there are new words sometimes
	- due to random initialization of weights when finding optimal coefficients for model 
	- https://github.com/CAHLR/semantic_model

> Improve the data
	
1. Course description BOW space
	- train improved models with class descriptions (over course descriptions)
	- class description different for each semester, year

1. Course embedding vector space
	- *higher tf-bias = more specific, lower tf-bias = more general*
	- *equivalencies use tf-idf, while analogies use zero/one representation*
	- look at paper again for the difference between equivalency & analogy vectors; what is the validation set used for analogy vecs? 
	- what is the loss function and where is the train/test split

1. ask Jenny / Zach for explanations of course vectors
	- what would be a good analogy? 
	- adding a course from econ dpt + course from environmental science should return an env econ course
	- courses that are similar e.g. from the same department would be clustered together and have similar descriptions

1. how can we have word predictions on courses that don't have descriptions? 
	- keywords produced from regressing vectors on BOW space, which uses the entire description corpus as a dictionary
	- L&S 124 description is incorrect?? http://guide.berkeley.edu/courses/l_s/ 
		- it's the course not class description

1. Course results could be shown that neither match to the keywords nor the description if the query was cosine similar to words in the description or keywords as determined by a google pre-trained word vector model. 
	- **Since the relationships between words expressed in news articles are not necessarily specialized to a domain (as per Mansi), we could fine-tune the embedding by using the google vector values as starting values for the weights, and iterating the fit to the course description corpus.**


--- 

# SEARCH WEB DEVELOPMENT

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
