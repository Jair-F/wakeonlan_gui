FROM alpine:3.22

RUN apk update && apk upgrade
RUN apk add git
RUN apk add python3 py3-pip py3-flask

RUN mkdir /server
RUN git clone https://github.com/Jair-F/wakeonlan_gui.git /server

WORKDIR /server
EXPOSE 80
CMD [ "/server/deploy_run.sh" ]
