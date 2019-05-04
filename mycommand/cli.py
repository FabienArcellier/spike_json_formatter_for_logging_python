#!/usr/bin/python
# coding=utf-8

from __future__ import print_function

import click
from mycommand.utils import hello
from mycommand.cli_logger import get_logger


@click.group()
def cli():
    pass


@click.command('command1')
@click.option('--name')
def command1(name):
    logger = get_logger('mycommand')
    logger.info("arguments", extra={'arguments': {'name': name}})
    hello_name = hello(name)
    print(hello_name)


cli.add_command(command1)

if __name__ == '__main__':
    cli()
