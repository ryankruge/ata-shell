from shell import *

MODULES_DIRECTORY = "C:/Users/Tomas/Documents/Scripts/ATA/Modules"
TITLE = "ata"

try:
	shell = Shell(TITLE, directory=MODULES_DIRECTORY, standalone=False)
	shell.Spawn()

	while shell.active:
		shell.UpdateShell()
except KeyboardInterrupt:
	shell.Kill()