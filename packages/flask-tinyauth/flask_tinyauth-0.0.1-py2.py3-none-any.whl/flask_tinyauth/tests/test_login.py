import json
import unittest
from unittest import mock

from flask import Flask

from flask_tinyauth import login


class TestAuthorize(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.debug = True
        self.app.config['TESTING'] = True
        self.app.config['DEBUG'] = True
        self.app.config['TINYAUTH_SERVICE'] = 'test'
        self.app.config['TINYAUTH_ENDPOINT'] = 'http://localhost/'
        self.app.config['TINYAUTH_ACCESS_KEY_ID'] = 'root'
        self.app.config['TINYAUTH_SECRET_ACCESS_KEY'] = 'password'
        self.app.register_blueprint(login.login_blueprint)
        self.client = self.app.test_client()

        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def tearDown(self):
        self._ctx.pop()

    def test_static_404(self):
        response = self.client.get('/login/static/missing.css')
        assert response.status_code == 404

    def test_static_serves_js(self):
        response = self.client.get('/login/static/main.b9228724.js')
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/javascript'

    def test_login_get(self):
        response = self.client.get('/login')
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
        assert response.get_data(as_text=True).strip().startswith('<!DOCTYPE html>\n<html lang="en">')
        assert response.get_data(as_text=True).strip().endswith('</html>')

    @mock.patch('flask_tinyauth.api.session')
    def test_login_post(self, session):
        session.post.return_value.json.return_value = {
            'token': '',
            'csrf': '',
        }

        response = self.client.post('/login', content_type='application/json', data=json.dumps({
            'username': 'root',
            'password': 'password',
        }))

        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        assert json.loads(response.get_data(as_text=True)) == {}

        assert session.post.call_args is not None
        assert session.post.call_args[0][0] == 'http://localhost/api/v1/services/test/get-token-for-login'
        request_kwargs = session.post.call_args[1]
        assert request_kwargs['auth'] == ('root', 'password')
        assert request_kwargs['headers']['Accept'] == 'application/json'
        assert request_kwargs['headers']['Content-Type'] == 'application/json'
        assert request_kwargs['json'] == {
            'csrf-strategy': 'cookie',
            'username': 'root',
            'password': 'password',
        }

    def test_logout(self):
        self.client.set_cookie('localhost', 'tinycsrf', 'sdsdsd')
        self.client.set_cookie('localhost', 'tinysess', 'sdsdsd')

        response = self.client.get('/logout')

        assert response.status_code == 302
        assert response.headers['Location'] == 'http://localhost/login'

        assert response.headers.get_all('Set-Cookie') == [
            'tinysess=; Expires=Thu, 01-Jan-1970 00:00:00 GMT; Path=/',
            'tinycsrf=; Expires=Thu, 01-Jan-1970 00:00:00 GMT; Path=/',
        ]
