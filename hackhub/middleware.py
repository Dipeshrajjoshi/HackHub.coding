import logging
from django.shortcuts import render
from django.http import HttpResponseServerError

# grabbing the logger we defined in settings.py
logger = logging.getLogger('django')

# this middleware catches any crazy errors that happen during a request
class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # standard middleware stuff, just pass the request along
        response = self.get_response(request)
        return response

    # This runs whenever something breaks in a view to show a nice error page
    def process_exception(self, request, exception):
        # logging the error so we can check the logs/django.log later
        logger.error(f"Unhandled Exception: {exception}", exc_info=True, extra={
            'request': request,
        })
        
        # for now we let django handle the response, but we logged the crash details above
        return None
