FROM python:3.9-slim-buster
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1
ENV LOG_LEVEL info
ENV PYTHONPATH "${PYTHONPATH}:/app/"
WORKDIR /app/
COPY . /app/

# RUN apt-get update && pip3 install  -r requirements.txt
RUN pip3 install  -r requirements.txt

# Install ASReml-4.2.1.158-Ubuntu-18.04
RUN apt-get update  \
  && apt-get install -y wget \
  && wget https://downloads.vsni.digital/2bdb06398e7dcf7d9a638092305b5b78fdffacb1/ASReml-4.2.1.170-Ubuntu-18.04.deb \
  && apt-get install -y ./ASReml-4.2.1.170-Ubuntu-18.04.deb \
  && apt-get install -y supervisor

ENTRYPOINT [ "./start-worker.sh" ]

