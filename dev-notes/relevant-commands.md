## Data Science Sandbox

1. `qsub` 
	- **Need to use absolute paths**
	- `qstat` to view status and `qdel` to kill jobs
	- `cat` output files to read
	- `top` to view jobs

1. GPU issues
	- `export CUDA_VISIBLE_DEVICES=""` to only use CPUs (`env` to check env variables)
	- export is a command that you give directly to the shell (e.g. bash), to tell it to add or modify one of its environment variables. You can't change your shell's environment from a child process (such as Python), it's just not possible.  Therefore you can't set which GPU using `os.environ["CUDA_VISIBLE_DEVICES"]="1,2,3"`
	- use `export CUDA_VISIBLE_DEVICES=1` instead
	- If encounter `ResourceExhaustedError` run `gpu_who` and kill your existing jobs, but make sure you don't accidentally kill the backend

1. `screen`
	- run `screen -S name` 
	- run the script / start up the backend / open jupyter notebook
	- When you use screen you need to detach with `CTRL+A+D` before you exit ssh.
	Misc:
		- `screen -r` will resume the current screen or return a list to resume
		- `screen -xS name-to-resume` 
		- `screen -ls` will list all current screens (ls = list)
		- `screen -d` will detach you from the screen and back into original session
		- `screen -d -r`? 
		- screen must be detached for you to go back into original terminal session
		- run `echo $STY` to check if you are in a screen which is a variable set by the screen command
		- `control + d` just terminates screen
	- `lsof -i :1371`, `kill PID` if necessary


1. To transfer between servers: `ssh -A -t user1@remote1 scp srcpath user2@remote2:destpath` 

	- `ssh -A -t matthew@askoski.berkeley.edu scp /home/matthew/data/course_shortname_title.pkl matthew@cahl.berkeley.edu:~/askoski/data`
	- `ssh -A -t matthew@cahl.berkeley.edu scp /home/matthew/askoski/data/course_subject_long_to_short.csv matthew@askoski.berkeley.edu:/home/matthew/data`

1. Use ipython env

	```
	ssh matthew@askoski.berkeley.edu
	jupyter notebook --generate-config
	jupyter notebook password
	jupyter notebook --ip 169.229.192.179 --port 1332 / jupyter notebook --ip maxwell.ischool.berkeley.edu --port 1332
	Go to http://maxwell.ischool.berkeley.edu:1332/ 
	```
	VS
	```
	jupyter notebook --no-browser --port=XXXX #replace this with a number greater than 1080#
	Then, on your local machine (e.g., laptop) type the following in a terminal
	ssh -N -L localhost:8888:localhost:XXXX username@askoski.berkeley.edu
	```

1. `jupyter notebook --certfile=/etc/jupn-cert.pem --keyfile /etc/jupn-key.key --ip cahl.berkeley.edu --port 1338`
1. https://cahl.berkeley.edu:1338/
	- issue with server persistently running, port is always open: https://stackoverflow.com/questions/38511673/cannot-quit-jupyter-notebook-server-running 
	- what does screen do? https://www.rackaid.com/blog/linux-screen-tutorial-and-how-to/ 
1. don't fork the system repos

	```
	with open(pickled_path, 'rb') as f:
    	vectors = pickle.load(f)
    # equivalent to: 
	my_file = open("example.txt", "r")
	text = my_file.read() # my_file = pickle.load()? 
	my_file.close()
    ```

--------------------------------------------------

## Web Dev SANDBOX

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

1. `ctrl + x` if you ever get stuck in nano

1. User Test Account
	- username: test-300934
	- password: f1$hNch1p$

How to get backend running:
1. From service folder: `source ../scripts/env.sh`
1. `python service.py -np`

master = ground truth <- staging server (PORT = 13XX) <- dev one feature at a time

`ports_used` to check which ports are available
`gpu_who` to check gpu 

```# ports used by user
netstat -tlnpe | awk '{print $7 " " $4}' | sed s/:/\ /g | grep -E '0.0.0.0|169.229.192.179' | awk '{if ($3 >= 1300 && $3 <=1399 ) print $3" "$1;}'| sort | awk '{ print "id -u -n " $2}' | sh | sort | uniq -c | sort
```
