# syntax = docker/dockerfile:1.3-labs
FROM ubuntu:20.04
LABEL MAINTAINER = Jack Elendil B. Lagare <j.lagare@irri.org>

ENV TZ=Asia/Manila
ENV EBSAF_ROOT=/home/aadmin/ebs-af
ENV PYSIMBA_ROOT=/home/aadmin/ebs-af/aeo

RUN <<EOF

## Change local timezone
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

## Add repository for R 4.x
apt-get update && apt-get install -y software-properties-common
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/'

## Install dependencies
apt-get update

apt-get install -y sudo cron postgresql-client libpq-dev r-base libgfortran5 python3.8 python3-pip \
    munge \
    supervisor \
    slurm-wlm \
    curl \
    uuid

apt-get update

## Install Python libraries
pip3 install psycopg2 gunicorn flask

EOF

COPY aeo /home/aadmin/ebs-af/aeo
COPY statistical_models /home/aadmin/ebs-af/models
COPY api /home/aadmin/ebs-af/api

RUN <<EOF

# Install R packages
Rscript -e "install.packages('optparse')"
Rscript -e "install.packages('R.oo')"
Rscript -e "install.packages('dplyr')"
Rscript -e "install.packages('crayon')"
Rscript -e "install.packages('Rdpack')"
Rscript -e "install.packages('/home/aadmin/ebs-af/models/packages/DiGGer_1.0.5_R_x86_64-redhat-linux-gnu.tar.gz', repos=NULL, type='source')"
Rscript -e "install.packages('/home/aadmin/ebs-af/models/packages/PBToolsDesign_2.1.0-21.07.09.tar.gz', repos=NULL, type='source')"
Rscript -e "install.packages('/home/aadmin/ebs-af/models/packages/ebsRtools_0.2.0.tar.gz', repos=NULL, type='source')"


# Add crontab entry for cleaner.py
echo "0 23 * * 6 /home/aadmin/ebs-af/aeo/bin/cleaner.py" >> /etc/crontab

# Create aadmin user
useradd -rm -d /home/aadmin -s /bin/bash -g root \
    -G sudo -u 1000 aadmin -p analyticsAdmin


EOF

WORKDIR /home/aadmin

COPY devops/slurm.tmpl /etc/slurm-llnl/slurm.conf
COPY devops/supervisord.tmpl /etc/supervisord.conf
COPY devops/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

CMD ["/bin/bash"]
