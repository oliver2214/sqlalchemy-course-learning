import datetime
import enum
from typing import Annotated
from sqlalchemy import ForeignKey, Table, String, Integer, MetaData, Column, text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
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


class ResumeORM(Base):
    __tablename__ = "resumes"
    id: Mapped[intpk]
    title: Mapped[str_50]
    compensation: Mapped[int | None]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


metadata_obj = MetaData()

workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String)
)
