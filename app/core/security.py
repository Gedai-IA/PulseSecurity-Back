from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt

from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta."""
    try:
        # Converte a senha para bytes
        password_bytes = plain_password.encode('utf-8')
        # Converte o hash para bytes se for string
        if isinstance(hashed_password, str):
            hashed_bytes = hashed_password.encode('utf-8')
        else:
            hashed_bytes = hashed_password
        
        # Verifica a senha usando bcrypt
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        # Log do erro para debug (opcional)
        print(f"Erro ao verificar senha: {e}")
        return False


def get_password_hash(password: str) -> str:
    """Gera hash da senha usando bcrypt."""
    # Garante que a senha seja uma string
    if not isinstance(password, str):
        password = str(password)
    
    # Converte a senha para bytes
    password_bytes = password.encode('utf-8')
    
    # Trunca a senha se for muito longa (bcrypt tem limite de 72 bytes)
    # Isso é raro, mas previne erros
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Gera o salt e faz o hash
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Retorna como string
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria token JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decodifica token JWT."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

