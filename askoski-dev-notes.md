# Service RNN Refactor

## To do 

1. figure out what the FE is sending to the BE 
1. figure out how the BE is turning that into predictions, rn the RNN is a blackbox, as well as the /nextcourse/predict endpoint
WHERE IS THE STUDENT ENROLLMENT HISTORY BEING OBTAINED? 

### FE Model 

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


## RNN 

- try dumping things to the *server terminal* by printing things from your predict endpoint OR use Postman to send requests so you can view the printed output easier

> /nextcourse/predict

-  receives a request form from the FE... and passes it into build_matrix_from_dict which is doing what exactly?  
- notice changing the SID changes the recommendations...so the data lookup has something to do with the SID


--- 

Logistics 

- Had to change all the endpoint urls from `api.askoski.berkeley` to just `askoski.berkeley`  to enable client server communication, but local version of `plan` endpoints doesn't work rn? 

How to get browser to forget user login data?  i.e. how to delete cache / locally stored data / cookies? 

- https://superuser.com/questions/1305644/how-can-i-delete-locally-stored-data-in-chrome
- Can't figure out which one works: empty cache and do hard reload from the refresh button, rebuilding the site,  maybe `clear site data` through dev tools just takes a few seconds to propogate?
- Sometimes you have to go to askoski.berkeley.edu and clear that data? - no, this doesn't make sense because your localhost is completely indepedent of the production server

---

# Server Development

1. run `screen -S name`
1. run the script / start up the backend / open jupyter notebook (jupyter notebook --ip 169.229.192.179 --port 1382)
1. When you use screen you need to detach with `CTRL+A+D` before you exit ssh. 
1. `screen -xS name-to-resume`
1. scroll in screen: https://unix.stackexchange.com/questions/40242/scroll-inside-screen-or-pause-output

- Hit your screen prefix combination (C-a / control+A by default), then hit Escape.
- THIS IS COPY MODE SO YOU HAVE TO ESCAPE OUT OF IT AGAIN TO SEE LIVE API CALLS 

## Backend

- now run `python ../scripts/refresh/refresh_env.py --port=1381 --no-pass` with `env.json` file
- now it's just `python service.py --no-pass` and change port manually in `env.json`
- what exists in `UCBD2` directory, referred to a lot in `env.json`?  does it matter for you rn?  you can view the lookup tables in models-askoski
- where is the production version of FE & BE located?

## Frontend

- https://github.com/CAHLR/Angular-AskOski/wiki/Standing-up-a-demo-frontend-on-maxwell no longer true because `development.js` removed? 

---

# Local Development

## FE 

- .spec file is for tests
- use `ng serve` and change env port in `environment.ts` to match the backend service you're using for now 
- supposed to use docker now instead instead of `npm install`, `ng serve` but README in Angular-AskOski is incorrect, no such `container.py` script?.  You can call `sh run-docker.sh` but this only opens production env, how to standup dev env? 
    - Kill docker process: Open a new shell and execute
    - `docker ps` # get the id of the running container
    - `docker stop <container>` # kill it (gracefully)

## BE 

- cannot standup service locally, need configurations & packages on maxwell until containerized 

--- 

Old dev notes: https://github.com/mdong127/ICS-research/tree/master/notes