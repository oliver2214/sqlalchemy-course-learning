import datetime
import enum
from sqlalchemy import ForeignKey, Table, String, Integer, MetaData, Column, text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Workload(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"


class WorkerORM(Base):
    __tablename__ = "workers"
    id = Column(Integer, primary_key=True)
    username = Column(String)


class ResumesOrm(Base):
    __tablename__ = "resumes"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    compensation: Mapped[int | None]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow
    )


metadata_obj = MetaData()

workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String)
)
