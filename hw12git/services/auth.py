from typing import Optional
from functools import wraps
from enum import Enum

from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from database.db import get_db
from repository import users as repository_users
from database.models import User

class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = "secret_key"
    ALGORITHM = "HS256"
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)


    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)


    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=150)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token


    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token


    async def decode_refresh_token(self, refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
        

    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception

        user = await repository_users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user


auth_service = Auth()




USER_ROLES = { "admin": ["admin"], "moderator": ["admin", "moderator"] }

async def get_user_role(user: User, db: Session) -> None:
    # user = db.query(User).filter(User.id == user.id).first()
    return user.roles

def check_role(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Отримання ролі користувача (ваша реалізація)
            user_role = get_user_role()  # Наприклад, отримуємо роль з JWT токену або бази даних
            if user_role not in USER_ROLES.get(role, []):
                raise HTTPException(status_code=403, detail="Access denied")
            return func(*args, **kwargs)
        return wrapper
    return decorator
   
#     @app.get("/admin")
#     @check_role("admin")
#     async def admin_route():
#        return {"message": "Admin access granted"}



class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    user = "user"

class User:
    def __init__(self, username: str, role: UserRole):
        self.username = username
        self.role = role

# Функція, яка повертає імітованого користувача
def get_user(username: str):
    # Реалізуйте логіку отримання користувача з бази даних або іншим способом
    # У цьому прикладі ми повертаємо користувача з фіксованою роллю "admin"
    return User(username=username, role=UserRole.admin)

# Перевірка ролі користувача для адміністратора
def check_admin(user: User = Depends(get_user)):
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access denied")

# Перевірка ролі користувача для менеджера
def check_manager(user: User = Depends(get_user)):
    if user.role != UserRole.manager:
        raise HTTPException(status_code=403, detail="Manager access denied")

# # Захищений маршрут для адміністратора
# @app.get("/admin")
# async def admin_route(user: User = Depends(check_admin)):
#     return {"message": "Admin access granted"}

# # Захищений маршрут для менеджера
# @app.get("/manager")
# async def manager_route(user: User = Depends(check_manager)):
#     return {"message": "Manager access granted"}

# # Захищений маршрут для звичайного користувача
# @app.get("/user")
# async def user_route(user: User):
#     return {"message": "User access granted"}
