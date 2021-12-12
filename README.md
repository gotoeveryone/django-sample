# django-sample

![Build Status](https://github.com/gotoeveryone/django-sample/workflows/Build/badge.svg)

## Requirements

- Docker

## Setup

```console
$ cp .env.example .env
```

## Run

```console
$ docker-compose up
```

## Migration

```console
$ docker-compose exec app pipenv run manage makemigrations # make migrations
$ docker-compose exec app pipenv run manage migrate
```

## Create administrator

```console
$ docker-compose exec app pipenv run manage createsuperuser
```
