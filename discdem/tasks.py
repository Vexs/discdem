import asyncio
import datetime
from operator import attrgetter
from sortedcontainers import SortedListWithKey


class TaskProcessor:
    def __init__(self):
        self.referendums = SortedListWithKey(key=attrgetter('expiry_dt'))

    async def start(self):
        while True:
            # for each task which has an expiry_dt past now, run the task
            # TODO: optomize
            split_pt = self.referendums.bisect_key(datetime.datetime.now())
            for ref in self.referendums[:split_pt]:
                if ref.is_passing():
                    await ref.action_func(ref.server, *ref.action_argv)

            self.referendums = SortedListWithKey(self.referendums[split_pt:], key=attrgetter('expiry_dt'))

            await asyncio.sleep(5)

    def add_task(self, referendum):
        self.referendums.add(referendum)


global_task_processor = TaskProcessor()
