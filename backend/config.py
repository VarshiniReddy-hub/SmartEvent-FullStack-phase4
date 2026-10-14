import os
from dotenv import load_dotenv

load_dotenv()

<<<<<<< HEAD
SECRET_KEY = os.getenv("SECRET_KEY", "smartevent-local-development-key-change-before-deployment")
=======
SECRET_KEY = os.getenv("SECRET_KEY")
>>>>>>> origin/main
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)