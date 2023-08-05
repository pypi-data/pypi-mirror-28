#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : base_worker.py
@Created       : 22/12/2017
"""
import asyncio
import logging

from aiospider import AIOSpider
from aiospider.models.job import RequestJob, ResponseJob
from aiospider.tools.bloom_tools import BloomFilter
from aiospider.tools.job_queue import JobQueue


class Worker:
    keys = {}
    name = 'base'
    worker = 'base'
    url_regex = None
    method = None
    filter_trigger = False
    params = {}
    require_params = []
    headers = {}

    def __init__(self, app=None):
        """

        :param app:
        """
        self._app = app

    @property
    def app(self):
        if not self._app:
            self._app = AIOSpider(None)
        return self._app

    async def analyze(self, req_job, content):
        # do something with request success
        pass

    @staticmethod
    def parser(data: dict):
        return data

    @staticmethod
    def pre_handle(resp_job: ResponseJob):
        return resp_job.success, resp_job.content

    async def fail(self, resp_job):
        # do something with request fail
        await resp_job.request_job.send()

    async def _per_handle(self, resp_job: ResponseJob):
        success, content = self.pre_handle(resp_job)
        if success:
            return await self.analyze(resp_job.request_job, content=self.parser(content))
        else:
            await self.fail(resp_job)

    @classmethod
    async def request_builder(cls, keys: dict, params=None, headers=None, data=None, identity=None,
                              redirect_times=None,
                              allow_redirect=None,
                              proxy=None,
                              cookies=None):
        url = cls.url_regex
        for key, value in keys.items():
            url = url.replace('{%s}' % key, str(value))

        if not params:
            params = {}
        for must in cls.require_params:
            if must not in params:
                raise ValueError()

        if cls.filter_trigger:
            if await cls.filter(url, keys, params):
                return
        if isinstance(params, dict):
            cls.params.update(params)
        if headers:
            cls.headers.update(headers)
        return RequestJob(worker=cls.worker, url=url, method=cls.method, params=cls.params, data=data,
                          identity=identity, headers=cls.headers,
                          keys=keys,
                          cookies=cookies, proxy=proxy, name=cls.name, allow_redirect=allow_redirect,
                          redirect_times=redirect_times)

    @classmethod
    def req_queue_name(cls):
        return f'{cls.name}:{cls.worker}:request'

    @property
    def req_queue(self):
        return JobQueue(self.app, name=self.req_queue_name())

    @classmethod
    def resp_queue_name(cls):
        return f'{cls.name}:{cls.worker}:response'

    @property
    def resp_queue(self):
        return JobQueue(self.app, name=self.resp_queue_name())

    @classmethod
    def filter_name(cls):
        return f'{cls.name}:{cls.worker}:filter'

    @classmethod
    async def filter(cls, url, keys, params, *args, **kwargs):
        if params:
            key = f'{url}{sorted(params.items())}'
        else:
            key = f'{url}'
        return BloomFilter(cls.app, name=cls.filter_name()).exists(key)

    async def start(self):
        print(f'{self.name}:{self.worker}:Start')
        while True:
            try:
                queue = self.resp_queue
                content = await queue.get()
                if content:
                    resp_job = ResponseJob.from_json(content.decode())
                    await self._per_handle(resp_job)
                else:
                    await asyncio.sleep(1)

            except Exception as e:
                logging.exception(e)
