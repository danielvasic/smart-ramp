FROM ubuntu:18.04
LABEL org.opencontainers.image.source https://github.com/University-of-Mostar/smart-ramp
ENV TZ=Europe/Zagreb

RUN export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN export DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=0
RUN apt update
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
RUN apt install -y build-essential apt-utils curl openvpn ffmpeg libsm6 libxext6 xmlsec1 libmysqlclient-dev
RUN apt install -y libopencv-dev libtesseract-dev git cmake build-essential libleptonica-dev
RUN apt install -y liblog4cplus-dev libcurl3-dev openalpr

RUN export TESSDATA_PREFIX=/usr/share/openalpr/runtime_data/ocr/tessdata/
RUN apt install -y python3.7 python3.7-dev python3.7-distutils
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1

RUN curl https://bootstrap.pypa.io/pip/3.5/get-pip.py --output get-pip.py
RUN python get-pip.py

RUN pip3 install opencv-python
RUN pip3 install flask
RUN pip3 install flask_cors
RUN pip3 install pysaml2
RUN pip3 install flask_sqlalchemy
RUN pip3 install flask_migrate
RUN pip3 install mysqlclient
RUN pip3 install gunicorn
RUN pip3 install flask_login

RUN mkdir -p /var/log/flask-ramp
RUN mkdir -p /app/smartramp/

RUN mkdir -p /dev/net && \
    mknod /dev/net/tun c 10 200 && \
    chmod 600 /dev/net/tun

RUN cp -a /usr/share/openalpr/runtime_data/ocr/tessdata/*.traineddata /usr/share/openalpr/runtime_data/ocr/

COPY ./ /app/smartramp/
WORKDIR /app/smartramp/
RUN chmod +x run.sh

ENTRYPOINT [ "./run.sh" ]