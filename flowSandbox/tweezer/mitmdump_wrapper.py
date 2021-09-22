#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import sys
import os
from mitmproxy.tools.main import mitmdump


def mitmdump_main(*argv):
    sys.argv = [__file__] + list(argv)
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(mitmdump())



