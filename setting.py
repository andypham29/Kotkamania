# settings.py
from dotenv import load_dotenv

load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
from pathlib import Path  # Python 3.6+ only

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

import os


class Setting:
    CONSUMER_KEY = os.getenv("CONSUMER_KEY")
    CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
    KKMANIA_API_KEY = os.getenv("KKMANIA_API_KEY")
    NHL_YEAR = os.getenv("NHL_YEAR")
