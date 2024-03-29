#author: Kevin Palis <kdp44@cornell.edu>

FROM ubuntu:18.04
#update and install utility packages
RUN apt-get update -y && apt-get install -y \
 gnupg2 \
 wget \
 sudo \
 software-properties-common
EXPOSE 22 5432


#copy the entrypoint/config file and make sure it can execute
COPY config.sh /root
RUN chmod 755 /root/config.sh

#install Java so we can run liquibase
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0xB1998361219BD9C9 && \
apt-add-repository 'deb http://repos.azulsystems.com/ubuntu stable main' && \
apt install -y zulu-13

#Create the file repository configuration
#Import the repository signing key
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
apt-get -y update

#Install Postgresql13
RUN apt-get -y update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
postgresql-13 \
postgresql-client-13 

#set all environment variables needed to initialize the database - these can all be overriden during container run
ENV postgres_local_auth_method=md5
ENV postgres_host_auth_method=md5
ENV postgres_listen_address=*
ENV db_user=ebsuser
ENV db_pass=3nt3rpr1SE!
ENV db_name=ba_db
ENV pg_driver=postgresql-42.2.10.jar
ENV lq_contexts=schema,template
ENV lq_labels=clean
ENV default_statistics_target=100
ENV random_page_cost=1.1
ENV effective_cache_size=32GB
ENV max_parallel_workers_per_gather=4
ENV max_parallel_workers=10

COPY build build


ENTRYPOINT ["/root/config.sh"]
