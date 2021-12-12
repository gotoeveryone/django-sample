# django-sample

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
$ docker-compose exec backend pipenv run manage makemigrations # make migrations
$ docker-compose exec backend pipenv run manage migrate
```

## Create administrator

```console
$ docker-compose exec backend pipenv run manage createsuperuser
```
