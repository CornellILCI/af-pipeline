import os

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/Users/sb2597/Documents/GitHub/af-core/demos/ap/orchestrator/')
# import file

from flask import (
    Flask,
    render_template
)

from celery import Celery

import endpoints.demo_endpoint as demo

def startApi():

    celery = Celery(broker="amqp://admin:mypass@localhost:5672", backend="rpc://")
    #celery.conf.task_default_queue = 'jobs'

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )


    demo.register(app, celery)

    # If we're running in stand alone mode, run the application
    if __name__ == '__main__':
        app.run(debug=True)


startApi()