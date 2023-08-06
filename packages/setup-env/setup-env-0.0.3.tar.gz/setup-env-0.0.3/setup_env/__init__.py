from os.path import join

from setup_env.script_wrapper import scriptWrapper
from setup_env.utils import aptWrapper, BASE

# export installer
import setup_env.tuna as tuna

# define installer by wrapper
zsh = aptWrapper("zsh")
vscode = scriptWrapper(join(BASE, "scripts", "install_vscode.sh"))
docker = scriptWrapper(join(BASE, "scripts", "install_docker.sh"))
