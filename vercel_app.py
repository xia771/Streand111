import os
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'select_class.settings')
os.environ.setdefault('PYTHONPATH', '.')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Vercel needs the variable 'app'
app = application
