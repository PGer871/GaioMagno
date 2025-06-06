from sqlmodel import create_engine, SQLModel, Session, select
from typing import Annotated
from fastapi import Depends
import os
from faker import Faker
from app.config import config
# TODO: remember to import all the DB models here
from app.models import Event, User, Registration  # NOQA


sqlite_file_name = config.root_dir / "data/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True)


def init_database() -> None:
    ds_exists = os.path.isfile(sqlite_file_name)
    SQLModel.metadata.create_all(engine)
    if not ds_exists:
        f = Faker("it_IT")
        with Session(engine) as session:
            # (optional) initialize the database with fake data
            events = [
                Event(
                    title=f.sentence(nb_words=3),
                    description=f.text(max_nb_chars=40),
                    date=f.date_time_this_year(),
                    location=f.city(),
                )
                for _ in range(5)
            ]
            users = [
                User(username=f.user_name(), name=f.name(), email=f.email())
                for _ in range(5)
            ]

            session.add_all([*events, *users])
            session.commit()

            for idx in range(5):
                session.add(
                    Registration(
                        username=users[idx % len(users)].username,
                        event_id=events[idx % len(events)].id,
                    )
                )
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
