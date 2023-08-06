#! /usr/bin/env python3

import os

import setup_env.utils as utils


class scriptWrapper(object):
    def __init__(self, script_path):
        assert type(script_path) == str
        self.script_path = script_path

    def install(self):
        if not utils.is_root():
            return False, "Need root privileges to run"

        if os.system("bash " + self.script_path) != 0:
            return False, ""

        return True, ""
