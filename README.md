# React Practice

## Setup
Create a `docker-compose.env.yml` file as below.

```
services:

  postgres:
    environment:
      POSTGRES_PASSWORD: deadbeef

  backend:
    environment:
      AUTH_SALT: deadbeef
```

## Start Dev Server
```
docker compose up
```

## Develop

### Add npm package
```
docker compose exec frontend npm install <package>
```