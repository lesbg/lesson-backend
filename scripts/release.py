#!/usr/bin/python
import sys
sys.path.insert(0, '../src/lesson')

from controller import config

config.create_config("../examples/lesson.conf")
