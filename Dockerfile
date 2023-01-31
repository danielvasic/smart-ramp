FROM ubuntu:18.04
LABEL org.opencontainers.image.source https://github.com/University-of-Mostar/smart-ramp
ENV TZ=Europe/Zagreb

RUN export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN export DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=0
RUN apt-get update
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata

RUN apt-get install -y python3.7 python3.7-dev python3.7-distutils python3-setuptools python3-pip default-libmysqlclient-dev libxmlsec1 libxmlsec1-dev xmlsec1 build-essential

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1

RUN pip3 install --upgrade pip wheel setuptools
RUN pip3 install xmlsec
RUN pip3 install mysqlclient
RUN pip3 install flask
RUN pip3 install flask_cors
RUN pip3 install pysaml2
RUN pip3 install flask_sqlalchemy
RUN pip3 install flask_migrate
RUN pip3 install gunicorn
RUN pip3 install flask_login

RUN mkdir -p /var/log/flask-ramp
RUN mkdir -p /app/smartramp/

COPY ./ /app/smartramp/
WORKDIR /app/smartramp/
RUN chmod +x run.sh

ENTRYPOINT [ "./run.sh" ]
