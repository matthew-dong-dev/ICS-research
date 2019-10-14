
## Requirements Feature

- in Models-Askoski you can treat the RNN as a blackbox but how exactly is it making predictions for a particular student?  
- try dumping things to the console see what's being returned at each step
- `getStudentData()` calls `getLookupTables` which calls `getLookup` which references the `selects` dict in service.py?

## questions

- what exists in `UCBD2` directory, referred to a lot in `env.json`?  does it matter for you rn?  you can view the lookup tables in models-askoski
- where is the production version of FE & BE located?

---

Old README: https://github.com/CAHLR/ICS-research 

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

# How to stand up dev instance on server

1. run `screen -S name`
1. run the script / start up the backend / open jupyter notebook (jupyter notebook --ip 169.229.192.179 --port 1382)
1. When you use screen you need to detach with `CTRL+A+D` before you exit ssh. 
1. `screen -xS name-to-resume`
1. scroll in screen: https://unix.stackexchange.com/questions/40242/scroll-inside-screen-or-pause-output

- Hit your screen prefix combination (C-a / control+A by default), then hit Escape.

## Backend

- now run `python ../scripts/refresh/refresh_env.py --port=1381 --no-pass` with `env.json` file

## Frontend

- https://github.com/CAHLR/Angular-AskOski/wiki/Standing-up-a-demo-frontend-on-maxwell no longer true because `development.js` removed? 

## DevOps Guides

1. https://circleci.com/blog/build-cicd-piplines-using-docker/
1. https://travis-ci.com/CAHLR/Angular-AskOski/
1. https://docs.travis-ci.com/user/for-beginners/
