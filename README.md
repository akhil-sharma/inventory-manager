# inventory-manager

A simple inventory management system individuals.

python=3.11.5

## Running the application

1. **Installation** : `pip intall -r requirements.txt`

2. **Production** : `uvicorn main:app`  | **Development** : uvicorn main:app --reload

## Notes for the Contributers

1. Use the following [guidelines](https://www.conventionalcommits.org/en/v1.0.0-beta.2/#:~:text=Commits%20MUST%20be%20prefixed%20with,bug%20fix%20for%20your%20application.) to structure your commit messages.

2. Personal branches will use the following naming convention:

    NAME = `TYPE_<author>_<topic>`

    TYPE = `fix | feat | chore | docs | style | refactor | test`

**Starting the Database** : `docker run --name db_postgres_inventory_manager -p 5432:5432 -e POSTGRES_PASSWORD=<password> -d postgres`
