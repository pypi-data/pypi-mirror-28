#! /usr/bin/env python3

import subprocess
import setup_env.utils as utils

def comment_official():
    new_sources_list = ""

    list_path = "/etc/apt/sources.list"
    official_flag = "ubuntu.com/ubuntu"
    
    with open(list_path) as f:
        for l in f.readlines():
            l = l.strip()
            if len(l) > 0 and l[0] != '#' and l.find(official_flag) != -1:
                l = "#" + l

            new_sources_list += l + "\n"

    with open(list_path, "w") as f:
        f.write(new_sources_list)

def add_tuna():
    dis_code = subprocess.check_output(['lsb_release', '-cs']).decode("utf-8").strip()
    list_path = "/etc/apt/sources.list.d/tuna.list"

    sources_list = """deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ CODE main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ CODE-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ CODE-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ CODE-security main restricted universe multiverse
    """
    
    sources_list = sources_list.replace("CODE", dis_code)
    with open(list_path, "w") as f:
        f.write(sources_list)


def install():
    if not utils.is_root():
        return False, "Need root privileges to run"

    comment_official()
    add_tuna()

    utils.APT_UPDATED = False

    return True, ""
