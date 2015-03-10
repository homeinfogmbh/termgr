"""WSGI main program for ImmoSearch"""

from termgr.controllers.setup import SetupController

def application(environ, start_response):
    """Main WSGI method"""
    ctrl = SetupController(environ.get('PATH_INFO', ''),
                           environ.get('QUERY_STRING', ''))
    status, content_type, charset, response_body = ctrl.run()
    response_headers = [('Content-Type',
                         '; '.join([content_type,
                                    '='.join(['charset', charset])])),
                       ('Content-Length', str(len(response_body))),
                       ('Access-Control-Allow-Origin', '*')]
    start_response(status, response_headers)
    return [response_body]

