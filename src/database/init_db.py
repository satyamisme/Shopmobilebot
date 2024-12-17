from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, User, Role
from src.config import settings
from src.services.auth_service import AuthService
import asyncio
import os

async def init_database():
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Initialize database engine
    engine = create_async_engine(settings.DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    
    # Create default admin user and roles if they don't exist
    async with async_session() as session:
        # Check if admin role exists
        admin_role = await session.get(Role, 1)
        if not admin_role:
            admin_role = Role(
                name="admin",
                permissions="all"
            )
            session.add(admin_role)
        
        # Check if user role exists
        user_role = await session.get(Role, 2)
        if not user_role:
            user_role = Role(
                name="user",
                permissions="search"
            )
            session.add(user_role)
        
        # Create default admin user if it doesn't exist
        auth_service = AuthService(session)
        admin_user = await session.get(User, 1)
        if not admin_user:
            admin_user = User(
                username=settings.ADMIN_USERNAME,
                password_hash=auth_service.get_password_hash(settings.ADMIN_PASSWORD),
                is_active=True
            )
            admin_user.roles.append(admin_role)
            session.add(admin_user)
        
        await session.commit()

def init_db():
    asyncio.run(init_database())