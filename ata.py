from shell import *

MODULES_DIRECTORY = "C:/Users/Tomas/Documents/Scripts/ATA/Modules"
COMMANDS = [ 'help', 'exit', 'dismount', 'mount', 'lsmod', 'clear' ]
TITLE = "ata"

def HandleCommand(command, shell):
	match command:
		case 'help':
			shell.Help()
		case 'exit':
			shell.Kill()
		case 'dismount':
			shell.Dismount()
		case 'mount':
			shell.SelectModule()
		case 'lsmod':
			shell.DisplayModules()
		case 'clear':
			shell.Clear()
	shell.command = False

try:
	shell = Shell(COMMANDS, TITLE, directory=MODULES_DIRECTORY, standalone=True)
	shell.Spawn()

	while shell.active:
		shell.UpdateShell()

		if shell.command: HandleCommand(shell.command, shell)
except KeyboardInterrupt:
	shell.Kill()