# flask_tinyauth

[![Docker Automated build](https://img.shields.io/docker/automated/tinyauth/flask_tinyauth.svg)](https://hub.docker.com/r/tinyauth/flask_tinyauth/) [![PyPI](https://img.shields.io/pypi/v/flask_tinyauth.svg)](https://pypi.python.org/pypi/flask_tinyauth) [![Codecov](https://img.shields.io/codecov/c/github/tinyauth/flask_tinyauth.svg)](https://codecov.io/gh/tinyauth/flask_tinyauth)

Helper functions (and blueprints) for integrating tinyauth authorization into your flask microservices.


## Dev Environment

You can get a simple dev environment with Docker and docker-compose. Dev happens on macOS with Docker for Mac:

```
docker-compose build
docker-compose up
```

This will automatically run any migrations.

You can run tests with:

```
docker-compose run --rm flask py.test flask_tinyauth/
```

And run flake8 with:

```
docker-compose run --rm flask flake8 flask_tinyauth/
```
