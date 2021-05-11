
![Alt text](https://thumbnails-photos.amazon.com/v1/thumbnail/jlO5R-FlQi2jc7XIDi0WIw?viewBox=1153%2C328&ownerId=A3RL6H4CGV9EDF&groupShareToken=BMjypj3yTjKYQZeEzFAEUw.WzZF0j057nuvZB9AjXgh1l "EBS Project")

# Breeding Analytics Database

This is the database module of the Breeding Analytics Applications. You'll find all the database scripts and binaries in this repository.

This project has been fully containerized. The commands to help you use this container is outlined below. When you run the container, the following will be done for you:

1. Ubuntu base image with utility tools installed
2. Postgres 13 installed and configured
3. Database engine tuned to run in a modest server
4. Database user created based on the passed variable or created from the default
5. Database created based on the passed variable or created from the default
6. Liquibase migration against the created database - effectively giving you the latest BA schema. Note that you can override the default contexts if you need fixture data, etc.

## Contents of this repository

#### Liquibase in EBS

There are too many ways you can use Liquibase for database versioning and change control, we have put up a [guideline across EBS as to how a database project should be structured](https://ebsproject.atlassian.net/wiki/spaces/DB/pages/29006528708/EBS+Database+Project+Structure). If you are contributing to this repository, it is imperative that you read the linked document and conform to the standards we've put in place.

#### Dockerfile and config.sh
Contains all the containerization steps. The config.sh is the entrypoint and you'll find all the database provisioning in there.

#### Build/liquibase directory
Contains all the liquibase scripts and binaries.

#### Build/util
Contains all utility scripts to make automation easier


## Using this container

Usage can be classified into two types: database development and general usage. The following environment variables/parameters are available (shown below with their respective default values) and can be set during `docker run` invocation or overriden via environment variables on docker compose or swarm:

```bash
postgres_local_auth_method=trust
postgres_host_auth_method=trust
postgres_listen_address=*
db_user=ebsuser
db_pass=3nt3rpr1SE!
db_name=ba_db
pg_driver=postgresql-42.2.10.jar
lq_contexts=schema,template
lq_labels=clean
default_statistics_target=100
random_page_cost=1.1
effective_cache_size=32GB
max_parallel_workers_per_gather=4
max_parallel_workers=10
```

### Docker Compose Alternative

Aka "I don't want to learn Docker right now" alternative. In case you just want to get a DB container with all the defaults and don't want to deal with all the docker commands mentioned below, this one's for you. Go into the `deploy` directory:

* To start the ba-db container/service:
```bash
docker compose -f ba-db.yml up -d
```
* To stop the ba-db container/service
```bash
docker compose -f ba-db.yml down
```


### Database Development

As mentioned above, the container will set up and configure everything you need. So you can focus on just writing SQL or database scripts. As long as they are in the build directory, the container will pick it up.

**Steps**


* Make sure your repository is up to date with remote (ie. `git pull --all`)
* Write your code, ex. for liquibase, make sure the SQL files are in build/liquibase/changesets directory and specified in a changelog XML (see [Database Management Guideline](https://ebsproject.atlassian.net/wiki/spaces/DB/pages/104235022/Database+Change+Management))
* Build the image. Make sure you are in the root directory of this repository, then run

```bash  
docker build --force-rm=true -t ba-db .
```

* If the build succeeds, you should now have the docker image locally. You can then start and initialize the container. You have two options depending on wether or not you want the database data to persist. Change variable values as you see fit (-v).
	* Persist data across docker runs: 
	```bash 
	docker run --detach --name ba-db -h ba-db -p 5433:5432 --health-cmd="pg_isready -U postgres || exit 1" -e "db_name=ba_db" -e "db_user=ebsuser" -e "lq_contexts=schema,template,fixture" -e "lq_labels=clean,develop" -v ba_postgres_etc:/etc/postgresql -v ba_postgres_log:/var/log/postgresql -v ba_postgres_lib:/var/lib/postgresql -it ba-db:latest
	```
	* Do not persist data (whenever container is removed via `docker rm`, the data goes away with it): 
	```bash
	docker run --detach --name ba-db -h ba-db -p 5433:5432 --health-cmd="pg_isready -U postgres || exit 1" -e "db_name=ba_db" -e "db_user=ebsuser" -e "lq_contexts=schema,template,fixture" -e "lq_labels=clean,develop" -it ba-db:latest
	```

* Wait a minute or two. Feel free to check the status of the schema migration via `docker logs ba-db`.
* You now have a running Postgres 13 on port 5433 with all the latest changes. You can either connect to it to port 5433 from outside the container, or go inside the container and check via psql

```bash
docker exec -ti ba-db bash
su - postgres
psql
```

* Lastly, you have the option to either **keep the container running** as long as you're making your database changes, then invoking liquibase within the container to test. This way you save time by not having to rebuild the image everytime. Once you are happy with your work, push your liquibase changesets to this repository.

>Note that the example commands above creates a schema with fixture data. If you don't want that, modify the liquibase context being passed, ie. remove the `fixture` context

### General Usage

Typically, for general usage, you do not need to modify any database scripts or add new SQL. So the steps are simpler. You don't even need to pull this repository.

#### Get the official docker image from **EBSProject Dockerhub**

> The official nightly build tag is **dev**. Release images are tagged according to version numbers. Check the Dockerhub Repository for current tags. [BA-DB Dockerhub](https://hub.docker.com/r/ebsproject/ba-db)

**Steps**


* Run the container. You have two options depending on wether or not you want the database data to persist.

* Persist data across docker runs:
```bash
docker run --detach --name ba-db -h ba-db -p 5433:5432 --health-cmd="pg_isready -U postgres || exit 1" -e "db_name=ba_db" -e "db_user=ebsuser" -e "lq_contexts=schema,template,fixture" -e "lq_labels=clean,develop" -v ba_postgres_etc:/etc/postgresql -v ba_postgres_log:/var/log/postgresql -v ba_postgres_lib:/var/lib/postgresql -it ebsproject/ba-db:dev
```
* Do not persist data (whenever container is removed via `docker rm`, the data goes away with it): 
```bash
docker run --detach --name ba-db -h ba-db -p 5433:5432 --health-cmd="pg_isready -U postgres || exit 1" -e "db_name=ba_db" -e "db_user=ebsuser" -e "lq_contexts=schema,template,fixture" -e "lq_labels=clean,develop" -it ebsproject/ba-db:dev
```
* Wait a minute or two. Feel free to check the status of the schema migration via `docker logs ba-db`.

* You now have a running Postgres 13 on port 5433 with all the latest changes. You can either connect to it to port 5433 from outside the container, or go inside the container and check via psql

```bash
docker exec -ti ba-db bash
su - postgres
psql
```

> The example commands above will create the container off of the nightly build (tag=dev). Change the tag as needed.

