#!/usr/bin/env python3
# coding: utf-8
from functools import wraps

from . import static_path
from . import template_path

__author__ = 'Jux.Liu'

route_dict = {
    'get': {},
    'post': {}
}


def route(url, methods=['get']):
    def _route(func):
        @wraps(func)
        def __route(*args, **kwargs):
            for method in methods:
                route_dict[method][url] = func
            return

        return __route

    return _route


def route_static(request):
    """
built-in function,
return static files
    :param request:
    :return:
    """
    filename = request.query.get('file', )
    path = '{static_path}{filename}'.format(static_path=static_path, filename=filename)
    with open(path, 'rb') as f:
        header = 'HTTP/1.x 200 OK\r\nContent-Type:{filetype}'.format(filetype='')
        response = '{header}\r\n\r\n{body}'.format(header=header, body=f.read())
        return response


def return_template(filename):
    """
    :param filename:
    :param path:
    :return:
    """
    template_file = '{path}{filename}'.format(path=template_path, filename=filename)
    with open(template_file, 'r', encoding='utf-8') as f:
        return f.read()
