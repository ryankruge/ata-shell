from scapy.all import ARP, srp, Ether, get_if_list
import sys, colorama, socket, importlib

class Discovery:
	def __init__(self, target, interface, required):
		self.target = target
		self.interface = target
		self.required = required

	def GetHosts(self):
		packet = Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(pdst=self.target)
		replies = srp(packet, iface=self.interface, timeout=1, verbose=False)[0]

		if not replies: return []

		addresses = []
		for reply in range(0, len(replies)):
			addresses.append(replies[reply][1].psrc)[0]
		return addresses

	def ReverseDNS(self, host):
		try:
			hostname = socket.gethostbyaddr(host)[0]
			return hostname
		except:
			return "N/A"

	def PrintMessage(self, message):
		print("{}[{}*{}]{} {}").format(
			colorama.Style.DIM,
			colorama.Style.RESET_ALL,
			colorama.Style.DIM,
			colorama.Style.RESET_ALL,
			message
		)

	def VerifyRequired(self, arguments):
		for argument in required:
			if argument not in arguments:
				return False
		return True

HELP = """Commands:
HELP      - Prints this display.
TARGET    - Used to determine the subnet.
INTERFACE - Used to select a network interface."""

SHELL_DIRECTORY = "C:/Users/Tomas/Documents/Scripts/ATA"
TITLE = 'discovery'
COMMANDS = [ 'help', 'target', 'interface', 'start' ]


def HandleCommand(command, shell):
	match command:
		case 'help':
			print("Helping")
			shell.Help()
	shell.command = None

def Initialise():
	try:
		sys.path.append(SHELL_DIRECTORY)
		library = importlib.import_module('shell')

		shell = library.Shell(COMMANDS, TITLE, dialogue=HELP, standalone=True)
		shell.Spawn()

		while shell.active:
			shell.UpdateShell()

			if shell.command: HandleCommand(shell.command, shell)
	except Exception as error:
		print(error)
		return

# def PopulateParameters(arguments, flags, dictionary):
# 	try:
# 		temporary = dictionary
# 		for argument in range(0, len(arguments)):
# 			if arguments[argument] in flags:
# 				dictionary[arguments[argument]] = arguments[argument + 1]
# 		return temporary
# 	except TypeError:
# 		PrintMessage("There was an error whilst populating the parameter list.")
# 		sys.exit()

# REQUIRED = [ '-t', '-i' ]
# CONFIGURABLE = [ '-t', '-i' ]

# HELP_MESSAGE = f"""WOT ({colorama.Fore.RED}Who's Out There?{colorama.Fore.WHITE}):
# A simple tool for host discovery.

# [Required]:
# {colorama.Style.DIM}[{colorama.Style.RESET_ALL}-t{colorama.Style.DIM}]{colorama.Style.RESET_ALL} Define the target for the scan.
# {colorama.Style.DIM}[{colorama.Style.RESET_ALL}-i{colorama.Style.DIM}]{colorama.Style.RESET_ALL} Define the desired network interface.

# [Optional]:
# {colorama.Style.DIM}[{colorama.Style.RESET_ALL}-h{colorama.Style.DIM}]{colorama.Style.RESET_ALL} Print the help display."""

# try:
# 	if '-h' in sys.argv:
# 		print(HELP_MESSAGE)
# 		sys.exit()

# 	if '-l' in sys.argv:
# 		interfaces = get_if_list()
# 		for interface in interfaces:
# 			PrintMessage(f"{interface}")
# 		sys.exit()

# 	if not VerifyRequired(sys.argv, REQUIRED):
# 		PrintMessage("Failure to verify provided flags. Please ensure you have included required criteria.")
# 		sys.exit()

# 	parameters = { '-t': None, '-i': None }
# 	parameters = PopulateParameters(sys.argv, CONFIGURABLE, parameters)

# 	discovery = Discovery(
# 		parameters['-t'], 
# 		parameters['-i']
# 	)

# 	hosts = discovery.GetHosts()
# 	if not hosts:
# 		PrintMessage("There was an error whilst attempting to scan the network.")

# 	for host in hosts:
# 		PrintMessage("Result for {}[{}{}{}]{}: {}({}{}{}){}".format(
# 			colorama.Style.DIM,
# 			colorama.Style.RESET_ALL,
# 			host,
# 			colorama.Style.DIM,
# 			colorama.Style.RESET_ALL,
# 			colorama.Style.DIM,
# 			colorama.Style.RESET_ALL,
# 			discovery.ReverseDNS(host),
# 			colorama.Style.DIM,
# 			colorama.Style.RESET_ALL
# 		))
# except KeyboardInterrupt:
# 	PrintMessage("Received halt signal. Exiting gracefully.")
# 	sys.exit()