
# Misc notes / questions / to do's

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

## Remote Backend

- change port manually in `env.json` & run `python service.py --no-pass` 

Deprecated

- `python ../scripts/refresh/refresh_env.py --port=1381 --no-pass` with `env.json` file
- `source env.sh` `python service.py -np`

## Data Science Sandbox

1. `qsub` 
	- **Need to use absolute paths**
	- `qstat` to view status and `qdel` to kill jobs
	- `cat` output files to read
	- `top` to view jobs

1. GPU memory issues
	- `export CUDA_VISIBLE_DEVICES=""` to only use CPUs (`env` to check env variables)
	- export is a command that you give directly to the shell (e.g. bash), to tell it to add or modify one of its environment variables. You can't change your shell's environment from a child process (such as Python), it's just not possible.  Therefore you can't set which GPU using `os.environ["CUDA_VISIBLE_DEVICES"]="1,2,3"`
	- use `export CUDA_VISIBLE_DEVICES=1` instead
	- If encounter `ResourceExhaustedError` or `Allocator (GPU_0_bfc) ran out of memory` run `gpu_who` and kill your existing jobs, but make sure you don't accidentally kill the backend OR reduce batch size

--------------------------------------------------

## Remote Frontend

- https://github.com/CAHLR/Angular-AskOski/wiki/Standing-up-a-demo-frontend-on-maxwell no longer true because `development.js` removed? 

## Standing up FE 

## Local FE 

1. start dev instance using: 

`npm run-script development`
`node development.js`

1. **Devtools** - `CMD + Shift + C` to open 
1. Network tab:
	- hit preserve log to record the time it takes for processes to work
1. Can use as IDE in sources tab 
	- access component properties in the console using `this`
	- establish breakpoint using `debugger` command

1. if compile error when running `ng serve --open` make sure `npm install` first

```
npm install --save @angular/material @angular/cdk
rm -rf node_modules
npm install
```

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

How to get backend running:
1. From service folder: `source ../scripts/env.sh`
1. `python service.py -np`

