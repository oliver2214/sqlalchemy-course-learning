import asyncio
import os
import sys

from queries.core import SyncCore, AsyncCore
from queries.orm import SyncORM, AsyncORM

sys.path.insert(1, os.path.join(sys.path[0], ".."))


# SyncCore.select_workers()
# SyncCore.update_workers()
# SyncCore.select_workers()

SyncORM.select_workers()
SyncORM.update_worker()
SyncORM.select_workers()
