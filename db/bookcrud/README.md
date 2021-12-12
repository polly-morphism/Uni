# Лобораторна робота 3
## Веpзун Поліни км-81

# Book CRUD

Проста CRUD система (Create, Read, Update, Delete) application built on [Django Rest Framework][drf], [Nuxt.js][nuxt] and [Nginx][nginx].

Для продакшену є:

- Automatic HTTPS з Let's Encrypt та [Certbot][certbot].
- Капча.

Юзер може робити:

- CRUD book entries.
- Login and logout.
- Sign up.

## Installation


```bash
cd bookcrud
docker-compose -f local.yml up --build
```

http://127.0.0.1.

![Screenshot](screenshot.png)

## ERD

![ERD](erd.png)

## Deploying

rm `.envs/.production.example` as `.envs/.production` and customize it.

```bash
ssh $YOUR_SERVER
cd bookcrud
docker-compose -f production.yml up --build
```

ТАКОЖ: set `STAGING_ENV` to `False`
