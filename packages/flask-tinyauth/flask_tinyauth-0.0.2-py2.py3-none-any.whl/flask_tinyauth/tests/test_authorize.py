import json
import unittest
from unittest import mock

from flask import Flask
from requests import exceptions
from werkzeug.datastructures import Headers

from flask_tinyauth import AuthorizationFailed, authorize, login


class TestAuthorize(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['TINYAUTH_SERVICE'] = 'test'
        self.app.config['TINYAUTH_ENDPOINT'] = 'http://localhost/'
        self.app.config['TINYAUTH_ACCESS_KEY_ID'] = 'root'
        self.app.config['TINYAUTH_SECRET_ACCESS_KEY'] = 'password'
        self.app.register_blueprint(login.login_blueprint)
        self.client = self.app.test_client()

        @self.app.route('/')
        def index():
            authorize.authorize_or_401('TestPermission', 'res_class', 'res_key')
            return 'INDEX'

        @self.app.route('/raise')
        def or_raise():
            authorize.authorize_or_raise('TestPermission', 'res_class', 'res_key')
            return 'INDEX'

        @self.app.route('/sub-page')
        def sub_page():
            authorize.authorize_or_401('TestSubPagePermission')
            return 'SUB-PAGE'

        @self.app.route('/hi')
        def hi():
            authorize.authorize_or_login('TestPermission', 'res_class', 'res_key')
            return 'INDEX'

        @self.app.errorhandler(AuthorizationFailed)
        def handle_invalid_usage(error):
            return 'YOU HAVE FAILED THIS AUTH'

        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def tearDown(self):
        self._ctx.pop()

    @mock.patch('flask_tinyauth.api.session')
    def test_authorize_or_401_bypass(self, session):
        self.app.config['TINYAUTH_BYPASS'] = True
        try:
            response = self.client.get('/')
        finally:
            self.app.config['TINYAUTH_BYPASS'] = False

        assert session.post.call_count == 0
        assert response.status_code == 200
        assert response.get_data(as_text=True) == 'INDEX'

    @mock.patch('flask_tinyauth.api.session')
    def test_authorize_or_401_authd(self, session):
        session.post.return_value.json.return_value = {
            'Authorized': True,
        }
        response = self.client.get('/')

        assert session.post.call_args is not None
        assert session.post.call_args[0][0] == 'http://localhost/api/v1/services/test/authorize-by-token'
        request_kwargs = session.post.call_args[1]
        assert request_kwargs['auth'] == ('root', 'password')
        assert request_kwargs['headers']['Accept'] == 'application/json'
        assert request_kwargs['headers']['Content-Type'] == 'application/json'
        assert request_kwargs['json']['permit'] == {
            'TestPermission': ['arn:tinyauth:test:default::res_class/res_key']
        }
        assert request_kwargs['json']['context']['SourceIp'] == '127.0.0.1'
        assert Headers(request_kwargs['json']['headers'])['Content-Length'] == '0'

        assert response.status_code == 200
        assert response.get_data(as_text=True) == 'INDEX'

    @mock.patch('flask_tinyauth.api.session')
    def test_authorize_or_401_no_resource_instance_authd(self, session):
        session.post.return_value.json.return_value = {
            'Authorized': True,
        }
        response = self.client.get('/sub-page')

        assert session.post.call_args is not None
        assert session.post.call_args[0][0] == 'http://localhost/api/v1/services/test/authorize-by-token'
        request_kwargs = session.post.call_args[1]
        assert request_kwargs['auth'] == ('root', 'password')
        assert request_kwargs['headers']['Accept'] == 'application/json'
        assert request_kwargs['headers']['Content-Type'] == 'application/json'
        assert request_kwargs['json']['permit'] == {
            'TestSubPagePermission': ['arn:tinyauth:test:default::']
        }

        assert response.status_code == 200
        assert response.get_data(as_text=True) == 'SUB-PAGE'

    @mock.patch('flask_tinyauth.api.session')
    def test_authorize_or_401_not_authd(self, session):
        session.post.return_value.json.return_value = {
            'Authorized': False,
        }
        response = self.client.get('/')
        assert response.status_code == 401
        assert json.loads(response.get_data(as_text=True)) == {
            "Authorized": False
        }

    @mock.patch('flask_tinyauth.api.session')
    def test_authorize_or_401_connection_error(self, session):
        session.post.side_effect = exceptions.ConnectionError()
        response = self.client.get('/')
        assert response.status_code == 401
        assert json.loads(response.get_data(as_text=True)) == {
            "Authorized": False
        }

    @mock.patch('flask_tinyauth.api.session')
    def test_authorize_or_login_bypass(self, session):
        self.app.config['TINYAUTH_BYPASS'] = True
        try:
            response = self.client.get('/hi')
        finally:
            self.app.config['TINYAUTH_BYPASS'] = False

        assert session.post.call_count == 0
        assert response.status_code == 200
        assert response.get_data(as_text=True) == 'INDEX'

    @mock.patch('flask_tinyauth.api.session')
    def test_authorize_or_login_authd(self, session):
        session.post.return_value.json.return_value = {
            'Authorized': True,
        }
        response = self.client.get('/hi')
        assert response.status_code == 200
        assert response.get_data(as_text=True) == 'INDEX'

    @mock.patch('flask_tinyauth.api.session')
    def test_authorize_or_login_not_authd(self, session):
        session.post.return_value.json.return_value = {
            'Authorized': False,
        }
        response = self.client.get('/hi')
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://localhost/login'

    @mock.patch('flask_tinyauth.api.session')
    def test_authorize_or_login_connection_error(self, session):
        session.post.side_effect = exceptions.ConnectionError()
        response = self.client.get('/hi')
        assert response.status_code == 302
        assert response.headers['Location'] == 'http://localhost/login'

    @mock.patch('flask_tinyauth.api.session')
    def test_authorize_or_raise_bypass(self, session):
        self.app.config['TINYAUTH_BYPASS'] = True
        try:
            response = self.client.get('/raise')
        finally:
            self.app.config['TINYAUTH_BYPASS'] = False

        assert session.post.call_count == 0
        assert response.status_code == 200
        assert response.get_data(as_text=True) == 'INDEX'

    @mock.patch('flask_tinyauth.api.session')
    def test_authorize_or_raise_authd(self, session):
        session.post.return_value.json.return_value = {
            'Authorized': True,
        }
        response = self.client.get('/raise')

        assert session.post.call_args is not None
        assert session.post.call_args[0][0] == 'http://localhost/api/v1/services/test/authorize-by-token'
        request_kwargs = session.post.call_args[1]
        assert request_kwargs['auth'] == ('root', 'password')
        assert request_kwargs['headers']['Accept'] == 'application/json'
        assert request_kwargs['headers']['Content-Type'] == 'application/json'
        assert request_kwargs['json']['permit'] == {
            'TestPermission': ['arn:tinyauth:test:default::res_class/res_key']
        }
        assert request_kwargs['json']['context']['SourceIp'] == '127.0.0.1'
        assert Headers(request_kwargs['json']['headers'])['Content-Length'] == '0'

        assert response.status_code == 200
        assert response.get_data(as_text=True) == 'INDEX'

    @mock.patch('flask_tinyauth.api.session')
    def test_authorize_or_raise_not_authd(self, session):
        session.post.return_value.json.return_value = {
            'Authorized': False,
        }
        response = self.client.get('/raise')
        assert response.get_data(as_text=True) == 'YOU HAVE FAILED THIS AUTH'

    @mock.patch('flask_tinyauth.api.session')
    def test_authorize_or_raise_connection_error(self, session):
        session.post.side_effect = exceptions.ConnectionError()
        response = self.client.get('/raise')
        assert response.get_data(as_text=True) == 'YOU HAVE FAILED THIS AUTH'
