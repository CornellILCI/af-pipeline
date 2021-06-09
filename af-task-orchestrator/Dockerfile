FROM python:3.9-slim-buster
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1
ENV LOG_LEVEL info
ENV PYTHONPATH "${PYTHONPATH}:/app/"
WORKDIR /app/
COPY . /app/

# Copy asreml license file 
COPY ./licenses/EiB.lic /home/asreml/licenses/asreml.lic
# RUN apt-get update && pip3 install  -r requirements.txt
RUN pip3 install  -r requirements.txt
ENTRYPOINT [ "./start-worker.sh" ]

