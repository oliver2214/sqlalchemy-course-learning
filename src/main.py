import asyncio
import datetime
import os
import sys

from queries.core import SyncCore, AsyncCore
from queries.orm import SyncORM, AsyncORM

sys.path.insert(1, os.path.join(sys.path[0], ".."))


# SyncCore.select_workers()
# SyncCore.update_workers()
# SyncCore.select_workers()

# SyncORM.select_workers()
# SyncORM.update_worker()
# SyncORM.select_workers()

# SyncORM.create_tables()

# SyncORM.insert_data()
# SyncORM.insert_resume(title="Python Junior Developer",
#                       compensation=50_000,
#                       workload="fulltime",
#                       worker_id=1)
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
# SyncORM.insert_into_persons()

SyncORM.select_avg_compensation("Python", 40000)
