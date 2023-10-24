# inventory-manager

A simple inventory management system individuals.

python=3.11.5

## .env

The environment variables need to be set in a .env file which is placed in the root directory.

The structure of the .env file is as follows:

```config
# Database
# Turso Access Details
DATABASE_URL=<url>
AUTH_TOKEN=<token>

# JWT Configuration
SECRET_KEY=<key>
ALGORITHM=<alg>
ACCESS_TOKEN_EXPIRE_MINUTES=<time>
```

NOTE: You can also set the environment variables directly in the shell if you don't want to create the .env file.

## Running the application

1. **Installation** : `pip intall -r requirements.txt`

2. **Production** : `uvicorn main:app`  | **Development** : `uvicorn main:app --reload`

## Notes for the Contributers

1. Use the following [guidelines](https://www.conventionalcommits.org/en/v1.0.0-beta.2/#:~:text=Commits%20MUST%20be%20prefixed%20with,bug%20fix%20for%20your%20application.) to structure your commit messages.

2. Personal branches will use the following naming convention:

    NAME = `TYPE_<author>_<topic>`

    TYPE = `fix | feat | chore | docs | style | refactor | test`

