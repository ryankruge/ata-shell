import sys, os, platform, importlib

ERRORS = {
	'MODULE_MOUNT_ERROR':      "There was an error whilst attempting to mount a module.",
	'MODULE_DIRECTORY_EMPTY':  "There was an error whilst scanning the module directory.",
	'MODULE_PRESENT':          "There is already a module mounted.",
	'NO_MODULE_ERROR':         "There are no modules currently mounted.",
	'DISMOUNT_ERROR':          "There was an error whilst trying to dismount the current module.",
	'INVALID_COMMAND_ERROR':   "Invalid command.",
	'INVALID_DIRECTORY_ERROR': "Please check that the modules directory is valid.",
	'COMMAND_LIST_ERROR':      "Command list is empty or invalid.",
	'STANDALONE_SHELL_ERROR':  "This is a standalone shell."
}

DIALOGUE = """HELP     - Prints this display.
EXIT     - Exits this shell environment.
CLEAR    - Clears the current text buffer.
MOUNT    - Will present a list of all mountable modules.
LSMOD    - Will list all available modules.
DISMOUNT - Dismount the currently loaded module."""

DEFAULT_DIRECTORY = "C:/Users"
DEFAULT_TITLE = 'ata'
DEFAULT_COMMANDS = [ 'help', 'exit', 'dismount', 'mount', 'lsmod', 'clear' ]

class Shell:
	def __init__(self, title, dialogue=DIALOGUE, directory=DEFAULT_DIRECTORY, standalone=False):
		self.title      = title
		self.directory  = directory
		self.standalone = standalone
		self.dialogue = dialogue

		self.commands = {
			'help': self.Help,
			'exit': self.Kill,
			'dismount': self.Dismount,
			'mount': self.SelectModule,
			'lsmod': self.DisplayModules,
			'clear': self.Clear
		}

		self.active   = False
		self.command  = ""
		self.platform = platform.system()

		self.module  = None
		self.modules = []

	def Spawn(self):
		self.active = True
		if not self.standalone: sys.path.append(self.directory)

	def Kill(self):
		self.active = False
		sys.exit()

	def Help(self):
		print(f"Commands:\n{self.dialogue}")

	def UpdateShell(self):
		read = input(f"{self.title}> ").lower()

		if self.EvaluateCommand(read):
			return
		self.command = read

	def SelectModule(self):
		if self.standalone:
			print(ERRORS['STANDALONE_SHELL_ERROR'])
			return False
		self.DisplayModules()

		try:
			selection = int(input("select> "))

			module = self.modules[selection]

			if not self.CheckModule(module): return False
			if not self.Mount(module): return False
			
			print("Module mounted.")
		except Exception as error:
			print(error)
			return False
		return True

	def DisplayModules(self):
		if self.standalone:
			print(ERRORS['STANDALONE_SHELL_ERROR'])
			return False

		self.GatherModules()
		for module in range(0, len(self.modules)):
			print(f"{module}. {self.modules[module].upper()}")

	def GatherModules(self):
		if self.standalone:
			print(ERRORS['STANDALONE_SHELL_ERROR'])
			return False

		try:
			files = os.listdir(self.directory)
		except:
			return False

		self.modules = []
		for file in range(0, len(files)):
			path = os.path.splitext(files[file])
			if not path[len(path) - 1] == '.py':
				continue
			self.modules.append(path[0])

		if not self.modules:
			return False
		return True

	def Dismount(self):
		if self.standalone:
			print(ERRORS['STANDALONE_SHELL_ERROR'])
			return False
		if not self.module:
			print(ERRORS['NO_MODULE_ERROR'])
			return False

		del sys.modules[self.module]
		self.title = DEFAULT_TITLE
		self.module = None

	def Mount(self, module):
		if not self.CheckModule(module): return False

		try:
			imported = importlib.import_module(module)
			imported.Initialise()
			self.Kill()
		except Exception as error:
			print(error)
			return False
		return True

	def Clear(self):
		match self.platform:
			case "Windows":
				os.system("cls")
			case "Linux":
				os.system("clear")

	def CheckModule(self, module):
		if module == self.module:
			return False
		if self.module:
			return False
		return True

	def EvaluateCommand(self, command):
		if not command in self.commands: return False

		self.commands[command]()
		return True