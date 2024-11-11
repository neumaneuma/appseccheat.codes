# appseccheat.codes

A CTF web app designed to teach software developers application security by showcasing what vulnerable code looks like, how to write code to exploit the vulnerability, and how to write code to patch the vulnerability.

## How to run webapp locally

### Running for the first time

1. Install [docker](https://docs.docker.com/get-docker/) if it is not already installed.
2. Run `docker compose -f docker-compose.yaml up --build`. Be sure to wait enough time before running the next command to allow time for the application to start up, especially on first run. The presence of this log line indicates the database is ready:

```
db_1   | 2021-03-22T22:37:00.973213Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.0.23'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
```

### Running subsequent times

1. Run `docker compose -f docker-compose.dev.yaml up --build`
2. The web server is now accessible at [`127.0.0.1:12300`](http://127.0.0.1:12300)

## Miscellaneous

- Any changes made to the server code locally will be automatically reloaded in the docker container. Feel free to make changes and play around with the code to help you understand how it works better!
- Run `docker exec -it appseccheatcodes-db-1 psql --dbname=postgres --username=postgres` to open a shell that accesses the database. The password will be `postgres`.
  - `docker exec -it` opens an interactive terminal for a container
  - `appseccheatcodes-db-1` is the name of the database container
  - `psql --dbname=postgres --username=postgres` is the command to run within the interactive terminal

## Setting up dev environment

- To run functional tests: `DEV_MODE=true python3 -m backend.tests.driver`

TODO:

- vue3
  - ssrf lfi challenge should be radio button ui for selecting the url
- updated css
- ssrf1
- ssrf2
- docker race condition after deleting all containers
- have exploits send flags to stdout or something, and pipe it to functional test somehow to be able to test in prod
- make sqli2 username dynamic to avoid any potential race conditions. will require a post endpoint to generate the username that vue calls, should also populate the db with the new username
- is my impl of db login vulnerable to timing attacks?
- why doesn't bcrypt work? probably have to use BlobField? https://docs.peewee-orm.com/en/latest/peewee/models.html#field-types-table
- cors light
