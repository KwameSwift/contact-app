import os
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
CSV_PATH = os.environ.get('CSV_PATH')
AWS_BUCKET_REGION = os.environ.get('AWS_BUCKET_REGION')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.environ.get('AWS_REGION')
SECRET_KEY=os.environ.get('SECRET_KEY')
