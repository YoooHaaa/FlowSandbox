# coding=utf-8
import hashlib
import os

from mitmproxy import http
from wisbec.date.time import TimeUtil
from wisbec.filesystem.filesystem import FilesystemUtil


def now() -> str:
    return TimeUtil.now('%Y-%m-%d_%H-%M-%S')


def exit_tweezer():
    print("正在退出 tweezer... ...")
    os.kill(os.getpid(), 9)


def convert_to_str_match_regex(src: str) -> str:
    return '^{}$'.format(src.replace('*', '(.*?)'))


def dict_get(d: dict, key: str):
    if key in d:
        return d[key]
    else:
        return None


def get_str_md5(src: str) -> str:
    return hashlib.md5(src.encode('utf-8')).hexdigest()


def save_img(file_name: str, flow: http.HTTPFlow):
    FilesystemUtil.create_directories(os.path.dirname(file_name))
    with open(file_name, 'wb+') as f:
        f.write(flow.response.content)


def save_line(file_name: str, line: str):
    if line == '':
        return
    FilesystemUtil.create_directories(os.path.dirname(file_name))
    with open(file_name, 'a+') as f:
        f.write(line)
        f.write(os.linesep)


def remove_prefix(src: str, prefix: str) -> str:
    if src.startswith(prefix):
        return src[len(prefix):]
    return src
