from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.models.users import User, UserCreate, UserRole
from app.db import get_session


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY environment variable set")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

router = APIRouter(prefix="/users", tags=["Users"])

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = session.exec(
        select(User).where(User.username == username)
    ).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_admin(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=403,
            detail="Only admin can perform this action"
        )
    return current_user

@router.post("/create", response_model=User)
async def create_user(
    user: UserCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_admin)
):
    db_user = session.exec(
        select(User).where(User.username == user.username)
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        password=hashed_password,
        role=user.role
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.exec(
        select(User).where(User.username == form_data.username)
    ).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {"sub": user.username, "exp": datetime.utcnow() + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/init-admin", response_model=User)
async def initialize_admin(
    admin: UserCreate,
    session: Session = Depends(get_session)
):
    # Check if any admin exists
    existing_admin = session.exec(
        select(User).where(User.role == UserRole.admin)
    ).first()
    
    if existing_admin:
        raise HTTPException(
            status_code=400,
            detail="Admin already exists"
        )
    
    # Ensure the role is admin
    if admin.role != UserRole.admin:
        raise HTTPException(
            status_code=400,
            detail="Initial user must be an admin"
        )
    
    # Create admin user
    hashed_password = get_password_hash(admin.password)
    db_user = User(
        username=admin.username,
        password=hashed_password,
        role=UserRole.admin
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user