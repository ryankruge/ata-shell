#!/usr/bin/python3
# All software written by Tomas. (https://github.com/shelbenheimer/ata-shell)

from shell import Shell

TITLE = "ata"

try:
	shell = Shell(TITLE, standalone=False)
	shell.Spawn()

	while shell.active:
		shell.UpdateShell()
except KeyboardInterrupt:
	shell.Kill()