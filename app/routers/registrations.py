from fastapi import APIRouter
from sqlmodel import select, delete

from app.models import Registration
from app.data.db import SessionDep

router = APIRouter(prefix="/registrations", tags=["registrations"])


@router.get("/", response_model=list[Registration])
def list_regs(session: SessionDep):
    return session.exec(select(Registration)).all()


@router.delete("/")
def delete_registration(username: str, event_id: int, session: SessionDep):
    session.exec(
        delete(Registration).where(
            Registration.username == username,
            Registration.event_id == event_id,
        )
    )
    session.commit()
    return "Registration deleted"
