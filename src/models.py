import datetime
import enum
from typing import Annotated
from sqlalchemy import ForeignKey, Table, String, Integer, MetaData, Column, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base, str_16

intpk = Annotated[int, mapped_column(Integer, primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.utcnow)]
str_50 = Annotated[str, 50]


class Workload(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"


class WorkerORM(Base):
    __tablename__ = "workers"
    id: Mapped[intpk]
    username: Mapped[str]

    resumes: Mapped[list["ResumeORM"]] = relationship(
        back_populates="worker",
    )


class Persons(Base):
    __tablename__ = "persons"

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str_16]
    profiles: Mapped[list["Profiles"]] = relationship()


class Profiles(Base):
    __tablename__ = "profiles"

    id: Mapped[intpk]
    age: Mapped[int]
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    person: Mapped["Persons"] = relationship()


class ResumeORM(Base):
    __tablename__ = "resumes"
    id: Mapped[intpk]
    title: Mapped[str_50]
    compensation: Mapped[int | None]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    worker: Mapped[WorkerORM] = relationship(
        back_populates="resumes"
    )

    vacancies_replied: Mapped[list["VacancyORM"] | None] = relationship(
        back_populates="resumes_replied",
        secondary="vacancies_replies"
    )


class VacancyORM(Base):
    __tablename__ = "vacancies"
    id: Mapped[intpk]
    title: Mapped[str_50]
    compensation: Mapped[int | None]

    resumes_replied: Mapped[list["ResumeORM"] | None] = relationship(
        back_populates="vacancies_replied",
        secondary="vacancies_replies"
    )


class VacanciesReplyORM(Base):
    __tablename__ = "vacancies_replies"
    resume_id: Mapped[int] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        primary_key=True
    )
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancies.id", ondelete="CASCADE"),
        primary_key=True
    )





















metadata_obj = MetaData()

workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String)
)
