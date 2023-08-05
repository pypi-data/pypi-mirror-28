Generic job queue module
=================

Project target provide a standard interface for push job to queue system & job worker

Currently only support using SQLAlchemy (That mean you can choice any relational database system) as broker

Table of contents
=================
  * [Installation](#installation)
  * [Development](#development)
  * [Testing](#testing)
  * [Usage](#usage)
    * [Create table structure](#create-table-structure)
    * [Push Job To Queue](#push-job-to-queue)
    * [Pull job from queue](#pull-job-from-queue)
  * [Best Practice](#best-practice)

Installation
============
```bash
pip3 install generic_job_queue
```

Development
===========
Project is using [pipenv](https://github.com/kennethreitz/pipenv) to manage dependency

So in order to get started, install pipenv first.
```bash
pip3 install pipenv
# Or if you are mac user
brew install pipenv
``` 

After install pipenv, you can setup this repo by following command
```bash
pipenv --three install
```

Testing
=======
Following command will execute all test and shown the code coverage report
```bash
pipenv shell
py.test --cov=generic_job_queue
```

Usage
=====
Create table structure
----------------------
```python
from sqlalchemy import create_engine

from generic_job_queue import SALAlchemyModelBase

engine = create_engine('sqlite:///:memory:', echo=True)
SALAlchemyModelBase.metadata.create_all(engine)

```

Push Job To Queue
-----------------
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from generic_job_queue import SQLAlchemyJob
from generic_job_queue import SQLAlchemyJobQueue

engine = create_engine('sqlite:///:memory:', echo=True)
sa_session_maker = sessionmaker(bind=engine)
job_name = "The display name of Job"
job_handler = "demo"
job_payload = {}
job = SQLAlchemyJob.new_job(job_handler, job_payload, job_name)
SQLAlchemyJobQueue(sa_session_maker).push_job(job)
```

Pull job from queue
-------------------
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from generic_job_queue.contracts import JobHandler
from generic_job_queue import SQLAlchemyJobQueue
from generic_job_queue import JobPuller

class DemoJobHandler(JobHandler):
    def handle(self, job, job_logger):
        print("Demo")

engine = create_engine('sqlite:///:memory:', echo=True)
sa_session_maker = sessionmaker(bind=engine)
puller = JobPuller(SQLAlchemyJobQueue(sa_session_maker))
puller.set_handler("demo", DemoJobHandler())
puller.start()
```
