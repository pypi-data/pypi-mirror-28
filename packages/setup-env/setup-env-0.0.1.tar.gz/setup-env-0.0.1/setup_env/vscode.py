#! /usr/bin/env python3

import os

from setup_env import utils


def install():
    if not utils.is_root():
        return False, "Need root privileges to run"
    
    script_path = os.path.join(utils.BASE, "scripts", "install_vscode.sh")

    if os.system("bash " + script_path) != 0:
        return False, ""
    
    return True, ""

if __name__ == "__main__":
    print(install())
