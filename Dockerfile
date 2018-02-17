FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /project
WORKDIR /project
RUN mkdir static logs
VOLUME ["/project/logs/"]

ADD requirements.txt /project/

RUN pip install gunicorn
RUN pip install -r requirements.txt

ADD . /project/
EXPOSE 8000

COPY ./docker_entrypoint.sh /
ENTRYPOINT ["/docker_entrypoint.sh"]
