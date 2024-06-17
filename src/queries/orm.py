from models import Persons, Profiles, WorkerORM, ResumeORM, VacancyORM
from database import Base, session_factory, sync_engine, async_session_factory
from sqlalchemy import Integer, and_, cast, func, select
from sqlalchemy.orm import joinedload, selectinload, aliased


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
    def insert_worker(username: str):
        worker = WorkerORM(username=username)
        with session_factory() as session:
            session.add(worker)
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
            worker = session.get(WorkerORM, 1)
            print(f"{worker.username=}")

    @staticmethod
    def select_workers():
        with session_factory() as session:
            workers = select(WorkerORM)
            result = session.execute(workers)
            workers = result.all()
            print(f"{workers=}")

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

    @staticmethod
    def join_cte_subquery_window_func(programming_language:str = "Python"):
        '''WITH
                helper2 AS (
                    SELECT
                        *,
                        compensation - avg_compensation_by_workload AS compensation_diff
                    FROM (
                            SELECT
                                w.username, r.compensation, workload, avg(r.compensation) OVER (
                                    PARTITION BY
                                        workload
                                )::int AS avg_compensation_by_workload
                            FROM resumes r
                                JOIN workers w ON w.id = r.worker_id
                        ) helper1
                )
            SELECT *
            FROM helper2
            ORDER BY compensation_diff DESC'''
        with session_factory() as session:
            r = aliased(ResumeORM)
            w = aliased(WorkerORM)
            subq = (
                select(
                    r,
                    w,
                    func.avg(r.compensation).over(partition_by=r.workload).cast(Integer).label("avg_compensation_by_workload"),
                )
                .select_from(r)
                .join(w, w.id == r.worker_id)
                .subquery("helper1")
            )

            cte = (
                select(
                    subq.c.worker_id,
                    subq.c.username,
                    subq.c.compensation,
                    subq.c.workload,
                    subq.c.avg_compensation_by_workload,
                    (subq.c.compensation - subq.c.avg_compensation_by_workload).label("compensation_diff")
                )
                .cte("helper2")
            )

            query = (
                select(cte)
                .order_by(cte.c.compensation_diff.desc())
            )

            result = session.execute(query)
            result = result.all()

            print(f"{result=}")

    @staticmethod
    def insert_persons_profiles():
        with session_factory() as session:
            person = Persons(name="Aydar")
            profile1 = Profiles(age=27, person_id=2)
            profile2 = Profiles(age=47, person_id=2)

            session.add_all([person, profile1, profile2])
            session.commit()


    @staticmethod
    def select_person_with_lazy_relationship():
        with session_factory() as session:
            query = select(Persons)

            result = session.execute(query)
            persons = result.scalars().all()

            profiles1 = persons[0].profiles
            print(f"{profiles1=}")

            profiles2 = persons[1].profiles
            print(f"{profiles2=}")

    @staticmethod
    def select_person_with_joined_relationship():
        with session_factory() as session:
            query = (
                select(Persons)
                .options(joinedload(Persons.profiles))
            )

            result = session.execute(query)
            persons = result.unique().scalars().all()

            profiles1 = persons[0].profiles
            print(f"{profiles1=}")

            profiles2 = persons[1].profiles
            print(f"{profiles2=}")

    @staticmethod
    def select_person_with_selectinload_relationship():
        with session_factory() as session:
            query = (
                select(Persons)
                .options(selectinload(Persons.profiles))
            )

            result = session.execute(query)
            persons = result.unique().scalars().all()

            profiles1 = persons[0].profiles
            print(f"{profiles1=}")

            profiles2 = persons[1].profiles
            print(f"{profiles2=}")








class AsyncORM:
    @staticmethod
    async def async_insert_data():
        async with async_session_factory() as async_session:
            worker_bobr = WorkerORM(username="Bobr")
            worker_vlad = WorkerORM(username="Vlad")
            async_session.add_all([worker_bobr, worker_vlad])
            await async_session.commit()
