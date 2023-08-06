#! /usr/bin/env python3

import os

BASE = os.path.dirname(os.path.realpath(__file__))

APT_UPDATED = False

def is_root():
    return os.getuid() == 0

def apt_install(pkgs = []):
    if len(pkgs) == 0:
        return False, "pkgs is empty"
    
    if not is_root():
        return False, "Need root privileges to run"

    global APT_UPDATED
    if not APT_UPDATED:
        if os.system("apt update") != 0:
            return False, ""
        APT_UPDATED = True

    if os.system("apt install -y " + " ".join(pkgs)) != 0:
        return False, ""
    
    return True, ""

class aptWrapper(object):
    def __init__(self, pkgs = []):
        if type(pkgs) == str:
            pkgs = [pkgs, ]
        self.pkgs = pkgs
    
    def install(self):
        return apt_install(self.pkgs)