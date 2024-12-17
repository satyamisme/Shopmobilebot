from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.config import settings
from src.database.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)
    
    async def authenticate_user(self, username: str, password: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user or not self.verify_password(password, user.password_hash):
            return None
        return user
    
    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    
    async def get_current_user(self, token: str) -> User | None:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            username: str = payload.get("sub")
            if username is None:
                return None
        except JWTError:
            return None
        
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        return user