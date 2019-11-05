test-300852
f1$hNch1p$

# Misc notes / questions

1. where are the SSL certs located? `/research/askoski_common/ssl/`
1. what exists in `UCBD2` directory, referred to a lot in `env.json`?  does it matter for you rn?  you can view the lookup tables in models-askoski
1. where is the production version of FE & BE located?

Directions for you to pursue

1. finish RNN preprocess refactor
1. plan refactor
    1. refactor rnn_predict function (everything except form data) + 
1. data-askoski - start looking through the repo, any immediate action items here? 
1. add unit test coverage for your refactored shit? look at testing pipeline
1. remove global variables - a lot of overhead

What is APR data?

- sid, course and what requirement it fulfills, t/f for fulfilled

---

## Testing

> Mamba is just like Behat in php, both are BDD testing frameworks.  Just like you have scenarios and keywords in behat, you have contexts and keywords in mamba

1. How are travis and mamba linked? - by the travis.ci file
1. don't you need to the command `pipenv run mamba` to run all the tests instead of just `- mamba --format=documentation`, apparently not, you can see for yourself in the travis job log all that all the tests are running on build
1. read mamba documentation
1. look through other test files 

---

# Remote Development 

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

- **Had to change all the endpoint urls from `api.askoski.berkeley` to just `askoski.berkeley`  to enable client server communication, but local version of `plan` endpoints doesn't work rn?**

How to get browser to forget user login data?  i.e. how to delete cache / locally stored data / cookies? 

- https://superuser.com/questions/1305644/how-can-i-delete-locally-stored-data-in-chrome
- Can't figure out which one works: empty cache and do hard reload from the refresh button, rebuilding the site,  maybe `clear site data` through dev tools just takes a few seconds to propogate?
- Sometimes you have to go to askoski.berkeley.edu and clear that data? - no, this doesn't make sense because your localhost is completely indepedent of the production server

- .spec file is for tests
- use `ng serve` and change env port in `environment.ts` to match the backend service you're using for now 
- supposed to use docker now instead instead of `npm install`, `ng serve` but README in Angular-AskOski is incorrect, no such `container.py` script?.  You can call `sh run-docker.sh` but this only opens production env, how to standup dev env? 
    - Kill docker process: Open a new shell and execute
    - `docker ps` # get the id of the running container
    - `docker stop <container>` # kill it (gracefully)

## BE 

- cannot standup service locally, need configurations & packages on maxwell until containerized 