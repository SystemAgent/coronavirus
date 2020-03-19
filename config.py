import os

from dotenv import load_dotenv


PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(PROJECT_PATH, '.env'), override=True)

POSTGRES_USER = os.environ.get('POSTGRES_USER', os.environ.get('USER'))
POSTGRES_PASS = os.environ.get('POSTGRES_PASS', '')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'corona_bg')
