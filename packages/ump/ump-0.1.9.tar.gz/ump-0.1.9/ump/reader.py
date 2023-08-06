# coding: utf8

"""
读取者
将记录从文件中一条条的取出来，并移动pos
"""

import os
import datetime
import constants
from log import logger
import json


class Reader(object):
    directory = None
    unit_fmt = None
    unit_interval = None

    cache_file_path = None
    cache_file_content = None

    pos_file = None
    # index是下次fetch需要使用的行号，即使文件不存在，那初始化的index=0即可
    # dict(unit='2018011001', index=None)
    pos_unit_time = None
    pos_index = None

    def __init__(self, directory, unit_fmt=None, unit_interval=None):
        self.directory = directory
        self.unit_fmt = unit_fmt or constants.UNIT_FMT
        self.unit_interval = unit_interval or constants.UNIT_INTERVAL

    def fetch(self, end_unit_time=None, init_unit_time=None):
        """
        拉取一条数据
        :param end_unit_time: 闭区间
        :param init_unit_time: 闭区间
        :return:
        """
        self._prepare_pos_file()

        now = datetime.datetime.now()
        # 如果 end_unit_time 不传入的话，就使用上个interval
        if not end_unit_time:
            end_unit_time = datetime.datetime.strptime(
                (now - datetime.timedelta(**self.unit_interval)).strftime(self.unit_fmt),
                self.unit_fmt
            )

        # 可以强制指定开始时间，但是仅当pos没有记录时有效
        # 否则就会设置为和end_unit_time一样
        if not init_unit_time:
            init_unit_time = end_unit_time

        if self.pos_unit_time is None:
            # 说明第一次生成
            self.pos_unit_time = init_unit_time
            self.pos_index = 0

        if self.pos_unit_time > end_unit_time:
            # 已经超过了end_unit_time
            logger.debug('post_unit_time: %s, end_unit_time: %s', self.pos_unit_time, end_unit_time)
            return None

        while True:
            # 从pos开始的文件开始寻找
            unit = self.pos_unit_time.strftime(self.unit_fmt)
            full_file_path = os.path.join(self.directory, unit)
            full_directory = os.path.dirname(full_file_path)

            if not os.path.exists(full_directory):
                os.makedirs(full_directory)

            if os.path.exists(full_file_path):
                # 文件存在
                # 如果不是缓存的文件，那就变成缓存的文件
                if self.cache_file_path != full_file_path:
                    self.cache_file_path = full_file_path
                    with open(self.cache_file_path, 'r') as f:
                        self.cache_file_content = f.readlines()

                for i, line in enumerate(self.cache_file_content):
                    # 这里不用担心，因为0 > None，所以pos_index=None不会有影响
                    if i < self.pos_index:
                        continue

                    # 不管是否是最后一行都+1，可能超过最大行数的
                    self.pos_index = i + 1
                    # 保存下一个位置
                    self._save_pos_file()

                    # 不做解析，因为还要upload。没必要
                    return line

                # 如果整个文件跑完了，都没有发现
                # 那就继续找下一个呗

            if self.pos_unit_time + datetime.timedelta(**self.unit_interval) > end_unit_time:
                # 已经超过了时间了
                logger.debug('post_unit_time: %s, end_unit_time: %s', self.pos_unit_time, end_unit_time)
                return None
            else:
                self.pos_unit_time += datetime.timedelta(**self.unit_interval)
                self.pos_index = 0
                self._save_pos_file()
                # 继续下一个循环

    def _prepare_pos_file(self):
        if self.pos_file:
            return

        pos_file_path = os.path.join(self.directory, constants.POS_FILENAME)
        if not os.path.exists(pos_file_path):
            # 文件不存在
            pos_directory = os.path.dirname(pos_file_path)
            if not os.path.exists(pos_directory):
                os.makedirs(pos_directory)

            with open(pos_file_path, 'w') as f:
                # 创建出来
                pass

        # 读写模式，并且不会清空内容
        self.pos_file = open(pos_file_path, 'r+')
        pos_data = self.pos_file.read()
        pos_values = json.loads(pos_data) if pos_data else dict()

        pos_unit = pos_values.get('unit')
        if pos_unit:
            self.pos_unit_time = datetime.datetime.strptime(pos_unit, self.unit_fmt)

        self.pos_index = pos_values.get('index')

    def _save_pos_file(self):

        pos_values = dict(
            unit=self.pos_unit_time.strftime(self.unit_fmt),
            index=self.pos_index,
        )

        # 清空
        self.pos_file.truncate(0)
        # 一定要seek，否则write多次会报错
        # truncate之后的seek主要解决偏移位置的问题，否则写出来乱七八糟
        self.pos_file.seek(0)
        self.pos_file.write(json.dumps(pos_values))
        self.pos_file.flush()
