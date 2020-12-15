# Micro Proctoring

This is a server of microproctoring service. It's been written on `flask` and uses `uwsgi` for deploy.
The frontend part is stored in a separate repo. It's been written on `react`.

To make the things work you need:
1. Install and run microproctoring server. (It's described below)
2. Compile frontend part using react
3. Place \*.js files got from the previous step to the static folder on server. Update index.html of the server using index.html compiled by react.

## Prerequirements:

- Ubuntu 20. _(Other systems are also possible, but there may be some issues)_

Firstly install

- Python3
- pip
- venv
- sqlite

## Prepare to run the app:

1. Clone the repo and navigate to it:

 ```
 git clone https://github.com/morriell/micro_proctoring.git
 cd micro-proctoring
 ```

2. Create virtualenv and activate it:

```
python3 -m virtualenv venv
source ./venv/bin/activate
```

3. Install requirements:

```
pip install -r requirements.txt
```

4. Create database using python interactive comand line:

```
$ python3
Python 3.8.5 (default, Jul 28 2020, 12:59:40) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from project import db, create_app
>>> db.create_all(app=create_app()) 
```

Now db.sqlite file should appear in project folder

Everything is ready to get launched.

## Run app

Remember to get virtualenv activated (See p.2 from above).

To run locally, the app should be started with develop config:

```
export CONF_NAME=dev; flask run
```

Now you can check `localhost:500` for the app

## ToDo

- [x] Replace profile page with relevant one
- [x] Create start and stop record buttons
- [x] Update a page with link to the record done (redirect after stop record)
- [ ] Replace css with a local one
- [x] Add a timer to recieve_photo method. The timer returns time left till the max session length
- [ ] Show the timer if less then 30 min left
- [x] Send photoes using ajax POST
- [x] Create a method to start the record session. May be add a new field to DB
- [x] Create a method to accept pictures and store them. Name of a picture should be a timestamp
- [x] Create a method to finish record session
- [x] Create a page to show artifacts
- [x] Create a separate table for sessions
- [x] Make an archive from fotos, place a timastamp file nearby and return a link to this folder after record was stopped
- [x] Create a script that removes outdated records
- [ ] Translate all menus etc
- [ ] Write some instructions for users
- [ ] Add deployment configs
- [ ] Add e-mail based authorization
