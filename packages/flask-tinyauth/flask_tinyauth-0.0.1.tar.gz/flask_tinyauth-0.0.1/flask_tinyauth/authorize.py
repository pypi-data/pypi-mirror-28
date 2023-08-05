import datetime

from flask import abort, jsonify, make_response, request, url_for

from . import api, exceptions, redirect


def authorize(permission, resource_class=None, resource='', ctx=None):
    context = {
        'SourceIp': request.remote_addr,
        'RequestDateTime': datetime.datetime.utcnow().isoformat(),
    }
    context.update(ctx or {})

    if resource_class:
        resource_arn = api.format_arn(resource_class, resource)
    else:
        resource_arn = api.get_arn_base()

    return api.call('authorize-by-token', {
        'permit': {
            permission: [resource_arn],
        },
        'headers': request.headers.to_wsgi_list(),
        'context': context,
    })


def authorize_or_401(permission, resource_class=None, resource='', ctx=None):
    try:
        authorized = authorize(permission, resource_class, resource, ctx)
    except exceptions.AuthorizationFailed:
        abort(make_response(jsonify({'Authorized': False}), 401))

    if authorized['Authorized'] is not True:
        abort(make_response(jsonify(authorized), 401))

    return authorized


def authorize_or_login(permission, resource_class=None, resource='', ctx=None):
    try:
        authorized = authorize(permission, resource_class, resource, ctx)
    except exceptions.AuthorizationFailed:
        raise redirect.Redirect(url_for('login.login'))

    if authorized['Authorized'] is not True:
        raise redirect.Redirect(url_for('login.login'))

    return authorized
