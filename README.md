# WebMRP Core Services

This is a set of services that will enable the creation of webapps.

## Architecture Model
![Backend Architecture Model](docs/images/backend-architecture.png)

## Validations Endpoint
Validations endpoint 
```
/api/validation/:provider/:fn/:value
```
is a gateway to services that may be added to the system. It accetps `GET` or `PUT` requests. Validation params are
- *provider*: the validation service name
- *fn*: the service method that will be called
- *value*: the value that will be validated

## Running services in the development environment

* Run RabbitMQ with docker exposing the default port
```
docker run -p 5672:5672 --hostname nameko-rabbitmq rabbitmq:3
```
* Export env vars with database information, then run the start script

```
export DB_HOST=localhost
export DB_PORT=5432
export DB_USER=db_user_name
export DB_PASS=db_password
export DB_NAME=database_name
./start.sh
```
