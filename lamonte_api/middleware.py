from lamonte.settings import DEBUG
from logging import getLogger
from pprint import pprint
from time import time
from json import dumps
from rest_framework.exceptions import APIException
from rest_framework.response import Response
import re


class LoggingMiddleware:
    def __init__(self):
        self.logger = getLogger('django.request')
        self.headers = re.compile(r'^(HTTP_.+|CONTENT_TYPE|CONTENT_LENGTH)$')

    def process_request(self, request):
        request.start_time = time()

    def process_response(self, request, response):
        headers = {}
        for key in request.META:
            if self.headers.match(key):
                headers[key] = request.META[key]

        if "HTTP_AUTHORIZATION" in headers and not DEBUG:
            headers["HTTP_AUTHORIZATION"] = "Value was hidden for safety reasons"

        self.logger.info('[%s] %s (%.1fs)\nHeaders\n%s', response.status_code, request.get_full_path(), time() - request.start_time, headers)

        return response



class HeaderMiddleware(object):
    def process_response(self, request, response):
        response["Content-Length"] = len(response.content)
        return response

