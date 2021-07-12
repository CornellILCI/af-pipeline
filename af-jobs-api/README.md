### To Run the API

1. Make sure that you are running the orchestrator
2. On line 19 of api.py, point to the RabbitMQ server.
3. Run API.py

### To run the Demo

Run the API, open a browser and go to localhost:5000/demo (This will execute a GET)

### To add a new endpoint

1. Write a new Enndpoint in the endpoints folder (See: demo_endpoint.py for an example)
2. Add the endpoint to the app in api.py. (example on line 30)


## Submitting Job Requests

### Job Request

A `job request` describes the workflow to be executed by the af-task-orchestrator.  It contains the different parameters that will be used by the tasks the compose the job.  The job request is passed into the AF Jobs API as a `JSON` encoded request body.

The server response will include the `jobId` generated for the job request.  It can be used to track the status of the submitted job via the Get Job Status Endpoint.

### Job Request Parameters

All `job`s have the following mandatory fields:

| Parameter Name | Description | Type | Possible Values |
| -------------- | ----------- | ---- | --------------- |
| `processName`      | Name of the analysis workflow to execute | string | See *list of available workflows* |

### Gather Data Request Parameters

| Parameter Name | Description | Type | Possible Values | Default | Required/Optional |
| -------------- | ----------- | ---- | --------------- | ------- | ----------------- |
| `dataSource` | API Data source | string | `EBS` or `BRAPI` | none | Required |
| `dataSourceId` | API Data source ID | string | Specific datasource ID | none | Required |
| `dataType`  | Data type | string | `PHENOTYPE` or `GENOTYPE` | `PHENOTYPE` | Optional |
| `experimentId` | Experiment ID | string | This maybe the DB identifier of the experiment | | Optional |
| `occurrenceId` | Occurrence ID | string | DB identifier of the occurrence | Optional |
| `traitId` | Trait Id | string | DB identifier of the trait | Optional |
| `apiBearerToken` | Bearer Token to be used to access the data API | | | Required |

The gather_data step will download data depending on the provided parameters.  If `occurrenceId` is provided then plots, plot measurements, and occurence data will be included in the task parameters for use by the next step of the called workflow where `gather_data` is a part of.  If `experimentId` is present then `gather_data` will include Experiment info.  Same would be done for `traitId`.

#### Example Curl Request

```bash
% curl -X POST --header 'Content-Type: application/json' --data '{"processName": "sample_analysis_workflow", "dataSource": "BRAPI", "dataType": "PHENOTYPE", "occurrenceId": "456", "apiBearerToken": "eyShjsdjiweioago485qHaqjaser"} http://locahost:5000

{"status": "ok", "jobId": "e1f24256-46ac-4401-af78-6ae2fdbbcae5"}
```





