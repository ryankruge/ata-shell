#!/usr/bin/python3
from shell import *

MODULES_DIRECTORY = "/home/ryan/Documents/Packages/ata-shell/Modules"
TITLE = "ata"

try:
	shell = Shell(TITLE, directory=MODULES_DIRECTORY, standalone=False)
	shell.Spawn()

	while shell.active:
		shell.UpdateShell()
except KeyboardInterrupt:
	shell.Kill()
