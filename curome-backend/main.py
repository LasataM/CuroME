from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import engine, Base, get_db
import models
import schemas
import auth
import auth_utils

# ------------------------------------------------------------------
# Create database tables
# ------------------------------------------------------------------

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CuroME API")


# ------------------------------------------------------------------
# Registration
# ------------------------------------------------------------------

@app.post(
    "/auth/register",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    # Check existing email
    db_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    # Hash password
    hashed_pw = auth.hash_password(user.password)

    # Create user
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role,
        name=user.name,
        age=user.age,
        gender=user.gender,
        phone=user.phone,
        specialization=user.specialization,
        license_number=user.license_number,
        linked_patient_id=user.linked_patient_id,

        patient_id=(
            f"PAT-{user.name[:3].upper()}{user.age or 0}"
            if user.role == schemas.RoleEnum.PATIENT
            else None
        ),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ------------------------------------------------------------------
# Login
# ------------------------------------------------------------------

@app.post("/auth/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == form_data.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not auth.verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = auth_utils.create_access_token(
        data={
            "sub": user.email,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# ------------------------------------------------------------------
# Current User
# ------------------------------------------------------------------

@app.get(
    "/users/me",
    response_model=schemas.UserResponse,
)
def get_current_logged_in_user(
    current_user: models.User = Depends(auth.get_current_user),
):
    return current_user


# ------------------------------------------------------------------
# Root
# ------------------------------------------------------------------

@app.get("/")
def read_root():
    return {
        "message": "CuroME API is running!"
    }