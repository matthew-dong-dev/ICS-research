
# Service RNN Refactor

This seems like a huge task, but just fucking grind through it even though so much of it is a blackbox like wtf are they working with tensors for?  One thing at a time e.g. don't bother with the RNN preprocess obj/class yet.  First just focus on refactoring build_matrix_from_dict, and before that just figure out what each part of the code is doing.  **WORK ITERATIVELY**

## To do 

1. [x] figure out what info the FE is sending to the BE 
1. [x] figure out how the BE is turning that into predictions, rn the RNN is a blackbox, as well as the /nextcourse/predict endpoint
WHERE IS THE STUDENT ENROLLMENT HISTORY BEING OBTAINED? 
1. [x] comment what each portion of the code is doing / identify the helper functions being called to help figure out what the purpose of that code is
1. [x] focus first on breaking down build_matrix_from_dict into smaller functions --> Add documentation and improve method names
1. [x] start by factoring out a get_student_dict function
1. [x] refactor parts of code so there exists a 1-1 correspondence between a method and a lstm input e.g. a get_eval_input, get_eval_major, get_entry_list method
1. [x] continue by adding documentation to the functions, which'll help you figure out what the critical portions of the code is doing
1. [x] move relevant shit to a RNN_preprocess.py file 
1. [] refactor `get_student_enrollment_data`?  look at `lookup_dict`
    - "lookup_dict: This is the mapping between SID and anonID, which allows use to grab anonymized info for that student. This is faked in --no-pass mode, see No Pass Mode wiki page."
    - `anon = lookup_dict[sid]`
    - anon is the Internal Faked CalNet ID
    - where is dummy_lookup_dict being used?
1. add test coverage?  look at testing pipeline
1. end goal is creating separate build_matrix_from_dict class, pass in arguments during instantiation like APR obj.
1. consistently pull from master
1. update README

If I have a few quick questions about the RNN preprocessing, are you the person to set up a meeting with or someone else?  

### Notes / questions

1. disable debugger before pushing
1. Who to touch base with for following questions: 
    1. can you rename all the eval and x_eval variables or is that some sort of deep learning model convention?
        - renaming eval_input to eval_courses
    1. What is BOS
    1. what is myCourses?  caching student data that's already been loaded? 
    1. does the fact we're only using course history, major, and entry type as lstm input mean those are the only features in our model?
1. Ask Jeff to verify that this shit works in production mode (vs no-pass) also plan still works as expected

## RNN BE  

- try dumping things to the *server terminal* by printing things from your predict endpoint after being called after logging in from the FE and being redirected to the /suggestions URL 
- need a better debugging strategy to visualizing what each variable represents that isn't dumping to the terminal window   - use Flask debugger + Postman.  Postman to send requests a lot easier than loading the FE and if there's an error after sending a request you can read the traceback from the Debugger using raw form in Postman , just won't be able to use the console

> /nextcourse/predict

- receives a request form from the FE... and passes it into build_matrix_from_dict which is doing what exactly?  
- notice changing the SID changes the recommendations...so the data lookup has something to do with the SID
- trying to get a feel for what the inputs to the lstm model are aka the outputs of BMFD - you're trying to dump it in postman but flask won't send numpy arrays

The first part of BMFD is to obtain a student_dict which looks like  `OrderedDict([(20163, [164, 7358, 901, 2331]), (20171, [542, 664, 569, 590]), (20173, [1550, 2736, 6, 594]), (20181, [4072, 760, 543])])`

where the key is the year_semester and the list is the course_ids which we can verify in `anon_id2sems` -->  `"999985": "2016 Fall|2016 Fall|2016 Fall|2016 Fall|2017 Spring|2017 Spring|2017 Spring|2017 Spring|2017 Fall|2017 Fall|2017 Fall|2017 Fall|2018 Spring|2018 Spring|2018 Spring",` and `anon_id2enroll` --> `"164|7358|901|2331|542|664|569|590|1550|2736|6|594|4072|760|543"`

Then the student_dict is unraveled to look like `"x_eval_list": [ [ 164, 7358, 901, 2331 ], [ 542, 664, 569, 590 ], [ 1550, 2736, 6, 594 ], [ 4072, 760, 543 ] ]` and  `"x_eval_semester": [ [ 20163, 20163, 20163, 20163 ], [ 20171, 20171, 20171, 20171 ], [ 20173, 20173, 20173, 20173 ], [ 20181, 20181, 20181 ] ]`

build_matrix_from_dict returns 5 things (*eval_input*, *eval_major*, x_eval_list, x_eval_semester_list, *entry_list*) but only 3 get used as input (`lstm_model.predict([eval_input, eval_major, entry_list]`) 

understand these three, these are the ones that are numpy arrays / matrices and therefore you're having a hard time visualizing in flask 

x_eval_matrix shape is np.zeros((1, MAX_SEM + 1, MAX_COURSE)) = (1, 13, 15)

**printing eval_input from preprocess:  (1, 13, 9324)
**printing eval_major from preprocess:  (1, 13, 268)


### RNN FE Model 

- try dumping things to the *browser console* see what's being returned at each step

In ngOnInit() in recs component first calls: 
```
this.lookupTables.getId2Sub(),
this.flaskService.getStudentData() // THIS ONLY HAS TO DO WITH MAJORS? 

``` 
then calls
component's `this.getRecs();` which calls `this.flaskService.getRecs(false)` 
which sends a post request to `nextcourse/predict`  via `this.http.post(url, body)` 

-  not sure how it gets the data it's setting in the body and 
- then reroutes the page to suggestions with some query params

the predict endpoint dumps:

```
{'status':status, 'result':return_list, 'current_year': currentYear, \
'guide_berkeley_0': guide0, 'guide_berkeley_1': guide2 , \
'CCN':CCN, 'Description':title}
```

Then in the FE we index over `result` and map it to its subject with `response.result[index] in this.courseToSub`

...
- `getStudentData()` calls `getLookupTables` which calls `getLookup` which references the `selects` dict from service.py?

