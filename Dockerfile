FROM python:3.9.6

ENV TZ Asia/Tokyo

ENV APP_ROOT /var/app/
WORKDIR $APP_ROOT

COPY Pipfile $APP_ROOT
COPY Pipfile.lock $APP_ROOT

RUN pip install --upgrade pip && \
  pip install pipenv && \
  pipenv sync -d
