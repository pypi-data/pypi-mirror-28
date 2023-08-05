import re
import json
import random
import logging
import aiohttp
import asyncio
from .BaseGetter import BaseGetter


class APIGetter(BaseGetter):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.base_url = self.config.source
        self.retry_count = 0
        self.curr_size = 0
        self.responses = list()
        self.done = False
        self.need_clear = False
        self.page_token = ""
        self.miss_count = 0
        self.total_count = 0

    def init_val(self):
        self.base_url = self.config.source
        self.retry_count = 0
        self.curr_size = 0
        self.responses = list()
        self.done = False
        self.need_clear = False
        self.page_token = ""
        self.miss_count = 0
        self.total_count = 0

    def generate_sub_func(self):
        def sub_func(match):

            return match.group(1) + self.page_token + match.group(3)
        return sub_func

    def update_base_url(self, key="pageToken"):
        if self.base_url[-1] == "/":
            self.base_url = self.base_url[:-1]
        elif self.base_url[-1] == "?":
            self.base_url = self.base_url[:-1]

        key += "="
        if key not in self.base_url:
            if "?" not in self.base_url:
                self.base_url = self.base_url + "?" + key + self.page_token
            else:
                self.base_url = self.base_url + "&" + key + self.page_token
        else:
            self.base_url = re.sub("(" + key + ")(.+?)($|&)", self.generate_sub_func(), self.base_url)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.need_clear and self.responses:
            self.responses.clear()
            self.need_clear = False

        if self.done:
            logging.info("get source done: %s, total get %d items, total filtered: %d items" %
                         (self.config.source, self.total_count, self.miss_count))
            self.init_val()
            raise StopAsyncIteration

        while True:
            try:
                async with self.config.session.get(self.base_url) as resp:
                    text = await resp.text()
                    result = json.loads(text)
            except Exception as e:
                logging.error("%s: %s" % (str(e), self.base_url))
                await asyncio.sleep(random.randint(self.config.random_min_sleep, self.config.random_max_sleep))
                self.retry_count += 1
                if self.retry_count <= self.config.max_retry:
                    continue
                else:
                    # fail
                    logging.error("Give up, Unable to get url: %s, total get %d items, total filtered: %d items" %
                                  (self.base_url, self.total_count, self.miss_count))
                    self.done = True
                    if self.responses:
                        self.need_clear = True
                        return self.responses
                    else:
                        return await self.__anext__()

            if "data" in result:
                # success
                self.retry_count = 0
                origin_length = len(result["data"])
                self.total_count += origin_length

                if self.config.filter:
                    curr_response = [self.config.filter(i) for i in result["data"]]
                    curr_response = [i for i in curr_response if i]
                    self.miss_count += origin_length - len(curr_response)
                else:
                    curr_response = result["data"]
                self.responses.extend(curr_response)
                self.curr_size += len(curr_response)

            # get next page if success, retry if fail
            if "pageToken" in result:
                if not result["pageToken"]:
                    self.done = True
                    if self.responses:
                        self.need_clear = True
                        return self.responses

                self.page_token = str(result["pageToken"])
                self.update_base_url()

            elif "retcode" in result and result["retcode"] == "100002":
                self.done = True
                if self.responses:
                    self.need_clear = True
                    return self.responses

                logging.info("get source done: %s, total get %d items, total filtered: %d items" %
                             (self.config.source, self.total_count, self.miss_count))
                return await self.__anext__()
            else:
                if self.retry_count >= self.config.max_retry:
                    logging.error("Give up, Unable to get url: %s, total get %d items, total filtered: %d items" %
                                  (self.base_url, self.total_count, self.miss_count))
                    self.done = True
                    if self.responses:
                        self.need_clear = True
                        return self.responses

                self.retry_count += 1
                await asyncio.sleep(random.randint(self.config.random_min_sleep, self.config.random_max_sleep))
                return await self.__anext__()

            if self.config.max_limit and self.curr_size > self.config.max_limit:
                self.done = self.need_clear = True
                return self.responses
            elif len(self.responses) >= self.config.per_limit:
                self.need_clear = True
                return self.responses
            elif self.done:
                # buffer has empty data, and done fetching
                return await self.__anext__()

    def __iter__(self):
        raise ValueError("APIGetter must be used with async generator, not normal generator")


class APIBulkGetter(BaseGetter):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.api_configs = self.to_generator(self.config.configs)

        self.pending_tasks = list()
        self.buffers = list()
        self.success_task = 0
        self.curr_size = 0
        self.need_clear = False

    @staticmethod
    def to_generator(items):
        for i in items:
            yield i

    async def fetch_items(self, api_config):
        async for items in APIGetter(api_config):
            self.buffers.extend(items)

    def fill_tasks(self):
        if len(self.pending_tasks) >= self.config.concurrency:
            return

        for api_config in self.api_configs:
            self.pending_tasks.append(self.fetch_items(api_config))
            if len(self.pending_tasks) >= self.config.concurrency:
                return

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.need_clear:
            self.buffers.clear()

        self.fill_tasks()
        while self.pending_tasks:
            done, pending = await asyncio.wait(self.pending_tasks, timeout=self.config.interval)
            self.pending_tasks = list(pending)
            self.success_task += len(done)
            if self.buffers:
                self.need_clear = True
                self.curr_size += len(self.buffers)
                return self.buffers
            else:
                # after interval seconds, no item fetched
                self.fill_tasks()
                logging.info("After %.2f seconds, no new item fetched, current done task: %d, pending tasks: %d" %
                             (float(self.config.interval), self.success_task, len(self.pending_tasks)))
                continue

        logging.info("APIBulkGetter Done, total perform: %d tasks. fetch: %d items" % (self.success_task, self.curr_size))
        raise StopAsyncIteration

    def __iter__(self):
        raise ValueError("APIBulkGetter must be used with async generator, not normal generator")
