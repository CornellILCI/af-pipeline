## A Task Orchestration Platform Based on Celery 

This demo requires Docker.

Docker-compose will run 4 services:
1.  JobAPI - A REST based API for submitting jobs AND getting the status of the jobs from (NOTE: NOT YET IMPLEMENTED)
2.  RabbitMQ (with management interface so we can use that to submit jobs instead)
3.  Example Celery Worker With Job Consumer
4.  Redis (TODO: Not yet Included) for storing Job status / results


### How to RUN:

`
%  docker-compose build
` 

`
%  docker-compose up -d   
`

(or remove -d if you want the logs to display on your current console)


TODO:  JobAPI demo

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


