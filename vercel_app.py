import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Add the project root directory to the Python path
sys.path.insert(0, str(BASE_DIR))

# Configure Django settings before any Django imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'select_class.settings')

# Initialize Django WSGI application
from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
