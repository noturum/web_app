import os
from dotenv import load_dotenv
load_dotenv()

EXPIRE_MINUTES = os.getenv('EXPIRE_MINUTES')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
