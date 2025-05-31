FROM alpine:3.22

RUN apk update && apk upgrade
RUN apk add git bash
RUN apk add python3 py3-pip py3-flask

RUN mkdir /server
RUN git clone https://github.com/Jair-F/wakeonlan_gui.git /server

WORKDIR /server
EXPOSE 80
ENTRYPOINT [ "/server/deploy_run.sh" ]
