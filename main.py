#!/usr/bin/env python3
# coding: utf-8
from socket import socket

from . import Request
from . import log
from . import route_dict
from . import route_static

__author__ = 'Jux.Liu'

request = Request()


def parsed_path(path):
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        args = query_string.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def error(code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    # 之前上课我说过不要用数字来作为字典的 key
    # 但是在 HTTP 协议中 code 都是数字似乎更方便所以打破了这个原则
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def response_for_path(path):
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    log('path and query', path, query)
    routes = {
        '/static/': route_static,
    }
    routes.update(route_dict)
    response = routes.get(path, error)
    return response(request)


def run(host='', port=2333, **kwargs):
    """
main process
    :param host:
    :param port:
    :return:
    """
    with socket() as s:
        s.bind((host, port))
        while True:
            listen_buffer = kwargs['listen_buffer'] if 'listen_buffer' in kwargs.keys() else 5
            s.listen(listen_buffer)
            connection, address = s.accept()
            recv_buffer = kwargs['recv_buffer'] if 'recv_buffer' in kwargs.keys() else 1024
            req = connection.recv(recv_buffer)
            req = req.decode('utf-8')
            log('ip and request, {ip}\n{request}'.format(ip=address, request=req))

            if len(req.split()) < 2:
                # for handle chrome empty request
                continue

            path = req.split()[1]
            request.method = req.split[0]
            request.add_headers(req.split('\r\n\r\n', 1)[0].split('\r\n')[1:])

            response = response_for_path(path)
            connection.sendall(response)
            connection.close()


            # print(kwargs)


if __name__ == '__main__':
    run(host='1', port=2, c=3, d=4, e=5)
