FROM python:3.7 AS builder
LABEL organization="stageai"
RUN apt-get update && apt-get install -y \
	build-essential ca-certificates git postgresql-client make gcc g++ \
	python3-numpy python3-scipy
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /tmp/requirements.txt
RUN pip wheel -i https://jenkins.stageai.tech/devpi/root/pypi/+simple/ -r /tmp/requirements.txt


FROM python:3.7
RUN apt-get update && apt-get install -y postgresql-client
RUN useradd -m app && mkdir -p /home/app/src/coronavirus
COPY --from=builder /usr/src/app /wheels
RUN pip install gunicorn && pip install --no-cache /wheels/*
ENV APP_PATH /home/app/src/coronavirus
COPY . $APP_PATH
RUN cp $APP_PATH/docker/local_settings.py $APP_PATH/coronavirus/local_settings.py
RUN cp $APP_PATH/docker/entrypoint.sh /bin/coronavirus
WORKDIR $APP_PATH
RUN python setup.py install
RUN chown -R app:app $APP_PATH
EXPOSE 8000
USER app
ENTRYPOINT ["/bin/coronavirus"]
