#!/usr/bin/python3
from shell import *

TITLE = "ata"

try:
	shell = Shell(TITLE, standalone=False)
	shell.Spawn()

	while shell.active:
		shell.UpdateShell()
except KeyboardInterrupt:
	shell.Kill()