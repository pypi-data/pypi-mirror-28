import json
import logging
from .BaseGetter import BaseGetter


class JsonGetter(BaseGetter):
    def __init__(self, config):
        super().__init__(self)
        self.config = config
        self.responses = list()
        self.line_num = 0
        self.curr_size = 0
        self.need_clear = False
        self.done = False
        self.f_in = open(self.config.filename, self.config.mode, encoding=self.config.encoding)

    def init_val(self):
        self.responses = list()
        self.line_num = 0
        self.curr_size = 0
        self.need_clear = False
        self.done = False
        self.f_in.seek(0, 0)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.need_clear:
            self.responses.clear()
            self.need_clear = False

        if self.done:
            logging.info("get source done: %s" % (self.config.filename,))
            self.init_val()
            raise StopAsyncIteration

        for line in self.f_in:
            self.line_num += 1
            try:
                json_obj = json.loads(line)
            except json.decoder.JSONDecodeError:
                logging.error("JSONDecodeError. give up. line: %d" % (self.line_num, ))
                continue

            self.responses.append(json_obj)
            self.curr_size += 1

            if len(self.responses) > self.config.per_limit:
                self.need_clear = True
                return self.responses

            if self.config.max_limit and self.curr_size > self.config.max_limit:
                self.need_clear = self.done = True
                return self.responses

        self.need_clear = self.done = True
        if self.responses:
            return self.responses

        logging.info("get source done: %s" % (self.config.filename,))
        self.init_val()
        raise StopAsyncIteration

    def __iter__(self):
        for line in self.f_in:
            self.line_num += 1
            try:
                json_obj = json.loads(line)
            except json.decoder.JSONDecodeError:
                logging.error("JSONDecodeError. give up. line: %d" % (self.line_num, ))
                continue

            self.responses.append(json_obj)
            self.curr_size += 1

            if len(self.responses) > self.config.per_limit:
                yield self.responses
                self.responses.clear()

            if self.config.max_limit and self.curr_size > self.config.max_limit:
                yield self.responses
                self.responses.clear()
                break

        if self.responses:
            yield self.responses
        self.init_val()
        logging.info("get source done: %s" % (self.config.filename,))

    def __del__(self):
        self.f_in.close()
