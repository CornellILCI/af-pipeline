## A Task Orchestration Platform Based on Celery 

This demo requires Docker.

Docker-compose will run 4 services:

1.  JobAPI - A REST based API for submitting jobs AND getting the status of the jobs from (NOTE: NOT YET IMPLEMENTED)

2.  RabbitMQ (with management interface so we can use that to submit jobs instead)

3.  Example Celery Worker With Job Consumer

4.  Redis (TODO: Not yet Included) for storing Job status / results


### How to RUN:

From the repository root dir (since the docker-compose file is there):

`
%  docker-compose build
` 

`
%  docker-compose up -d   
`


(or remove -d if you want the logs to display on your current console)

This will run the af-jobs-api service, and the af-task-orchestrator service, along with a RabbitMQ service.


TODO:  JobAPI demo

### How To Submit A Job Using AF-Jobs-API Service (using Curl)

Get a token from [EBS UAT](https://b4rapi-uat.ebsproject.org/v3/auth/login) and then use the token in the request.

`
% curl -X POST --header 'Content-Type: application/json' --data '{"experimentId":"1", "occurenceId": "2", "traitId": "3", "dataSource": "EBS", "dataSourceId": "EBS1", "processName": "data_gathering_demo", "dataType": "PHENOTYPE", "apiBearerToken": "eyTokenHERE"}' http://localhost/process
`

### How To Submit "Jobs" Via Rabbit MQ 

1.  Login to the management interface:  http://localhost:15672/
2.  Username: admin,  Password: mypass
3.  Go to _Queues_
4.  Select _jobs_ queue
5.  On the Payload textarea, input either: 

```
{"jobId": "someid", "jobName": "sample_workflow"}
```

or

```
{"jobId": "fooid", "jobName": "sample_workflow_2"}
```

...and watch celery execute our workflow through the logs.

### How To Run Without Docker/Docker-compose

1.  You should have RabbitMQ running.
2.  You'll need to set the following env vars:

* `BROKER='amqp://<rabbituser>:<rabbitpass>@localhost:5672'`
* `BACKEND='rpc://'`
* `CONSUMER_QUEUE=jobs`

3.  Install python requirements: (on ap/orchestrator folder)  `pip3 install -r requirements.txt`
4.  You can celery worker:  (on ap folder) `celery -A orchestrator.app worker --pool=gevent --concurrency=20 -l debug`


