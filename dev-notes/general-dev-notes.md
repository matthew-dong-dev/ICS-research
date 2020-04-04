
# Misc notes / questions / to do's

1. look at network requests when you go to requirements tab
1. SSL 
    - look into SSL_context obj & clear related tabs after taking notes
    - where are the SSL certs located? `/research/askoski_common/ssl/`
    - CORS errors are  different from SSL errors but both can cause HTTP bad request errors if you are trying to make a cross-origin request or if you're trying to request a resource from a non secured site (e.g. there might be outside listeners)
    - potential problems - is it the server that's blocking the request?  yes... but could it also be the client?
    - what did you try so far?  if all else fails download the extension
1. What are these files in askoski_common
    env_dict["sidHashBin"] = commonPath + '/bins/sidHash_new.bin'
    env_dict["seedBin"] = commonPath + '/bins/seed.bin'
    env_dict["readBin"] = commonPath + '/bins/read.bin'
    env_dict["writeBin"] = commonPath + '/bins/write.bin'
    env_dict["classesIdBin"] = commonPath + '/bins/classesId.bin'
    env_dict["classesKeyBin"] = commonPath + '/bins/classesKey.bin'
    env_dict["key"] = commonPath + '/ssl/askoski.berkeley.key'
    env_dict["crt"] = commonPath + '/ssl/oski.crt.old'
1. what exists in `UCBD2` directory, referred to a lot in `env.json`?  does it matter for you rn?  you can view the lookup tables in models-askoski
1. where is the production version of FE & BE located? `/home/askoski`

## Testing

> Mamba is just like Behat in php, both are BDD testing frameworks.  Just like you have scenarios and keywords in behat, you have contexts and keywords in mamba

1. How are travis and mamba linked? - by the travis.ci file
1. don't you need to the command `pipenv run mamba` to run all the tests instead of just `- mamba --format=documentation`, apparently not, you can see for yourself in the travis job log all that all the tests are running on build
1. read mamba documentation
1. look through other test files 

---------------------------------------------------------------------------------

> Always pull from staging but start dev from master.
> KNOW WHEN YOU'RE IN REMOTE VS LOCAL DEV - you didn't see git ignore changes because your console was on the server and you accidentally removed files you thought you could get back but you were on the server Models-AskOski not local

# Remote Development 

1. Do work locally in an IDE, then copy & paste into ipython env is what Jeff recommends
1. run `screen -S name`
1. run the script / start up the backend / open jupyter notebook 
    - `jupyter notebook --ip maxwell.ischool.berkeley.edu --port 1382`
1. When you use screen you need to detach with `CTRL+A+D` before you exit ssh. 
1. `screen -xS name-to-resume`
1. scroll in screen: https://unix.stackexchange.com/questions/40242/scroll-inside-screen-or-pause-output
    - Hit your screen prefix combination (C-a / control+A by default), then hit Escape.
    - Copy mode only works in screen, you can scroll normally otherwise
1. `control + d` terminates screen
1. If you feel that the program is hanging, YOU HAVE TO ESCAPE OUT OF COPY MODE TO SEE LIVE OUTPUT
1. `screen -XS [session # you want to quit] quit` to kill a screen (case matters)

## Remote Backend

- change port manually in `env.json` & run `python service.py --no-pass` 

Deprecated

- `python ../scripts/refresh/refresh_env.py --port=1381 --no-pass` with `env.json` file
- `source env.sh` `python service.py -np`

```# ports used by user
netstat -tlnpe | awk '{print $7 " " $4}' | sed s/:/\ /g | grep -E '0.0.0.0|169.229.192.179' | awk '{if ($3 >= 1300 && $3 <=1399 ) print $3" "$1;}'| sort | awk '{ print "id -u -n " $2}' | sh | sort | uniq -c | sort
```

export outDir='/home/matthew/Models-AskOski/ICS/data'
outDir='/home/matthew/Models-AskOski/ICS'
echo $outDir

>>> python
>>> import os
>>> os.environ['outDir']

## Remote Frontend

- https://github.com/CAHLR/Angular-AskOski/wiki/Standing-up-a-demo-frontend-on-maxwell no longer true because `development.js` removed? 

---

# Local Development

## Local FE 

1. if something is broken here run npm install or restart the app

- running into local FE error again where it keeps trying to log into your account and you can't get the site to forget your login details so you can use the dummy account. maybe it's CAS that's caching login details?  it's the same error when trying to log into caltime - you inputted your credentials incorrectly once and kept getting stuck in an login error message.  Worked in icognito but using dev tools to clear shit didn't work, you had to clear everything through the browser settings for you to be able to go in properly again.   

How to get browser to forget user login data?  i.e. how to delete cache / locally stored data / cookies? 

- https://superuser.com/questions/1305644/how-can-i-delete-locally-stored-data-in-chrome
- Can't figure out which one works: empty cache and do hard reload from the refresh button, rebuilding the site,  maybe `clear site data` through dev tools just takes a few seconds to propogate?
- Sometimes you have to go to askoski.berkeley.edu and clear that data? - no, this doesn't make sense because your localhost is completely indepedent of the production server

- **Had to change all the endpoint urls from `api.askoski.berkeley` to just `askoski.berkeley`  to enable client server communication, but local version of `plan` endpoints doesn't work rn?** - resolved with latest update to staging 11/5 

- .spec file is for tests
- use `ng serve` and change env port in `environment.ts` to match the backend service you're using for now 
- supposed to use docker now instead instead of `npm install`, `ng serve` but README in Angular-AskOski is incorrect, no such `container.py` script?.  You can call `sh run-docker.sh` but this only opens production env, how to standup dev env? 
    - Kill docker process: Open a new shell and execute
    - `docker ps` # get the id of the running container
    - `docker stop <container>` # kill it (gracefully)

## Local BE 

- cannot standup service locally, need configurations & packages on maxwell until containerized 

### Transfer model files from timestamped to local dummy_data

1. To transfer between servers: `ssh -A -t user1@remote1 scp srcpath user2@remote2:destpath` 
	- `ssh -A -t matthew@askoski.berkeley.edu scp /home/matthew/data/course_shortname_title.pkl matthew@cahl.berkeley.edu:~/askoski/data`

1. Transfer file from server to local 
	- `scp matthew@askoski.berkeley.edu:/home/matthew/Data-AskOski/env.json /Users/mdong/dataScience/cahlr/askoski/Service-AskOski/service`
	- `scp matthew@askoski.berkeley.edu:/research/UCBD2/edw_data/2020-03-31-00-05/classAPI/next_sem_classes_new.p /Users/mdong/dataScience/cahlr/askoski/Service-AskOski/dummy_data/classAPI`

1. transfer from local to server
	- `scp /Users/mdong/Desktop/mdong.jpg matthew@askoski.berkeley.edu:/research/AskOski-CMS/people/img`