import sys, os, platform, importlib

ERRORS = {
	'MODULE_MOUNT_ERROR':     "There was an error whilst attempting to mount a module.",
	'MODULE_DIRECTORY_EMPTY': "There was an error whilst scanning the module directory.",
	'MODULE_PRESENT':         "There is already a module mounted.",
	'NO_MODULE_ERROR':        "There are no modules currently mounted.",
	'DISMOUNT_ERROR':         "There was an error whilst trying to dismount the current module.",
	'INVALID_COMMAND_ERROR':  "Invalid command.",
	'COMMAND_LIST_ERROR':     "Command list is empty or invalid."	
}

class Shell:
	def __init__(self, directory, commands, title, active=False):
		self.active   = active
		self.title    = title

		self.command = ""
		self.commands = commands

		self.module    = None
		self.platform  = platform.system()
		self.directory = directory
		self.modules   = []

	def Spawn(self):
		if not self.CheckCommands():
			print(ERRORS['COMMAND_LIST_ERROR'])
			return
		if not self.GatherModules():
			print(ERRORS['MODULE_DIRECTORY_EMPTY'])
			return

		sys.path.append(self.directory)
		self.active = True

	def Kill(self):
		self.active = False
		sys.exit()

	def UpdateShell(self):
		read = input(f"{self.title}> ").lower()

		if not self.EvaluateCommand(read):
			print(ERRORS['INVALID_COMMAND_ERROR'])
			return
		self.command = read

	def SelectModule(self):
		if not self.CheckModules(): return
		if self.module:
			print(ERRORS['MODULE_PRESENT'])
			return

		self.DisplayModules()
		
		try:
			selection = int(input("select> "))
			
			if not self.CheckModule(self.modules[selection]):
				print(ERRORS['MODULE_MOUNT_ERROR'])
				return
			if not self.Mount(self.modules[selection]):
				print(ERRORS['MODULE_MOUNT_ERROR'])
				return
		except:
			print(ERRORS['MODULE_MOUNT_ERROR'])
			return

	def DisplayModules(self):
		if not self.CheckModules():
			print(ERRORS['MODULE_DIRECTORY_EMPTY'])
			return

		for module in range(0, len(self.modules)):
			print(f"{module}. {self.modules[module].upper()}")

	def EvaluateCommand(self, command):
		if command not in self.commands:
			return False
		return True

	def CheckCommands(self):
		if not self.commands:
			return False
		return True

	def Dismount(self, title):
		if not self.module:
			print(ERRORS['NO_MODULE_ERROR'])
			return False

		try:
			del sys.modules[self.module]
			print(f"Dismounted {self.module}.")
		except:
			print(ERRORS['DISMOUNT_ERROR'])
			return False

		self.title = title
		self.module = None

		return True

	def CheckModule(self, module):
		if module == self.module:
			return False
		if self.module:
			return False
		return True

	def CheckModules(self):
		if not self.modules:
			return False
		return True

	def GatherModules(self):
		files = os.listdir(self.directory)
		if not files: return False

		for file in range(0, len(files)):
			path = os.path.splitext(files[file])
			if not path[len(path) - 1] == '.py':
				continue
			self.modules.append(path[0])

		if not self.CheckModules():
			self.modules = []
			return False
		return True
	
	def Mount(self, module):
		if not self.CheckModule(module): return False

		try:
			imported = importlib.import_module(module)
			print("Mounted module.")
		except:
			print(ERRORS['MODULE_MOUNT_ERROR'])
			return False

		self.title = module
		self.module = module
		return True

	def ModuleInformation(self):
		if not self.module:
			print(ERRORS['NO_MODULE_ERROR'])
			return
		print(f"The {self.module} module is currently loaded.")

	def Clear(self):
		match self.platform:
			case "Windows":
				os.system("cls")
			case "Linux":
				os.system("clear")

	def Help(self, message):
		print(message)