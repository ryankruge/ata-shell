from shell import *

MODULES_DIRECTORY = "C:/Users/Tomas/Documents/Scripts/AIO/Modules"
COMMANDS = [ 'help', 'exit', 'dismount', 'mount', 'lsmod', 'ls', 'clear' ]

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
		case 'ls':
			shell.ModuleInformation()
		case 'clear':
			shell.Clear()

try:
	shell = Shell(MODULES_DIRECTORY, COMMANDS)
	shell.Spawn()

	while shell.active:
		shell.UpdateShell()

		if shell.command: HandleCommand(shell.command, shell)
except KeyboardInterrupt:
	shell.Kill()