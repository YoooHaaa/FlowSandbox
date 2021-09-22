# -*- coding: utf-8 -*-
"""
    proxy.py
    ~~~~~~~~
    ⚡⚡⚡ Fast, Lightweight, Pluggable, TLS interception capable proxy server focused on
    Network monitoring, controls & Application development, testing, debugging.

    :copyright: (c) 2013-present by Abhinav Singh and contributors.
    :license: BSD, see LICENSE for more details.
"""
import contextlib
import os
import sys
import time
import logging

from types import TracebackType
from typing import List, Optional, Generator, Any, Type

from proxy.common.utils import bytes_
from proxy.common.flags import Flags
from proxy.core.acceptor import AcceptorPool
from proxy.http.handler import HttpProtocolHandler

logger = logging.getLogger(__name__)


class Proxy:

    def __init__(self, input_args: Optional[List[str]], **opts: Any) -> None:
        self.flags = Flags.initialize(input_args, **opts)
        self.acceptors: Optional[AcceptorPool] = None

    def write_pid_file(self) -> None:
        if self.flags.pid_file is not None:
            with open(self.flags.pid_file, 'wb') as pid_file:
                pid_file.write(bytes_(os.getpid()))

    def delete_pid_file(self) -> None:
        if self.flags.pid_file and os.path.exists(self.flags.pid_file):
            os.remove(self.flags.pid_file)

    def __enter__(self) -> 'Proxy':
        self.acceptors = AcceptorPool(
            flags=self.flags,
            work_klass=HttpProtocolHandler
        )
        self.acceptors.setup()
        self.write_pid_file()
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]) -> None:
        assert self.acceptors
        self.acceptors.shutdown()
        self.delete_pid_file()


@contextlib.contextmanager
def start(
        input_args: Optional[List[str]] = None,
        **opts: Any) -> Generator[Proxy, None, None]:
    """Deprecated.  Kept for backward compatibility.

    New users must directly use proxy.Proxy context manager class."""
    try:
        with Proxy(input_args, **opts) as p:
            yield p
    except KeyboardInterrupt:
        pass


def proxy_entry(
        input_args: Optional[List[str]] = None,
        **opts: Any) -> None:
    try:
        with Proxy(input_args=input_args, **opts):
            # TODO: Introduce cron feature instead of mindless sleep
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        pass

# proxy_entry(input_args=['--port', '8080'])