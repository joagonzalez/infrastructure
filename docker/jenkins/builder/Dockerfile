FROM python:3.7.5

USER root
RUN apt update \
      && apt update --fix-missing \
      && apt install sshpass -y \
      && apt install ansible -y \
      && rm -rf /var/lib/apt/lists/*

RUN pip install pymsteams
RUN pip install requests