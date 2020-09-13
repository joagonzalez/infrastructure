# VERSION 1.10.9
# AUTHOR: Joaquin Gonzalez
# DESCRIPTION: Basic Airflow container
# BUILD: docker build --rm -t newcos-airflow:1.0.0 harbor-01.newtech.com.ar/newcos-automation/newcos-airflow:1.10.9 .
# SOURCE: https://github.com/newtech-sm/newcos-airflow
# Support for TextFSM, InfluxDB writing, ansible in workers

FROM puckel/docker-airflow:1.10.9
LABEL maintainer="newtech"

# Airflow
ARG AIRFLOW_VERSION=1.10.9
ARG AIRFLOW_USER_HOME=/usr/local/airflow
ARG AIRFLOW_DEPS=""
ARG PYTHON_DEPS=""
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

# Define en_US.
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

# Disable noisy "Handling signal" log messages:
# ENV GUNICORN_CMD_ARGS --log-level WARNING

USER root
RUN apt update
RUN apt install -y ansible iputils-ping
RUN pip install pymsteams==0.1.12
RUN pip install uuid==1.30
RUN pip install --user textfsm
RUN pip install textfsm

COPY script/entrypoint.sh /entrypoint.sh
COPY config/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg

RUN chown -R airflow: ${AIRFLOW_USER_HOME}

EXPOSE 8080 5555 8793

USER airflow
WORKDIR ${AIRFLOW_USER_HOME}
ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]