# EveryoneAPI-PyDipper

# Summary

A basic python script hitting the https://www.everyoneapi.com/ for phone number related data.  
Input is line of 10 digit US Telephone numbers, output is the result of the API dip.  
This seemed like a good opportunity to play with Docker, documented running standalone and with Docker.

Setup an API token and SID from https://www.everyoneapi.com/sign-up (it's simple).

## Input

Your input file should be a list of telephone numbers, example:


```
$ cat test.csv
3155551212
6075551212
```

The `full` and `ocn` flag dictates what we are requesting.  You can modify the flags following the everyoneApi docs.

- OCN: `carrier` `carrier_o`
- FULL: `cnam`, `name`, `carrier`, `carrier_o`, `linetype`, `address`, `location`

## Using Docker

- Setup your working directory `mkdir ~/Documents/Dipper ; cd $_`
- Grab the repo `git clone https://github.com/ctaloi/EveryoneAPI-PyDipper.git .`
- Create a "shared" directory to store your input and output `mkdir shared`
- Drop your input csv into the new shared directory
- Add your EveryoneAPI `SID` and `TOKEN` to the `Dockerfile`
- Build the docker image `docker build -t docker-humanapi .`

Run the script using the following syntax:

`docker run -v shared:/shared -d docker-humanapi python /app/get_cnam.py /shared/numbers.csv full`

Huh? Explained:

- Run this: `docker run`
- Mount our shared directory to our Docker machine `-v shared:/shared`
- Run it as a daemon (remove if your want to connect to the tty) `-d`
- The image to run `docker-humanapi`
- The app to run `/shared/numbers.csv full`

Your results should end up under shared/

## Without Docker

PyDipper requires the `requests` python package.  Using a virtualenv to manage your Python setup is clean and easy.

**Note** this is done as root on a temporary virtualized node, if you plan to leave this in service I don't suggest using the root user.

Fresh Ubuntu 14.04 installation.

- Update your packages: `apt-get update ; apt-get upgrade -y`
- Install `pip`: `apt-get install python-pip`
- Install `git`:
- Install `virtualenvwrapper`: `pip install virtualenvwrapper`
- Configure `virtualenvwrapper` (http://virtualenvwrapper.readthedocs.org/en/latest/install.html) by adding the following to your shell startup file (`.bashrc` or `.profile`).
```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh
```

- Check the location of your current Python binary `which python`
```
root@bulk-cnam-dipper:~# which python
/usr/bin/python
```
- Create your virtualenv: `mkvirtualenv PyDipper`
- Check your work:
```
(PyDipper)root@bulk-cnam-dipper:~# which python
/root/.virtualenvs/PyDipper/bin/python
(PyDipper)root@bulk-cnam-dipper:~#
```

- Grab the repo `git clone https://github.com/ctaloi/EveryoneAPI-PyDipper.git`
- Install dependencies `pip install -r requirements.txt`

### Input

```
# cat test
5551234567
```

### Run

```
PYTHONWARNINGS="ignore:Unverified HTTPS request" python get_cnam.py test full
```

### STDOUT

```
full Search for numbers in test
Results in test_res.csv
Reading test
Searching for 1 numbers..
Using full
FULL LOOP
Writing to test_res.csv
 1 Lookup for 5551234567... 0.000195026397705
Batch complete, runtime 0.093190908432
```

### Result

```
root@bulk-cnam-dipper:~/EveryoneAPI-PyDipper# cat test_res.csv
Phone Number,Carrier ID,Carrier Name,Original Carrier ID,Original Carrier Name,CNAM,Derived Name,Line Type,Address,City,State,ZIP,latitude,longitude,Query Cost
5551234567,214,Growing Wireless Inc.,213,Paine Mobile Inc.,MICHAEL SEAVER,Michael Seaver,mobile,15 Robin Hood Lane,Long Island,NY,10003,40.799787,-73.971421,-0.1
```
