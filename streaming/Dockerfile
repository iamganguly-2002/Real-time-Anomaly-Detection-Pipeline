FROM apache/spark:3.4.0

USER root

RUN apt-get update && apt-get install -y python3-pip

COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

COPY . /app/

WORKDIR /app

CMD ["python3", "streaming_job.py"]