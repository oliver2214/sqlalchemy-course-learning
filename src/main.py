import asyncio
import datetime
import os
import sys

from queries.core import SyncCore, AsyncCore
from queries.orm import SyncORM, AsyncORM

sys.path.insert(1, os.path.join(sys.path[0], ".."))


# SyncORM.select_workers()
# SyncORM.update_worker()
# SyncORM.select_workers()

SyncORM.create_tables()

# SyncORM.insert_resume(title="Java Senior Developer",
#                       compensation=400_000,
#                       workload="fulltime",
#                       worker_id=3)
# SyncORM.insert_resume(title="Python Middle Developer",
#                       compensation=150_000,
#                       workload="fulltime",
#                       worker_id=2)
# SyncORM.insert_resume(title="Python Senior Developer",
#                       compensation=350_000,
#                       workload="fulltime",
#                       worker_id=2)
# SyncORM.insert_resume(title="Python Middle Developer",
#                       compensation=150_000,
#                       workload="parttime",
#                       worker_id=1)
# SyncORM.insert_vacancies()
# SyncORM.select_full_resumes()

# SyncORM.select_resumes()

# SyncORM.create_tables()
# SyncORM.join_cte_subquery_window_func()

# SyncORM.select_person_with_lazy_relationship()
# SyncORM.select_person_with_joined_relationship()
# SyncORM.select_person_with_selectinload_relationship()

# SyncORM.insert_persons_profiles()
# SyncORM.add_book_reservations()
# SyncORM.select_book_reservations()
