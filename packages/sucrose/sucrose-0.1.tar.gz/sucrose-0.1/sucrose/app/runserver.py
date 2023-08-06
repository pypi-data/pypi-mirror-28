from sucrose.app import app
import inspect
import json
from functools import wraps
from flask import request
import requests

import sys, traceback


class SucroseRemoteException(Exception):
    def __init__(self, message, exception_type):
        error_mess="{message}, exception_type:{exception_type}".format(
            message=message, exception_type=exception_type
        )
        super(SucroseRemoteException, self).__init__(error_mess)
        self.summmary = error_mess
        self.remote_exception = exception_type


def rpc(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            exc_info = sys.exc_info()

            the_args = json.loads(request.data)
            r = f(*args, **the_args)
            response = {'content': r, 'error': False}
            return json.dumps(response)

        except Exception as e:
            error = {'message': e.args, 'exception_type': str(type(e))}
            response = {'content': error, 'error': True}
            return json.dumps(response)

    return wrapped


def add_service(service):
    service_instance = service()
    for function in dir(service_instance):
        if (inspect.ismethod(getattr(service_instance, function)) and not
                function.startswith('_')):

            url = "/{service}/{function}".format(
                service=service_instance.__name__, function=function)
            app.add_url_rule(
                url, service_instance.__name__ + function,
                getattr(service_instance, function),
                methods=['POST'])


class RpcProxy(object):
    def __init__(self, service_name, host='0.0.0.0'):
        self.service = service_name
        self.host = host

    def __getattr__(self, name):
        def method_proxy(*args, **kwargs):
            url = '{host}/{service}/{method}'.format(
                host=self.host, service=self.service,
                method=name)
            r = requests.post(url, data=json.dumps(kwargs))

            response = json.loads(r.content)

            if not response['error']:
                return response['content']
            else:
                raise SucroseRemoteException(
                    response['content']['message'],
                    response['content']['exception_type']
                )
        return method_proxy


def run_services(port, debug=False, threaded=True):
    app.run(host='0.0.0.0', debug=debug, port=port, threaded=threaded)
