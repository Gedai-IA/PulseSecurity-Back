from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.infrastructure.database.session import get_db
from app.infrastructure.database.models import UserModel
from app.api.v1.schemas.auth_schemas import (
    UserCreateSchema,
    UserLoginSchema,
    UserResponseSchema,
    TokenSchema,
)
from app.core.security import verify_password, get_password_hash, create_access_token

router = APIRouter()


@router.post("/auth/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    """Registra um novo usuário."""
    # Verifica se o usuário já existe
    result = await db.execute(
        select(UserModel).where(
            (UserModel.username == user_data.username) | (UserModel.email == user_data.email)
        )
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        if existing_user.username == user_data.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username já está em uso"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já está em uso"
            )
    
    # Cria novo usuário
    hashed_password = get_password_hash(user_data.password)
    new_user = UserModel(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return UserResponseSchema(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        full_name=new_user.full_name,
        is_active=new_user.is_active,
    )


@router.post("/auth/login", response_model=TokenSchema)
async def login(
    credentials: UserLoginSchema,
    db: AsyncSession = Depends(get_db),
):
    """Autentica um usuário e retorna um token JWT."""
    # Busca o usuário
    result = await db.execute(
        select(UserModel).where(UserModel.username == credentials.username)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verifica se o usuário está ativo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )
    
    # Verifica a senha
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Cria o token
    access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
    
    return TokenSchema(
        access_token=access_token,
        token_type="bearer",
        user=UserResponseSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
        ),
    )
