## ODD MySQL adapter

ODD MySQL adapter is used for extracting datasets and and data transformers info and metadata from MySQL. This adapter is implemetation of pull model (see more https://github.com/opendatadiscovery/opendatadiscovery-specification/blob/main/specification/specification.md#discovery-models). By default application gather data from MySQL every minute, put it inside local cache and then ready to give it away by /entities API.

This service based on Python Flask and Connexion frameworks with APScheduler.

#### Data entities:
| Entity type | Entity source |
|:----------------:|:---------:|
|Dataset|Tables, Columns|
|Data Transformer|Views|

For more information about data entities see https://github.com/opendatadiscovery/opendatadiscovery-specification/blob/main/specification/specification.md#data-model-specification

## Quickstart
Application is ready to run out of the box by the docker-compose (see more https://docs.docker.com/compose/).
Strongly recommended to override next variables in docker-compose .env file:

```
MYSQL_DATABASE=oddadapter
MYSQL_USER=oddadapter
MYSQL_PASSWORD=odd-adapter-password

CLOUD_TYPE=aws
CLOUD_REGION=region_1
CLOUD_ACCOUNT=account_1
```

After docker-compose run successful, application is ready to accept connection on port :8080. 
For more information about variables see next section.

#### Config for Helm:
```
podSecurityContext:
  fsGroup: 65534
image:
  pullPolicy: Always
  repository: 436866023604.dkr.ecr.eu-central-1.amazonaws.com/odd-mysql-adapter
  tag: ci-655380
nameOverride: odd-mysql-adapter
labels:
  adapter: odd-mysql-adapter
config:
  envFrom:
  - configMapRef:
      name: odd-mysql-adapter
  env:
  - name: DEMO_GREETING
    value: "Hello from the environment"
  - name: DEMO_FAREWELL
    value: "Such a sweet sorrow"
```
More info about Helm config in https://github.com/opendatadiscovery/charts


## Environment
Adapter is ready to work out of box, but you probably will need to redefine some variables in compose .env file:

```Python
FLASK_ENVIRONMENT = development #For production case change this to "production"
FLASK_APP = wsgi:application #Path to wsgi module of application (required by gunicorn)

MYSQL_HOST = db-mysql #Host of your ClickHouse database.
MYSQL_PORT = 3306 #Port of your ClickHouse database.
MYSQL_DATABASE = oddadapter #Name of your ClickHouse database.
MYSQL_USER = oddadapter #Username of your ClickHouse database.
MYSQL_PASSWORD = odd-adapter-password #Password of your ClickHouse database.

CLOUD_TYPE = aws #Name of your cloud service. Used to form ODDRN.
CLOUD_REGION = region_1 #Region of your cloud service. Used to form ODDRN.
CLOUD_ACCOUNT = account_1 #Account of your cloud service. Used to form ODDRN.
```

## Requirements
- Python 3.8
- MySQL 5.7
