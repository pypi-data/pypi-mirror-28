# -*- coding: utf8 -*-

import click
import datetime


class UpdateTimer(object):
    def __init__(self, interval=1.):
        self.__interval = interval
        self.__start_time = None

    def can_update(self):
        now = datetime.datetime.utcnow()
        if self.__start_time is None or (now - self.__start_time).total_seconds() > self.__interval:
            self.__start_time = now
            return True

        return False


class PrintStatus(object):
    def __init__(self, nl_on_clone=True):
        self.__update_timer = UpdateTimer()
        self.__first_status = True
        self.__last_printed_msg = None
        self.__last_msg = None
        self.__nl_on_clone = nl_on_clone

    def close(self):
        if self.__last_msg is not None and self.__last_msg != self.__last_printed_msg:
            self.__print_status(True, self.__last_msg)

        if self.__nl_on_clone:
            click.echo('\n', nl=False)

    def __get_formatted_message(self, msg, *args, **kwargs):
        formatted_msg = ''

        if self.__last_printed_msg:
            spaces = len(self.__last_printed_msg)
            formatted_msg += '\r' + (' ' * spaces) + '\r'

        formatted_msg += msg.format(*args, **kwargs)

        if self.__first_status:
            formatted_msg = '\n' + formatted_msg

        return formatted_msg

    def __print_status(self, force, msg, *args, **kwargs):
        formatted_msg = self.__get_formatted_message(msg, *args, **kwargs)

        self.__last_msg = formatted_msg.strip()

        if self.__update_timer.can_update() or force:
            click.echo(formatted_msg, nl=False)
            self.__last_printed_msg = self.__last_msg

        return True

    def print_status(self, msg, *args, **kwargs):
        printed_status = self.__print_status(False, msg, *args, **kwargs)

        if self.__first_status and printed_status:
            self.__first_status = False
