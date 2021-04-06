WORKFLOW_REGISTRY = dict()


def register(name, func):
    print(f"Registering workflow {name} to func:{func.__name__}")
    WORKFLOW_REGISTRY[name] = func
