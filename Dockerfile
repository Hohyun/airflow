FROM apache/airflow:3.0.3

ENV AIRFLOW_VERSION=3.0.3

USER root

RUN apt-get update \
  && apt-get install -y vim

USER airflow

RUN curl https://dl.min.io/client/mc/release/linux-amd64/mc -o $HOME/mc \
  && chmod +x $HOME/mc

ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt
