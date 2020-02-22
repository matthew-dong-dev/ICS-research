# START FROM TRELLO AND PUT THEM HERE ONCE YOU NEED TO EXPAND

## Action Item backlog

1. get familiar with how to do a semester changeover
1. update master file spreadsheet
    - look into refresh.md & env.sh & inputs.md - these files are outdated, but tells a lot about how things work
    -  RNN model weights are in a binary file called "askoski", the topology of the model is in "askoski.json" and "askoski.desc" just describes the hyper parameters that were used. The dictionary file "course2idx.json" can be used to translate between "Subject CourseNum" and the one-hot index for the model and "major2idx.json" can be used to translate the major to major one-hot index. Jenny's word2vec model is called "w2v_300_15_20_3.model" and uses the same indices as course2idx
    - clean ucbd2-archive & update spreadsheet, check what each file does and where it already exists in the system before deleting
        - start with hashed-archive
        - edw_askoski_apr_supplementary_course_lists --> exists inside APR folder of timestamped directory
        - edw_2018.tsv --> hashed grades old file
        - data.dict --> meta data
1. look at imported functions in refresh.py - what is refresh user, enrollments, grade_info, etc. doing
1. Creating a new filter in AskOski that will filter a user's suggested courses based on whether their majors fall within the class reservations. This filter will be applied automatically to the already existing Open Seats filter. This task is a two-step process:
    1)  Modify Data-AskOski to include reserve capacity information with each class, which involves querying the reserved seats API and augmenting the next_sem_dict to include reserve capacity data.
    2)  Modify Service-AskOski to filter classes shown based on the reserve capacity data and the student's own majors. This involves creating a mapping between majors as represented in AskOski to the requirement groups in the API, and then creating a filter with it.

------------------------------------------------------------

## Questions: 

1. what is the purpose of the copy files section? 
    cp $rootDir/outputs/course2nb.json $outDir
    cp $rootDir/outputs/askoski $outDir
    cp $rootDir/outputs/askoski.json $outDir
    cp $rootDir/outputs/course2vec.npy $outDir
    cp $rootDir/outputs/search_keywords.pkl $outDir
1. does it make sense that match_course_to_idx2course and joining course & class descriptions comes after all the retraining?  what's the point in that?  
    - difference between course_description_init vs course_description_final? 

## Errors? 

1. Is this error a problem in data refresh?  `invalid literal for int() with base 10: 'STUDENT_ID' STUDENT_ID`? 
1. Models c2v retraining message
    - refresh_serendipitous_c2v.py:74: RuntimeWarning: invalid value encountered in true_divide
  bow_weight_for_equi /= bow_weight0[:, np.newaxis]
    - refresh_serendipitous_bow.py:29: FutureWarning: by argument to sort_index is deprecated, please use 
.sort_values(by=...)
    courses = courses.sort_index(by=['idx'])
1. `Loaded Next Semester Courses HTTP Error 404: Not Found` - is this an actual error or did it just run out of pages to read and it's actually fine?  the class files look the same (from Data-AskOski refresh api script)
1. Traceback (most recent call last):
  File "course_api.py", line 35, in <module>
    headers['app_key'] = os.environ['courseAppKey']
  File "/usr/lib/python3.5/os.py", line 725, in __getitem__
    raise KeyError(key) from None
KeyError: 'courseAppKey'

------------------------------------------------------------

## Completed 

### Task: Reconcile Data-AskOski API scripts & Models-AskOski API scripts.  What's the difference between Models API scripts and Data API scripts?  
- Run completed this

### Task: Incorporate Courses / Classes API, Salt & Plan into Data pipeline 

- Explore re-training is broken - currently uses old research data. Update the models code to use pipeline Classes data instead of Classes_2011_2018 data

1. where does `hashed path` get defined? in env.sh vs env.json?  
    - actually from `makeJson` which takes dirName (timestamp) as an argument and then creates `env.json`
    - bash env file is unused
    - NEED `hashed` directory in UCBDATA
1. why does /research/UCBD2/pipeline-test still exist in env.json? bc env.json hasn't been updated from running master 
1. Double check that models retrain still runs on the hashed data in UCBD2/edw_data/hashed?  No, will definitely work because they're the same files
1. Running pipeline should retrain all the models and write all the files service needs to /models 
    - need to copy over env.json & relaunch service?  Yes
1. Checking update-pipeline runs without error, run from your own directory & reserve /askoski for master?  Yes
    - need to run in screen?  Yes
1. how to verify pipeline has successfully run?  should have outputs in the timestamped dir?  
    - yes, or copy env.json and make sure service runs as expected
1. Missing files?? 
    - `/research/UCBDATA/edw_askoski_apr_student_requirements.txt "['PERSON_PARTY_SK'] not found in axis"`, this is a try catch block
    - `cp: cannot stat '/research/UCBDATA/edw_askoski_course_lists.txt': No such file or directory` --> changed `edw_askoski_course_lists` to `edw_askoski_apr_course_lists`
    - Models-AskOski/RNN/evaluate.py: `No such file or directory: '/research/UCBD2/classAPI/next_sem_classes_new.p'` --> bring back folder UCBD2/classAPI from archive
    - nearest_course.py: `FileNotFoundError: [Errno 2] No such file or directory: '/research/UCBD2/edw_data/2019-12-10-17-55/model/course2idx_new.json'`
    - what are all the _bk files & what file are these? - _bk = backup files 
        - mv: cannot stat '/research/UCBD2/edw_data/2019-12-10-17-55/model/course2idx_all.json': No such file or directory
        - mv: cannot stat '/research/UCBD2/edw_data/2019-12-10-17-55/model/idx2course_all.json': No such file or directory
        - mv: cannot stat '/research/UCBD2/edw_data/2019-12-10-17-55/model/askoski_new': No such file or directory
        - mv: cannot stat '/research/UCBD2/edw_data/2019-12-10-17-55/model/askoski_new.json': No such file or directory
    - File "../C2V/preprocess.py", line 190, in <module> with open(os.path.join(RNN_DIR, 'course2idx.json'), 'r', encoding='utf-8') as f:
        No such file or directory: '/research/UCBD2/edw_data/2019-12-10-17-55/model/course2idx.json' <- this file is missing 3 times
    -  need to copy from prev timestamped directory?  no, it was caused by missing directory classAPI which caused all the course mappings to not be generated, this was a propagated error
1. File "train.py", line 253, in <module>
    sys.exit(main(sys.argv[2:]))
  File "train.py", line 204, in main
    has_gpa=hyper_parameter_dict['has_gpa'], has_bow=hyper_parameter_dict['has_bow'], use_pca=hyper_parameter_dict['use_pca'], detail_output=True)
  File "/research/home/askoski/Models-AskOski/RNN/evaluate.py", line 157, in run_on_evalset
    available_courses = get_available_courses(eval_semester)
  File "/research/home/askoski/Models-AskOski/RNN/evaluate.py", line 107, in get_available_courses
    print("There are {} unique courses offered in semester {}".format(len(course_detail_dict[eval_semester]), eval_semester))
KeyError: '20198' --> change to 20191 in RNN `config.json` by checking `course_detail_dict.json`
1. Traceback (most recent call last):
  File "add_new_courses.py", line 96, in <module>
FileNotFoundError: [Errno 2] File b'../shared/generate_descriptions/outputs/courses_with_description.tsv' does not exist: b'../shared/generate_descriptions/outputs/courses_with_description.tsv'
    - READING FROM A DIRECTORY AND FILE THAT DOESN'T EXIST
    - PROBABLY LOOKING FOR course_description_final.tsv BUT THIS FILE IS ONLY GENERATED DURING THE REFRESH STAGE
1. Traceback (most recent call last):
  File "nearest_course.py", line 110, in <module>
    main()
  File "nearest_course.py", line 97, in main
    course2idx_new = json.load(open(COURSE2IDX_NEW_PATH, 'r'))
FileNotFoundError: [Errno 2] No such file or directory: '/research/UCBD2/edw_data/2019-12-12-16-37/model/course2idx_new.json'
    - nearest_course.py called from `add_new_courses.sh`
    - `course2idx_new.json` not properly outputted from `add_new_courses.py`
1. File "augment_model.py", line 82, in <module>
    main(sys.argv[1])
mv: cannot stat '/research/UCBD2/edw_data/2019-12-12-16-37/model/course2idx_all.json': No such file or directory
mv: cannot stat '/research/UCBD2/edw_data/2019-12-12-16-37/model/idx2course_all.json': No such file or directory
mv: cannot stat '/research/UCBD2/edw_data/2019-12-12-16-37/model/askoski_new': No such file or directory
mv: cannot stat '/research/UCBD2/edw_data/2019-12-12-16-37/model/askoski_new.json': No such file or directory
    - ALL THESE ARE FROM THE SAME ERROR above bc
1. Traceback (most recent call last):
  File "../C2V/preprocess.py", line 190, in <module>
    with open(os.path.join(RNN_DIR, 'course2idx.json'), 'r', encoding='utf-8') as f:
FileNotFoundError: [Errno 2] No such file or directory: '/research/UCBD2/edw_data/2019-12-12-16-37/model/course2idx.json'
    - Also same error as above because course2idx_all.json is renamed to course2idx.json but the former is never created due to the error in `add_new_courses.py`
1. If need to run Models independently
    - export srcDir='/research/UCBD2/edw_data/2019-12-11-12-02/hashed'
    - export outDir='/research/UCBD2/edw_data/2019-12-11-12-02/model'
    - export saltDir='/research/UCBD2/edw_data/2019-12-11-12-02/salt'
    - export aprDir='/research/UCBD2/edw_data/2019-12-11-12-02/apr'
1. same error with `../shared/course_api/outputs/course_description_final.tsv` also `Getting class section data from API` only goes up to 33? 
    - changed `COURSE_DESCRIPTION_PATH` to `course_description_init.tsv` in `add_new_courses.py`
    - also change `course_info_path` in ICS `data-joining.py`
1. refresh_serendipitous_bow.py NLTK error causes `course_id.pkl` to not be generated which creates a propogated error in refresh_serendipitous_c2v
1. how is ICS still training the model with it doesn't even have a vector file?
    - because it's reading previous files in the local data directory --> need to remove these files
    - is it reading in the most updated files?  track where `idx2course` & `course2vec.npy` are coming from
1. cp: missing destination file operand after '/home/matthew/Models-AskOski/shared/class_api/outputs/abbreviations.tsv'
Try 'cp --help' for more information.
cp: missing destination file operand after '/home/matthew/Models-AskOski/shared/class_section_api/outputs/class_section_final.tsv'
- /research/UCBD2/edw_data/2020-01-09-19-51/plan
1. move deprecated files from askoski_common to archive in UCBD2 - do a text search for /research/askoski_common in Data and Models to see which files / folders are still being used
    - /research/UCBD2/ucbd2_archive/askoski_common_archive
1. refresh_serendipitous_c2v.py:74: RuntimeWarning: invalid value encountered in true_divide
  bow_weight_for_equi /= bow_weight0[:, np.newaxis]
  refresh_serendipitous_bow.py:29: FutureWarning: by argument to sort_index is deprecated, please use .sort_values(by=...)
  courses = courses.sort_index(by=['idx'])
1. /add_new_courses.sh: line 5: 31520 Killed   python augment_model.py askoski
mv: cannot stat '/research/UCBD2/edw_data/2020-01-16-13-04/model/askoski_new': No such file or directory
mv: cannot stat '/research/UCBD2/edw_data/2020-01-16-13-04/model/askoski_new.json': No such file or directory

### service errors  

> `cp /home/matthew/Data-AskOski/env.json /home/matthew/Service-AskOski/service`

```
Traceback (most recent call last):
  File "service.py", line 30, in <module>
    from load import *
  File "/research/home/matthew/Service-AskOski/service/load.py", line 111, in <module>
    bow_course_id_file = env_dict['bowCourseIdFile']
KeyError: 'bowCourseIdFile'
```
- there exists two bowCourseIdFiles in the old env.json with literally the same key --> only one in new env.json and is not called bowCourseIdFile but just courseIdFile
- course2vectorBOWEquivalencyMatrix vs bowRelationMatrix in old env.json since there's only one bowRelationMatrixFile in the new env.json
- there exists two references to same file `bestC2V` & `best_model_file`
    - actually not the same file, it's confusing naming convention bc bestC2V refers to `course2vec.npy` but best_model_file refers to `best_course2vec.pkl`

ValueError: Error when checking input: expected inputCourseMultihot to have shape (13, 9329) but got array with shape (13, 9368)
    - what is the difference between np and password mode where if all the files are the same between them, you get the same results and errors.  no you don't get the same results, bc of fake data but you do get the same error like you did above

[x] **writing courseDescriptionFinalFile to env.json should be a .tsv file** 
[x] what's the way to test if env.json works not just env.test.json? - we can assume if np mode works with the dummy_data files then production will work bc they are the same files.  What about the files that were diffed by github?  well if they were actually changed then Run took them from the latest pipeline run so np and p mode should still be the same
- refresh.sh (from Models) is dumping outputs into timestamped `salt` - why? SAlt stands for serendipitous alternatives

### Task: SQL DB Transition instead of pandas

- service-askoski will definitely have to change because it's will no longer load pickle files but make SQL queries?  possibly models-askoski will change
- keep data askoski pipeline to process data but load exports into mySQL to be used in production

### Task: Move all scripts and post-processed data out of UCBDATA & UCBD2
    
    - *Don't delete the encrypted files o/w you have to wait for the next data dump*
    - verify data is encrypted before moving out of UCBDATA - actually just keep here according to Zach
    - which are the files to not delete - don't delete the raw files

1. [x] archive files in UCBD2
1. [x] remove folders manually from UCBD2 - check if they can be deleted
    - pycache is just machine optimized code created every time python script is run, can be ignored - or deleted in this case
    - models-askoski is deprecated, nothing in git log
    - dev is empty
1. [x] change default srcDir path in models and add search model retrain
1. [x] Double save hash in UCBD2 & remove hashed data from UCBDATA in refresh.py 
    - Double check `rm -r` works from `os.system`
1. PR note
Included:
- Double save anonymized data to UCBD2/edw_data/hashed
- Remove hashed data from UCBDATA after saving to UCBD2

Test:
- Running pipeline should have hashed data saved to both timestamped directory and hashed directory in edw_data as well as hashed data removed from from UCBDATA
