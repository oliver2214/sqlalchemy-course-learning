from models import WorkerORM
from database import Base, session_factory, sync_engine, async_session_factory


def create_tables():
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)


def insert_data():
    worker_bobr = WorkerORM(username="Bobr")
    worker_vlad = WorkerORM(username="Vlad")
    with session_factory() as session:
        session.add_all([worker_bobr, worker_vlad])
        session.commit()


async def async_insert_data():
    async with async_session_factory() as async_session:
        worker_bobr = WorkerORM(username="Bobr")
        worker_vlad = WorkerORM(username="Vlad")
        async_session.add_all([worker_bobr, worker_vlad])
        await async_session.commit()
