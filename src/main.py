import asyncio
import os
import sys
from queries.orm import async_insert_data, create_tables

sys.path.insert(1, os.path.join(sys.path[0], ".."))

create_tables()
# insert_data()

asyncio.run(async_insert_data())
