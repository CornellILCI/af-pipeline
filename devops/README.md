README for devops folder
3 June 2020

This is the directory for devops.

## Building the Docker image for EBS AF AEO

At the root of the `ebs-af` project, run the command:

``` bash
docker build -t {IMAGE_NAME}:{IMAGE_TAG} -f devops/Dockerfile .
```  
