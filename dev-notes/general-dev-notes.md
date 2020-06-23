# Remote Development Workflow

1. Don't fork the system repos
1. Do work locally in an IDE, then copy & paste into ipython env or push and pull from github
1. run `screen -S name`
1. run the script / start up the backend / open jupyter notebook 
    - `jupyter notebook --ip maxwell.ischool.berkeley.edu --port 1382`
1. When you use screen you need to detach with `CTRL+A+D` before you exit ssh. 
1. `screen -xS name-to-resume`
1. [scroll in screen](https://unix.stackexchange.com/questions/40242/scroll-inside-screen-or-pause-output)
    - Hit your screen prefix combination (C-a / control+A by default), then hit Escape.
    - Copy mode only works in screen, you can scroll normally otherwise
1. `control + d` terminates screen
1. If you feel that the program is hanging, YOU HAVE TO ESCAPE OUT OF COPY MODE TO SEE LIVE OUTPUT
1. `screen -XS [session # you want to quit] quit` to kill a screen (case matters)

### using `screen`
	
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
- what does screen do? https://www.rackaid.com/blog/linux-screen-tutorial-and-how-to/ 

### using ipython env

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

`ports_used` to check which ports are available
`gpu_who` to check gpu 

```# ports used by user
netstat -tlnpe | awk '{print $7 " " $4}' | sed s/:/\ /g | grep -E '0.0.0.0|169.229.192.179' | awk '{if ($3 >= 1300 && $3 <=1399 ) print $3" "$1;}'| sort | awk '{ print "id -u -n " $2}' | sh | sort | uniq -c | sort
```

### Transfer model files from timestamped to local dummy_data

1. To transfer between servers: `ssh -A -t user1@remote1 scp srcpath user2@remote2:destpath` 
	- `ssh -A -t matthew@askoski.berkeley.edu scp /home/matthew/data/course_shortname_title.pkl matthew@cahl.berkeley.edu:~/askoski/data`

1. Transfer file from server to local 
	- `scp matthew@askoski.berkeley.edu:/home/matthew/Data-AskOski/env.json /Users/mdong/dataScience/cahlr/askoski/Service-AskOski/service`
	- `scp matthew@askoski.berkeley.edu:/research/UCBD2/edw_data/2020-05-29-14-43/search/search_keywords.pkl /Users/mdong/dataScience/cahlr/askoski/Service-AskOski/dummy_data/search`

1. transfer from local to server

## Using CAHL Server

1. `jupyter notebook --certfile=/etc/jupn-cert.pem --keyfile /etc/jupn-key.key --ip cahl.berkeley.edu --port 1338`
1. Go to https://cahl.berkeley.edu:1338/
    - issue with server persistently running, port is always open?: https://stackoverflow.com/questions/38511673/cannot-quit-jupyter-notebook-server-running 