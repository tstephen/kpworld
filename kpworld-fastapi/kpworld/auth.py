import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .database import get_db
from .db_models import User

logger = logging.getLogger(__name__)

# Security configurations
SECRET_KEY = "your-secret-key"  # In production, use secure environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token header dependency
token_header = APIKeyHeader(name="Authorization", auto_error=False)

def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """Create a JWT access token."""
    logger.info("Creating access token for data: %s", data)
    
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        token = f"Token {encoded_jwt}"
        logger.debug("Token created successfully")
        return token
    except Exception as e:
        logger.error("Failed to create access token: %s", str(e))
        raise

def get_token(authorization: str = Depends(token_header)) -> Optional[str]:
    """Extract token from authorization header."""
    logger.debug("Processing authorization header: %s", authorization)
    
    if not authorization or not authorization.startswith("Token "):
        logger.warning("Invalid or missing authorization header")
        return None
    
    token = authorization.replace("Token ", "")
    logger.debug("Token extracted successfully")
    return token

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(get_token)
) -> User:
    """Dependency to get the current authenticated user."""
    logger.info("Authenticating user from token")
    
    if not token:
        logger.error("No token provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Token"},
        )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            logger.error("Token payload missing email")
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError as e:
        logger.error("Failed to decode token: %s", str(e))
        raise HTTPException(status_code=401, detail="Invalid token") from e
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        logger.error("User not found for email: %s", email)
        raise HTTPException(status_code=401, detail="User not found")
    
    logger.info("Successfully authenticated user: %s", user.email)
    return user

# Optional Authentication - for endpoints that can work with or without auth
async def get_optional_user(
    db: Session = Depends(get_db),
    token: str = Depends(get_token)
) -> Optional[User]:
    """Dependency to optionally get the current user."""
    logger.debug("Attempting optional authentication")
    
    if not token:
        logger.debug("No token provided for optional auth")
        return None
    
    try:
        return await get_current_user(db, token)
    except HTTPException:
        logger.debug("Optional auth failed, continuing as anonymous")
        return None
