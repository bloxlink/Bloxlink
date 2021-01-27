# Bloxlink
Roblox Verification made easy! Features everything you need to integrate your Discord server with Roblox.

## Dependencies
  - Python 3.5+ (satisfied if using our Docker Compose file)
  - [Docker](https://www.docker.com/)
  - [Docker Compose](https://docs.docker.com/compose/)
  - [RethinkDB](https://rethinkdb.com/) (satisfied if using our Docker Compose file)
  - [Redis](https://redis.io) (satisfied if using our Docker Compose file)
  - [Requirements file](https://github.com/bloxlink/Bloxlink/blob/master/requirements.txt) (satisfied if using our Dockerfile)

## Configuration
  ### Configuration files
  Edit the [config.py](https://github.com/bloxlink/Bloxlink/blob/master/src/config.py) file. Some values, the "secrets" or "tokens", can be optionally saved as environmental variables instead.
  Save your environmental variables in [docker-compose.yml](https://github.com/bloxlink/Bloxlink/blob/master/docker-compose.yml) if you choose not to save the secrets in the config file.
  Valid secrets which can be saved as environmental variables are found in the [secrets.py](https://github.com/bloxlink/Bloxlink/blob/master/src/resources/secrets.py) file.

  Environmental variables have priority over the config file!

  ### Constants
  Some options which aren't required to be changed are in the [constants.py](https://github.com/bloxlink/Bloxlink/blob/master/src/resources/constants.py) file.

## Intents
The **Members Privileged Intent** is required for the bot to function. This can be toggled on your [Developer Dashboard](https://discord.com/developers/applications) unless your bot reached over 100 servers.

## Quick Setup
```sh
$ git clone https://github.com/bloxlink/Bloxlink
$ cd Bloxlink
$ docker-compose up --build
```

## Disclaimer
We do not provide support for self-hosting! This package has been made open-source to aid with contributions, not so you can run your own Bloxlink for private use. If something breaks or there's a vulnerability in a version you use, then you're on your own.

For this reason, we recommend using the official hosted bot at https://blox.link which is given regular updates.

Also, keep in mind that we use the AGPL-3.0 License, which means you're required to keep your local version open-source and state all changes that you have made to it.
# ISoDEVerifySystem
