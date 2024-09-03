import datetime
import enum
from typing import Annotated
from sqlalchemy import CheckConstraint, ForeignKey, Index, Table, String, Integer, MetaData, Column, text, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base, str_16

intpk = Annotated[int, mapped_column(Integer, primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.utcnow)]
str_50 = Annotated[str, 50]


class ReaderORM(Base):
    __tablename__ = "reader"

    reader_id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(64))
    surname: Mapped[str] = mapped_column(String(128))
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    email: Mapped[str] = mapped_column(String(128))
    password: Mapped[str] = mapped_column(String(128))
    balance: Mapped[float] = mapped_column(Numeric)

    books: Mapped[list["BookORM"]] = relationship(
        back_populates="readers",
        secondary="reservation",
    )

    __table_args__ = (
        CheckConstraint("balance >= 0", name="balance_constraint"),
        CheckConstraint("age >= 0", name="age_constraint"),
        Index("reader_email_index", "email"),
    )


class BookORM(Base):
    __tablename__ = "book"

    book_id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(256), nullable=True)
    genre: Mapped[str] = mapped_column(String(128), nullable=True)
    year_publishing: Mapped[str] = mapped_column(String(4), nullable=True)
    page_count: Mapped[int]
    book_price: Mapped[float] = mapped_column(Numeric)

    readers: Mapped[list["ReaderORM"]] = relationship(
        back_populates="books",
        secondary="reservation",
    )

    __table_args__ = (
        CheckConstraint("book_price >= 0", name="book_price_constraint"),
        CheckConstraint("page_count >= 0", name="page_count_constraint"),
        Index("book_title_index", "title"),
    )


class ReservationORM(Base):
    __tablename__ = "reservation"

    reservation_id: Mapped[intpk]
    book_id: Mapped[int] = mapped_column(
        ForeignKey("book.book_id", ondelete="CASCADE"),
        primary_key=True,
    )
    reader_id: Mapped[int] = mapped_column(
        ForeignKey("reader.reader_id", ondelete="CASCADE"),
        primary_key=True,
    )


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
    profiles: Mapped[list["Profiles"]] = relationship(back_populates="person")

    books: Mapped[list["Books"]] = relationship(
        back_populates="persons",
        secondary="book_reservations"
    )

    profiles_gr_30: Mapped[list["Profiles"]] = relationship(
        back_populates="person",
        primaryjoin="and_(Persons.id==Profiles.person_id, Profiles.age==47)"
    )

    __table_args__ = (
        Index("name_index", "name"),
    )


class Profiles(Base):
    __tablename__ = "profiles"

    id: Mapped[intpk]
    age: Mapped[int]
    person_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
    person: Mapped["Persons"] = relationship(back_populates="profiles")

    __table_args__ = (
        CheckConstraint("age >= 0 AND age <= 130", name="age_constraint"),
    )


class Books(Base):
    __tablename__ = "books"

    id: Mapped[intpk]
    title: Mapped[str]

    persons: Mapped[list["Persons"]] = relationship(
        back_populates="books",
        secondary="book_reservations",
    )


class Reservations(Base):
    __tablename__ = "book_reservations"

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id", ondelete="CASCADE"),
        primary_key=True,)
    person_id: Mapped[int] = mapped_column(
        ForeignKey("persons.id", ondelete="CASCADE"),
        primary_key=True,)


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

    __table_args__ = (
        Index("title_index", "title"),
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
