from models import WorkerORM
from database import Base, session_factory, sync_engine, async_session_factory
from sqlalchemy import select


class SyncORM:
    @staticmethod
    def create_tables():
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)

    @staticmethod
    def insert_data():
        worker_bobr = WorkerORM(username="Bobr")
        worker_vlad = WorkerORM(username="Vlad")
        with session_factory() as session:
            session.add_all([worker_bobr, worker_vlad])
            session.commit()

    @staticmethod
    def select_workers():
        with session_factory() as session:
            query = select(WorkerORM)
            result = session.execute(query)
            workers = result.scalars().all()
            print(f"{workers=}")

    @staticmethod
    def select_worker():
        with session_factory() as session:
            worker = session.get(WorkerORM, {"id": 1})
            print(f"{worker.username=}")

    @staticmethod
    def update_worker():
        with session_factory() as session:
            worker = session.get(WorkerORM, 2)
            worker.username = worker.username + "123"
            session.refresh(worker)
            session.commit()


class AsyncORM:
    @staticmethod
    async def async_insert_data():
        async with async_session_factory() as async_session:
            worker_bobr = WorkerORM(username="Bobr")
            worker_vlad = WorkerORM(username="Vlad")
            async_session.add_all([worker_bobr, worker_vlad])
            await async_session.commit()
