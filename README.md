This project is test task for compeny othercode.

Solution is API built with framework FastAPI.

Required python is 3.11

Project can be deployed in two ways:

1. In docker
2. For development

In both cases first should be done some preparations:

### Private and public keys for correct work of JWT encdoding

create folder **certs** in root directory of the project and generate private key with command:

```shell
openssl genrsa -out private.pem 2048
```

and then generate public key with command:

```shell
openssl rsa -in private.pem -outform PEM -pubout -out public.pem
```

both keys should be located in **certs** folder (should be created manually) in root directory of the project.

### Environment variables

If you run project in development mode, **.env** file in root directory of folder should be created, example of content provided in example.env file

And for docker should be created **docker.env** file, example of content provided in example.docker.env

All previous operations are enough to run project with docker with command from project directory:

```shell
docker-compose up
```

to run project in development mode some preparations still should be done

### Database

To run project in development mode should be created database with name described in .env file.

for example:

```shell
psql
```

```shell
create database otherblog;
```

### Virtual env

Create virtual env

```shell
python -m venv env
```

Activate virtual enviroment and install required packets

```shell
pip install -r requirements.txt
```

### Database migrations and fixtures

To execute migrations, run from project folder:

```shell
alembic upgrade head
```

There is examples of roles and permissions which should be loaded
in database with command:

```shell
python loadfixtures.py
```

At this point it should be enough to run project in development mode.

Just run from root directory of the project

```shell
uvicorn src.main:app --reload
```

## Important notes

### Docs

Api swagger docs located on address /api/docs

### RBAC

As example there are 4 available roles for users: admin, user, moderator, anonimus. Their permissions are described in json files in directory fixtures.

By default any registered user has permission user, Only admins can change assign user to a new role including admin.

To create first admin there is command which should be executed from root directory of the project or from workdir of the docker app container:

```shell
python add_user_to_role.py -e=<user_email> -r=admin
```

### Post filtering

To filter post there is possibility to pass base_filter parameter. This parameter
is stringified JSON. It allows to filter through joining of related table (In our case it's filtering Posts by author - User)

so to filter can be passed query parameter base_filter:

```
{
    "author__firstname": "Admin",
    "author__lastname": "Admin",
    "name": "Post name",
    "created_at__lt": "2024-01-06T20:19:32.757948"
}
```

all filters will add to request joins and where sql expressions. If key filter
marked with \_\_ (two underscores), app undersntands that table should be joined before filtering.

To filter by datetime of post creation datetime should be passed in format: %Y-%m-%dT%H:%M:%S.%f (see example above).

### Demo data

In the project there is script which can insert some data with some users and posts created only for demo purposes. It already has 3 users for each role (role anonimus is selected when user is not authorized in api).

login: aadmin@example.com  
password: AAdmin

login: uuser@example.com  
password: UUser

login: mmoderator@example.com  
password: MModerator

Just run this script from root project directory (if docker, connect first to app container and run this command from workdirectory):

```shell
python load_demo_data.py
```

Remeber to install data from fixtures before run this script.

### Test

To run test and check coverage first create database according to database name specified in .env file, but add prefix "test\_" to the name of the database.

Then from root of the project run:

```shell
pytest -v --cov=./src tests
```
