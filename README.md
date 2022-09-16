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