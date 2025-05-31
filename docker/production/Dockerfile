FROM ubuntu:22.04

RUN apt update && apt upgrade -y
RUN apt install -y git bash
RUN apt install -y python3 python3-pip

RUN mkdir /server
RUN git clone https://github.com/Jair-F/wakeonlan_gui.git /server

WORKDIR /server
RUN pip3 install -r requirements.txt
EXPOSE 5001
CMD [ "/server/deploy_run.sh" ]
