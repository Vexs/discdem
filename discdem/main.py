import asyncio
from client import client
import sys

from tasks import global_task_processor

import handlers


if __name__ == '__main__':

    # fetch passed token
    token_fn = sys.argv[1]
    with open(token_fn) as token_file:
        token_str = token_file.read().rstrip()

    # start client listening loop and task runner loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(
        client.start(token_str),
        global_task_processor.start()
    ))
