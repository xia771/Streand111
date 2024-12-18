"""
WSGI config for scss project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from django.core.handlers.wsgi import WSGIHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'select_class.settings')

class VercelWSGIHandler(WSGIHandler):
    def __call__(self, environ, start_response):
        try:
            return super().__call__(environ, start_response)
        except Exception as e:
            import traceback
            print('Error:', str(e))
            print('Traceback:', traceback.format_exc())
            raise

application = VercelWSGIHandler()
app = application
