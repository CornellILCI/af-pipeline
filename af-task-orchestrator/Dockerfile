FROM python:3.9-slim-buster
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1
ENV LOG_LEVEL info
ENV PYTHONPATH "${PYTHONPATH}:/app/"
WORKDIR /app/
COPY . /app/

#
RUN apt-get update 
RUN apt-get install -y dirmngr gnupg apt-transport-https ca-certificates software-properties-common
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-key '95C0FAF38DB3CCAD0C080A7BDC78B2DDEABC47B7'
RUN add-apt-repository 'deb http://cloud.r-project.org/bin/linux/debian buster-cran40/'

## Install ASReml-4.2.1.158-Ubuntu-18.04, R, supervisor
RUN apt-get update
RUN apt-get install -y wget
RUN wget https://downloads.vsni.digital/2bdb06398e7dcf7d9a638092305b5b78fdffacb1/ASReml-4.2.1.170-Ubuntu-18.04.deb
RUN apt-get install -y ./ASReml-4.2.1.170-Ubuntu-18.04.deb
RUN apt-get install -y supervisor

#ENV PATH="/app/scripts:${PATH}"

# Install ASREML-R
RUN apt install -y -t buster-cran40
RUN apt-get install -y -f r-base

# install R packages
RUN Rscript -e  "install.packages('sommer')"
RUN Rscript -e  "install.packages('RJSONIO')"
RUN Rscript -e  "install.packages('gtools')"

# RUN apt-get update && pip3 install  -r requirements.txt
RUN pip3 install --upgrade setuptools
RUN pip3 install  -r requirements.txt

ENTRYPOINT [ "./start-worker.sh" ]

