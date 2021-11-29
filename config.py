from os import environ, path
from dotenv import load_dotenv

# Load environment variables from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, 'demo.env'))

# Read environment variables
user = environ.get('REMOTE_USERNAME')
log_file_home_path = basedir + environ.get('LOGFILE_HOME_PATH')
database_hostname = environ.get('DATABASE_HOST_NAME')
database_user = environ.get('DATABASE_USER_NAME')
database_password = environ.get('DATABASE_USER_PASSWORD')
database_port = environ.get('DATABASE_PORT')
database_name = environ.get('DATABASE_NAME')
database_url = environ.get('DATABASE_URL')
