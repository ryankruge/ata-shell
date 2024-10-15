from shell import *

HELP_MESSAGE = """Commands:
HELP      - Prints this display.
EXIT      - Exits this shell environment.
CLEAR     - Clears the current text buffer.
MOUNT     - Will present a list of all mountable modules.
LS        - Presents information about the current module.
LSMOD     - Will list all available modules.
DISMOUNT  - Dismount the currently loaded module."""

MODULES_DIRECTORY = "C:/Users/Tomas/Documents/Scripts/AIO/Modules"
COMMANDS = [ 'help', 'exit', 'dismount', 'mount', 'lsmod', 'ls', 'clear' ]
TITLE = "ata"

def HandleCommand(command, shell):
	match command:
		case 'help':
			shell.Help(HELP_MESSAGE)
		case 'exit':
			shell.Kill()
		case 'dismount':
			shell.Dismount(TITLE)
		case 'mount':
			shell.SelectModule()
		case 'lsmod':
			shell.DisplayModules()
		case 'ls':
			shell.ModuleInformation()
		case 'clear':
			shell.Clear()

try:
	shell = Shell(MODULES_DIRECTORY, COMMANDS, TITLE)
	shell.Spawn()

	while shell.active:
		shell.UpdateShell()

		if shell.command: HandleCommand(shell.command, shell)
except KeyboardInterrupt:
	shell.Kill()