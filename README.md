[![Build Status](https://travis-ci.org/MahjongRepository/mahjong-portal.svg?branch=master)](https://travis-ci.org/MahjongRepository/mahjong-portal)

It is working with Python **3.6+** only.

The project is web-application to accumulate, calculate and display russian riichi-mahjong tournaments and ratings.

# Local Docker set up

You need to have installed docker and docker compose.

Steps to run the project:

1. `make build`
2. `make initial_data` (run this command only once, for the initial project setup)
3. `make up`

After these steps you will be able to access website here: http://0.0.0.0:8060/

# Production Docker set up

You need to have installed docker and docker compose.

Copy `.envs/.production.env.example` file and fill it with real data, but don't forget to keep it in secret (at least don't add it to version control system). Assign these env variables to the container with any way that is suits you (there are different options how to do it), and after that you can simply run `make build` and `make up` commands.

The configuration will get SSL certificate automatically, and everything should work out of the box. 

If needed, restore the database backup for the new installation.
