# Micro Proctoring

## Prerequirements:

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
