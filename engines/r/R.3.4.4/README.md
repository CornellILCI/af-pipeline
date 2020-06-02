R 3.4.4 Singularity Container
========

Dependences
--------
- Singularity >= 3.0
  - See installation instructions [singularity user guide] (]https://sylabs.io/guides/3.5/admin-guide/installation.html#installation-on-linux)
- ebs-af repository on /opt/ 
  - if repository is in other location, modify the %files section of the definition file

Files
--------

- R - Wrapper to invoque R within the container

- R-3.4.4-ubuntu-xenial-ebs.def - Definition file for singularity container.


Usage
--------

- Singularity image creation
  - See more information how to build: [singularity docs] (https://sylabs.io/guides/3.5/user-guide/build_a_container.html#building-containers-from-singularity-definition-files)
  ```console
   # singularity build<container name>.sif <definition file>
   #
   # singularity build R-3.4.4-ubuntu-xenial-ebs.sif R-3.4.4-ubuntu-xenial-ebs.def
  ```
- Wrapper file has to be on same directory of the singularity container image

- running container
  - use the wrapper to invoque R whitin the container 
  ```console
  $ R CMD BATCH </path to script>.R 
  ```
  - use singularity exec command
  ```console
  singularity exec <singularity containder> <command inside container>
  ```


