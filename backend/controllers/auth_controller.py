from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "votre_secret_key"
ALGORITHM = "HS256"


def create_token(user_id: int, role: str):
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {
        "sub": user_id,
        "role": role,
        "exp": expiration
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
