from fastapi import APIRouter, HTTPException, status
from sqlmodel import select, delete

from app.models import User, Registration
from app.data.db import SessionDep

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[User])
def list_users(session: SessionDep):
    return session.exec(select(User)).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: User, session: SessionDep):
    existing = session.get(User, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")
    session.add(user)
    session.commit()
    return {"username": user.username}


@router.delete("/")
def delete_all_users(session: SessionDep):
    session.exec(delete(Registration))
    session.exec(delete(User))
    session.commit()
    return "All users deleted"


@router.get("/{username}", response_model=User)
def get_user(username: str, session: SessionDep):
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{username}")
def delete_user(username: str, session: SessionDep):
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.exec(delete(Registration).where(Registration.username == username))
    session.commit()
    return "User deleted"
