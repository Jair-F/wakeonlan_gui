FROM alpine:3.22
USER root

RUN apk update && apk upgrade
RUN apk add git bash
RUN apk add python3 py3-pip

RUN mkdir /server
RUN git clone https://github.com/Jair-F/wakeonlan_gui.git /server

WORKDIR /server
RUN pip3 install --break-system-packages -r requirements.txt
EXPOSE 5001
ENTRYPOINT [ "/server/deploy_run.sh" ]
