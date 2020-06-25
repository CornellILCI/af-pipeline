README for devops folder
3 June 2020

This is the directory for devops.

## Building the Docker image for EBS AF AEO

1. Copy slurm.tmpl to slurm.conf.
``` bash
cp slurm.tmpl slurm.conf
```

2. Open slurm.conf and modify as necessary. 

3. Copy supervisord.tmpl to supervisord.tmpl.
```bash
cp supervisord.tmpl supervisord.tmpl
```

4. At the root of the `ebs-af` project, run the command:

``` bash
docker build -t {IMAGE_NAME}:{IMAGE_TAG} -f devops/Dockerfile .
```  
