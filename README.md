# appseccheat.codes
A CTF web app designed to teach software developers application security by showcasing what vulnerable code looks like, how to write code to exploit the vulnerability, and how to write code to patch the vulnerability.

## How to run webapp locally
### Running for the first time
1. Install [docker](https://docs.docker.com/get-docker/) if it is not already installed.
2. Run `docker compose -f docker-compose.dev.yaml up --build`. Be sure to wait enough time before running the next command to allow time for the application to start up, especially on first run. The presence of this log line indicates the database is ready:
```
db_1   | 2021-03-22T22:37:00.973213Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.0.23'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
```
3. From another tab in your terminal, run `docker exec -it appseccheatcodes_web_1 flask db initialize` to initialize the database. This also has the effect of resetting the database if you want to do that in the future.
4. The web server is now accessible at [`127.0.0.1:5000`](http://127.0.0.1:5000)

### Running subsequent times
1. Run `docker compose -f docker-compose.dev.yaml up --build`
2. The web server is now accessible at [`127.0.0.1:5000`](http://127.0.0.1:5000)

## Miscellaneous
* Any changes made to the server code locally will be automatically reloaded in the docker container. Feel free to make changes and play around with the code to help you understand how it works better!
* Run `docker exec -it appseccheatcodes_db_1 mysql -p appsecdb` to open a shell that accesses the database. The password will be `test`.
  * `docker exec -it` opens an interactive terminal for a container
  * `appseccheatcodes_db_1` is the name of the database container
  * `mysql -p appsecdb` is the command to run within the interactive terminal (`appsecdb` is the name of the database)
