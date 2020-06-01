Singularity container Definition
========

Files
--------

- R - Wrapper to invoque R within the container

- R-3.4.4-ubuntu-xenial-ebs.def - Definition file for singularity container.

Dependences
--------

- ebs-af repository on /opt/


Usage
--------

- Singularity image creation

# singularity build /tmp/R-3.4.4-ubuntu-xenial-ebs.sif /opt/ebs-af/models/singularity/R-3.4.4-ubuntu-xenial-ebs.def

- Move the sif file to destination folder and copy the wrapper




