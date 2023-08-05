from flask import redirect
from werkzeug.routing import HTTPException, RoutingException


class Redirect(HTTPException, RoutingException):

    def __init__(self, new_url, code=302):
        RoutingException.__init__(self, new_url)
        self.new_url = new_url
        self.code = code

    def get_response(self, environ):
        return redirect(self.new_url, self.code)
