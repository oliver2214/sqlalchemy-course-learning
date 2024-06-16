from sqlalchemy import insert, text, select, update
from database import sync_engine, async_engine
from models import metadata_obj, workers_table


class SyncCore:
    @staticmethod
    def get_sync_123():
        with sync_engine.connect() as conn:
            res = conn.execute(text("SELECT 1,2,3"))
            print(f"{res.first()=}")
            conn.commit()

    @staticmethod
    def create_tables():
        metadata_obj.drop_all(sync_engine)
        metadata_obj.create_all(sync_engine)

    @staticmethod
    def insert_data():
        with sync_engine.connect() as conn:
            stmt = insert(workers_table).values(
                [
                    {"username": "Aydar"},
                    {"username": "Dima"}
                ]
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_workers():
        with sync_engine.connect() as conn:
            query = select(workers_table)
            result = conn.execute(query)
            workers = result.all()
            print(f"{workers=}")

    @staticmethod
    def update_workers(worker_id: int = 2, new_username: str = "Misha"):
        with sync_engine.connect() as conn:
            stmt = text("UPDATE workers SET username=:new_username WHERE id=:id")
            stmt = stmt.bindparams(new_username=new_username, id=worker_id)
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def update_worker(worker_id: int = 2, new_username: str = "Misha"):
        with sync_engine.connect() as conn:
            query = (
                update(workers_table)
                .values(username=new_username)
                .filter_by(id=worker_id)
            )
            conn.execute(query)
            conn.commit()


class AsyncCore:
    async def get_async_123():
        async with async_engine.connect() as conn:
            res = await conn.execute(text("SELECT 1,2,3"))
            print(f"{res.first()=}")
