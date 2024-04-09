from sqlalchemy import Table, String, Integer, MetaData, Column
from database import Base


class WorkerORM(Base):
    __tablename__ = "workers"
    id = Column(Integer, primary_key=True)
    username = Column(String)


metadata_obj = MetaData()

workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String)
)
