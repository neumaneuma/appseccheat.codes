# appseccheat.codes
A CTF web app designed to teach software developers application security by showcasing what vulnerable code looks like, how to write code to exploit the vulnerability, and how to write code to patch the vulnerability.

## How to run webapp locally
1. Install [docker](https://docs.docker.com/get-docker/) if it is not already installed
1. Run `echo "test" > webapp/dbpwd.txt` if this is your first time running locally (this sets the password for the database to `test`, but you could change this to anything)
1. Run `docker-compose -f docker-compose.dev.yaml up`

## Miscellaneous
* Any changes made to the server code locally will be automatically reloaded in the docker container. Feel free to make changes and play around with the code to help you understand how it works better!
