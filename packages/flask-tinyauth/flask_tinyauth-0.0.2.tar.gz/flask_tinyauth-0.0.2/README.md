# flask_tinyauth

[![Docker Automated build](https://img.shields.io/docker/automated/tinyauth/flask_tinyauth.svg)](https://hub.docker.com/r/tinyauth/flask_tinyauth/) [![PyPI](https://img.shields.io/pypi/v/flask_tinyauth.svg)](https://pypi.python.org/pypi/flask_tinyauth) [![Codecov](https://img.shields.io/codecov/c/github/tinyauth/flask_tinyauth.svg)](https://codecov.io/gh/tinyauth/flask_tinyauth)

Helper functions (and blueprints) for integrating tinyauth authorization into your flask microservices.

## Protecting an API

```
from flask import Flask
from flask_tinyauth import authorize_or_401


app = Flask(__name__)

app.config['TINYAUTH_SERVICE'] = 'test'
app.config['TINYAUTH_ENDPOINT'] = 'http://localhost/'
app.config['TINYAUTH_ACCESS_KEY_ID'] = 'gatekeeper'
app.config['TINYAUTH_SECRET_ACCESS_KEY'] = 'keymaster'

@app.route('/api/v1/apples/list')
def list_apples():
    authorize_or_401('ListApples', 'apples')
    return jsonify([{'name': 'fred', 'weight': 50, 'color': 'red'}])

@app.route('/api/v1/apples/<name:path>')
def get_apple(name):
    authorize_or_401('GetApple', 'apples', name)
    return jsonify({'name': 'fred', 'weight': 50, 'color': 'red'})
```

Accessing `/api/v1/apples/list` will do a permissions test for `ListApples` with resource set to `arn:tinyauth:test:default::apples/`. Accessing `/api/v1/apples/fred` will do a permissions test for `GetApple` with resource set to `arn:tinyauth:test:default::apples/fred`.

This helper will return a 401 response (via flasks `abort()` mechanism) with a JSON error message if the user is not authenticated or does not have the required access.

# Customizing the authentication message

The `authorize_or_raise` variant works exactly the same as `authorize_or_401` only it allows authentication and authorization exceptions to be raised. These can then be handled by flask and `app.errorhandler`:

```
from flask import Flask
from flask_tinyauth import AuthorizationFailed, authorize_or_401


app = Flask(__name__)

app.config['TINYAUTH_SERVICE'] = 'test'
app.config['TINYAUTH_ENDPOINT'] = 'http://localhost/'
app.config['TINYAUTH_ACCESS_KEY_ID'] = 'gatekeeper'
app.config['TINYAUTH_SECRET_ACCESS_KEY'] = 'keymaster'

@app.route('/api/v1/apples/list')
def list_apples():
    authorize_or_raise('ListApples', 'apples')
    return jsonify([{'name': 'fred', 'weight': 50, 'color': 'red'}])

@self.app.errorhandler(AuthorizationFailed)
def handle_invalid_usage(error):
    return 'Authorization has failed'
```

# Protecting a user interface

flask_tinyauth is primarily for authenticating for API microservices. But you can build user interfaces with it too. In that case `authorize_or_401` is not appropriate - you will want to redirect the user to a login page not show them a JSON 401.

You can do this with `authorize_or_login`

```
from flask import Flask
from flask_tinyauth import authorize_or_login


app = Flask(__name__)

app.config['TINYAUTH_SERVICE'] = 'test'
app.config['TINYAUTH_ENDPOINT'] = 'http://localhost/'
app.config['TINYAUTH_ACCESS_KEY_ID'] = 'gatekeeper'
app.config['TINYAUTH_SECRET_ACCESS_KEY'] = 'keymaster'

@app.route('/')
def list_apples():
    authorize_or_login('AccessWebInterface')
    return '<html></html>'
```


## Adding a login page

The following is the bare minimum required to get a functional login page for your site (and logoff). Note that this **does not** protect any of your views by itself.

```
from flask import Flask
from flask_tinyauth import login_blueprint


app = Flask(__name__)

app.config['TINYAUTH_SERVICE'] = 'test'
app.config['TINYAUTH_ENDPOINT'] = 'http://localhost/'
app.config['TINYAUTH_ACCESS_KEY_ID'] = 'gatekeeper'
app.config['TINYAUTH_SECRET_ACCESS_KEY'] = 'keymaster'

app.register_blueprint(login_blueprint)
```


## admin-on-rest

This assumes that you have an API at `/api` guarded with `authorize_or_401` or `authorize_or_raise` and a page at `/` that serves your React app guarded with `authorize_or_login`.


## Settings

The backend to connect to is controlled by these settings:

 * `TINYAUTH_ENDPOINT`: The `https://` endpoint to access to authorize a HTTP request.
 * `TINYAUTH_ACCESS_KEY_ID`: Access key for a tinyauth user with permission to authorize requests for this service.
 * `TINYAUTH_SECRET_ACCESS_KEY`: Secret key for this user
 * `TINYAUTH_ENDPOINT_VERIFY`: Either a boolean, in which case it controls whether we verify the server's TLS certificate, or a string, in which case it must be a path to a CA bundle to use. Defaults to True.

Each permission check is for a permission and an `arn` that globally identifies an instance of a resource. An arn is constructed in the following form:

```
arn:partition:service:region::resource_type/resource_instance
```

The following settings control the `arn` used for your service.

 * `TINYAUTH_PARTITION`: Optional, defaults to `tinyauth`. A partition is a multi-region tinyauth cluster. For example, Amazon have the `aws` partition and the `aws-cn` partition. IAM users existing in the `aws` partition work for all regions in the `aws` partition. At a more modest scale, you likely have a production and test partition.
 * `TINYAUTH_SERVICE`: Required. This is your services name. This should be short and lowercase. Its how your microservice can be differentiated from other microservices of different types.
 * `TINYAUTH_REGION`: Optional, defaults to `default`. If you have multiple instances of your service in different data centers then you have regions, and tinyauth can consider there authorization requirements seperately.

Additionally development environments can set:

 * `TINYAUTH_BYPASS`: All `authorize_*` functions return that a user is authorized, completely bypassing auditing, authentication and authorization.


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
