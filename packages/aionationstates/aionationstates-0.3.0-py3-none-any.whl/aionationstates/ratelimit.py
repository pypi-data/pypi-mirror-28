"""Compliance with NationStates' API and web rate limits."""

import time
import asyncio
from collections import deque

from aionationstates.utils import logger


def _create_ratelimiter(requests, per):
    request_times = deque([0], maxlen=requests)
    portion_duration = per * 1.05  # some wiggle room

    def decorator(func):
        async def wrapper(*args, **kwargs):
            while True:
                right_now = time.perf_counter()
                since_portion_started = right_now - request_times[0]
                if since_portion_started < portion_duration:
                    to_sleep = portion_duration - since_portion_started
                    logger.debug(f'waiting {to_sleep} seconds on ratelimiter')
                    await asyncio.sleep(to_sleep)
                else:
                    request_times.append(right_now)
                    return await func(*args, **kwargs)
        return wrapper
    return decorator


# "API Rate Limit: 50 requests per 30 seconds."
# https://www.nationstates.net/pages/api.html#ratelimits
api = _create_ratelimiter(requests=50, per=30)

# "Scripts must send no more than 10 requests per minute."
# https://forum.nationstates.net/viewtopic.php?p=16394966#p16394966
web = _create_ratelimiter(requests=10, per=60)
