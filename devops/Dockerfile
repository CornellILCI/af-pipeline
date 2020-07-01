FROM ubuntu:20.04
LABEL MAINTAINER = Jack Elendil B. Lagare <j.lagare@irri.org>

ENV TZ=Asia/Manila
ENV EBSAF_ROOT=/home/aadmin/ebs-af
ENV PYSIMBA_ROOT=/home/aadmin/ebs-af/aeo

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y \
    sudo \
    cron \
    postgresql-client \
    libpq-dev \
    r-base \
    libgfortran5 \
    python3.8 \
    python3-pip \
    munge \
    supervisor \
    slurm-wlm \
    && pip3 install psycopg2 gunicorn flask

COPY aeo /home/aadmin/ebs-af/aeo

COPY models /home/aadmin/ebs-af/models

COPY api /home/aadmin/ebs-af/api

# Install R package
RUN Rscript -e "install.packages('/home/aadmin/ebs-af/models/packages/getopt_1.20.2.tar.gz',repos=NULL,type='source')"
RUN Rscript -e "install.packages('/home/aadmin/ebs-af/models/packages/optparse_1.6.1.tar.gz',repos=NULL,type='source')"
RUN Rscript -e "install.packages('/home/aadmin/ebs-af/models/packages/R.methodsS3_1.7.1.tar.gz',repos=NULL,type='source')"
RUN Rscript -e "install.packages('/home/aadmin/ebs-af/models/packages/Rcpp_1.0.0.tar.gz',repos=NULL,type='source')"
RUN Rscript -e "install.packages('/home/aadmin/ebs-af/models/packages/R.oo_1.22.0.tar.gz',repos=NULL,type='source')"
RUN Rscript -e "install.packages('/home/aadmin/ebs-af/models/packages/DiGGer_0.2-31_R_x86_64-unknown-linux-gnu.tar.gz',repos=NULL,type='source')"
RUN Rscript -e "install.packages('/home/aadmin/ebs-af/models/packages/plyr_1.8.4.tar.gz', repos=NULL, type='source')"
RUN Rscript -e "install.packages('/home/aadmin/ebs-af/models/packages/PBTools_2.0.0.tar.gz', repos=NULL, type='source')"

# Create aadmin user
RUN useradd -rm -d /home/aadmin -s /bin/bash -g root \
    -G sudo -u 1000 aadmin -p analyticsAdmin

WORKDIR /home/aadmin

COPY devops/slurm.conf /etc/slurm-llnl/slurm.conf
COPY devops/supervisord.conf /etc/
COPY devops/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

CMD ["/bin/bash"]
