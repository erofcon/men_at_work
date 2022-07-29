FROM python:3.9

ARG OPENCV_VERSION=4.5.3


WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update \
    && apt-get install ffmpeg libsm6 libxext6  -y  \
    && apt-get install -y netcat  \
    && pip install  --upgrade pip

COPY req.txt .

RUN pip install -r req.txt

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]