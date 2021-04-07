### To Run the API

1. Make sure that you are running the orchestrator
2. On line 19 of api.py, point to the RabbitMQ server.
3. Run API.py

### To run the Demo

Run the API, open a browser and go to localhost:5000/demo (This will execute a GET)

### To add a new endpoint

1. Write a new Enndpoint in the endpoints folder (See: demo_endpoint.py for an example)
2. Add the endpoint to the app in api.py. (example on line 30)