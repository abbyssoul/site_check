# Expample Using Kafka producer and consumer in python3
This is sample project consisting of two parts
 - REST checker - a util to check given rest resource and post it's status to a Kafka topic.
 - Kafka consumer to read from the same topic and write recieved values to a DB.

 ## Usage
### Using venv and installing python requirements
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running site cheker once
For stand-alone usage - when site checker is run from a CMD line
```sh
./check_site.py --url='https://api.github.com/'
```

## Running site cheker on an fixed time interval
It is possible to run site checker repeatedly until interap.
```sh
./check_site.py --url='https://api.github.com/' --interval=2
```
this will poll given site every 2 sec untill process is killed.

## Running status persister
Second component of the project is a kafak consumer that reads from status check data
and persists it in a DB.
To run this component from CLI:
It is possible to run site checker repeatedly until interap.
```sh
./store_status.py
```


# Configuration
Default REST status checker and persister rely on config files containing connection details 
for Kafka broker and DB.
- [rest_config.py](./rest_config.py) - Configuration for REST resource poller.
- [db_config.py](./db_config.py) - DB connection credentials.
- [kafka_config.py](./kafka_config.py) - Kafka broker configuration.


 ## Testing
This project is equiped with python unittests.
Easiest way to run unit tests:
```sh
nose2 -t . -s tests/unit/
```
