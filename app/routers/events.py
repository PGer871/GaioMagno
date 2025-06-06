from fastapi import APIRouter, HTTPException, status
from sqlmodel import select, delete

from app.models import Event, User, Registration
from app.data.db import SessionDep

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/", response_model=list[Event])
def list_events(session: SessionDep):
    events = session.exec(select(Event)).all()
    return events


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_event(event: Event, session: SessionDep):
    session.add(event)
    session.commit()
    session.refresh(event)
    return {"id": event.id}


@router.delete("/")
def delete_all_events(session: SessionDep):
    session.exec(delete(Registration))
    session.exec(delete(Event))
    session.commit()
    return "All events deleted"


@router.get("/{id}", response_model=Event)
def get_event(id: int, session: SessionDep):
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/{id}")
def update_event(id: int, new_event: Event, session: SessionDep):
    db_event = session.get(Event, id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    db_event.title = new_event.title
    db_event.description = new_event.description
    db_event.date = new_event.date
    db_event.location = new_event.location
    session.add(db_event)
    session.commit()
    return "Event updated"


@router.delete("/{id}")
def delete_event(id: int, session: SessionDep):
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    session.delete(event)
    session.exec(delete(Registration).where(Registration.event_id == id))
    session.commit()
    return "Event deleted"


@router.post("/{id}/register")
def register_user(id: int, user: User, session: SessionDep):
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    db_user = session.get(User, user.username)
    if not db_user:
        session.add(user)
        session.commit()
        db_user = user

    reg = session.get(Registration, (db_user.username, event.id))
    if reg:
        raise HTTPException(status_code=400, detail="User already registered")
    reg = Registration(username=db_user.username, event_id=event.id)
    session.add(reg)
    session.commit()
    return "Registered"
