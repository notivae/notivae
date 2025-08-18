# -*- coding=utf-8 -*-
r"""

"""
import time
import uuid
import structlog


logger = structlog.getLogger()


class PerformanceTimer:
    def __init__(self):
        self._id = str(uuid.uuid4())
        self._start_time = time.perf_counter()
        self._last_checkpoint = time.perf_counter()
        logger.info("PerformanceTimer started", id=self._id)

    def checkpoint(self, label: str = None):
        now = time.perf_counter()
        since_start = now - self._start_time
        since_last = now - self._last_checkpoint
        self._last_checkpoint = now

        logger.info(f"Checkpoint - since last: {since_last:.6f}s - since start: {since_start:.6f}s", label=label, id=self._id)
