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

# SyncORM.insert_resume(title="Python Middle Developer",
#                       compensation=330_000,
#                       workload="fulltime",
#                       worker_id=2)

SyncORM.select_resumes()
