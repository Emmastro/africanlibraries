import os

from dotenv import load_dotenv

load_dotenv()

if os.environ.get('RUNNING_ENV') == 'local':
	from .base import*
	from .local import *
else:
	from .base import *
	from .production import *