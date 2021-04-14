from flask import Flask, request
from flask_restful import Resource, Api

# from orchestrator.routes.example_route.tasks import sample_route as example_route

# from orchestrator.tasks.data_gathering.tasks import sample_data_gathering_task
# from orchestrator.tasks.workflow.tasks import sample_aggregator_task
# from orchestrator.tasks.calculation.tasks import sample_calculation_task
# from orchestrator.tasks.data_upload.tasks import sample_data_upload_task


def register(app, celery):

    api = Api(app)

    todos = {}

    class Demo(Resource):
        def get(self):
            print("GET RECIEVED")

            celery.signature(
                "sample_route", queue="jobs", kwargs={"jobId": "someid", "jobName": "sample_workflow"}
            ).delay()
            return {"response": "GET RECIEVED"}

        def put(self):
            return {"response": "PUT RECIEVED"}

        def post(self):
            return {"response": "POST RECIEVED"}

    api.add_resource(Demo, "/demo")
