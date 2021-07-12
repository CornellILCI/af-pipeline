# Developer Guide


## Generic Python Development Process (PROPOSED)

1.  Create a Python Virtual Environment for the project in your development environment.

2.  Manage the project repo using git.

3.  Install the component/application requirements using pip/pip3.

4.  Testing and Code Coverage

```bash
    $ cd /path/to/component_or_app

    $ coverage run -m pytest

    $ coverage report -m

```


    We can generate an HTML formatted report of the code coverage:


```bash
    $ coverage html
```


    ...which will generate a `htmlcov` folder containing the coverage report in web page format.  Open `index.html` to view in a web browser.

5.  Linting (Using Flakehell)

We recommend using flakehell (with flake8 plugins) to do code linting.

```bash
$ cd /path/to/component_or_app

$ flakehell lint .

```

For code formatting run isort and black:

```bash

$ isort .

$ black .

```



## AF Task Orchestrator

### Development Environment Setup

1. Install Python 3 <VERSIONHERE>.  Download python from [python.org](https://python.org/downloads) or via the package manager of your development environment.

2. Setup your python virtual environment.  Virtual environments are a good way to manage packages, creating one virtual environment per project.  For AF Task Orchestrator, we will be naming the virtual environment `ebs-afto`, but you can follow/use your own naming system for virtual environments.  Take note that this will create a directory in where you want to store your virtual environments.  In this example we are creating a `venvs` directory where we can store any virtual environment.


```bash
$ mkdir venvs

$ python3 -m venv venvs/ebs-afto

```

Activate the virtual environment (for Linux/MacOSX):

```bash
$ source venvs/ebs-afto/bin/activate
```

Your prompt should include the name of the activated virtual environment:

```bash
(ebs-afto) $ 
```

3.  Get the project repo via Git.

4.  Install the project requirements:

```bash
(ebs-afto) $ cd /path/to/af-core/
(ebs-afto) $ cd pip3 install -r requirements-dev-af-task-orch.txt
```

This will install project dependencies as well as dev tools for linting, testing and etc.

