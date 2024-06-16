from models import Persons, WorkerORM, ResumeORM, VacancyORM
from database import Base, session_factory, sync_engine, async_session_factory
from sqlalchemy import Integer, and_, cast, func, select
from sqlalchemy.orm import joinedload, selectinload


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
    def insert_resume(title,
                      compensation,
                      workload,
                      worker_id,
                      created_at=None,
                      updated_at=None):
        with session_factory() as session:
            resume = ResumeORM(title=title,
                               compensation=compensation,
                               workload=workload,
                               worker_id=worker_id,
                               created_at=created_at,
                               updated_at=updated_at)
            session.add(resume)
            session.commit()

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

    @staticmethod
    def select_avg_compensation(like_language: str, gt_compenstaion: int):
        '''SELECT round(avg(compensation), 2), workload
            FROM resumes
            where
                title like '%Junior%'
                and compensation > 40000
            group by
                workload'''
        with session_factory() as session:
            query = (
                select(
                    ResumeORM.workload,
                    cast(func.avg(ResumeORM.compensation), Integer).label("avg_compensation"),
                )
                .select_from(ResumeORM)
                .filter(and_(
                    ResumeORM.title.contains(like_language),
                    ResumeORM.compensation > gt_compenstaion,
                ))
                .group_by(ResumeORM.workload)
            )

            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = session.execute(query)
            result = res.all()
            print(result)

    @staticmethod
    def select_resumes():
        with session_factory() as session:
            query = (
                select(
                    ResumeORM.workload,
                    func.avg(ResumeORM.compensation).cast(Integer).label("avg_compensation")
                )
                .filter(and_(
                    ResumeORM.title.contains("Python"),
                    ResumeORM.compensation > 40000
                ))
                .group_by(ResumeORM.workload))

            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = session.execute(query)
            result = res.all()
            print(f"{result=}")

    @staticmethod
    def insert_vacancies():
        with session_factory() as session:
            new_vacancy = VacancyORM(title="Python Developer", compensation=130_000)
            resume_1 = session.get(ResumeORM, 1)
            resume_2 = session.get(ResumeORM, 2)
            resume_1.vacancies_replied.append(new_vacancy)
            resume_2.vacancies_replied.append(new_vacancy)
            session.commit()

    @staticmethod
    def select_full_resumes():
        with session_factory() as session:
            query = (select(ResumeORM)
                     .options(joinedload(ResumeORM.worker))
                     .options(selectinload(ResumeORM.vacancies_replied)))

            res = session.execute(query)
            resumes = res.unique().scalars().all()
            print(f"{resumes=}")

    @staticmethod
    def insert_into_persons():
        with session_factory() as session:
            person = Persons(name="Yellow")
            session.add(person)
            session.commit()


class AsyncORM:
    @staticmethod
    async def async_insert_data():
        async with async_session_factory() as async_session:
            worker_bobr = WorkerORM(username="Bobr")
            worker_vlad = WorkerORM(username="Vlad")
            async_session.add_all([worker_bobr, worker_vlad])
            await async_session.commit()
