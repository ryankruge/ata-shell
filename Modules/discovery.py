from scapy.all import ARP, srp, Ether
import sys, socket, importlib

class Discovery:
	def __init__(self, target, interface):
		self.target = target
		self.interface = target

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

def VerifyRequired(arguments, required):
	for flag in required:
		if flag not in arguments:
			return False
	return True

HELP = "SCAN - When provided with a subnet and network interface will trigger a host scan."

SHELL_DIRECTORY = "C:/Users/Tomas/Documents/Scripts/ATA"
TITLE = 'discovery'

TARGET_FLAG = "target"
INTERFACE_FLAG = "interface"

REQUIRED = [ TARGET_FLAG, INTERFACE_FLAG ]
CONFIGURABLE = [ TARGET_FLAG, INTERFACE_FLAG ]

def HandleCommand(command, shell):
	arguments = GetArguments(command) # FINAL ISSUE, PARSE ARGUMENTS THAT SUPPORT QUOTATIONS: "Wi-Fi 2" AS ONE PARAMETER.
	match arguments[0]:
		case 'scan':
			Main(arguments, shell)
	shell.command = None

def Main(arguments, shell):
	try:
		if not VerifyRequired(arguments, REQUIRED):
			print("Flag criteria not met.")
			return

		parameters = { TARGET_FLAG: None, INTERFACE_FLAG: None }
		parameters = PopulateParameters(arguments, CONFIGURABLE, parameters)

		discovery = Discovery(
			parameters[TARGET_FLAG],
			parameters[INTERFACE_FLAG]
		)

		hosts = discovery.GetHosts()
		if not hosts:
			print("There was an error whilst attempting to scan the network.")
			return

		for host in hosts: print(f"Result for [{host}]: ({discovery.ReverseDNS(host)})")
	except Exception as error:
		print(error)
		return

def PopulateParameters(arguments, flags, dictionary):
	try:
		temporary = dictionary
		for argument in range(0, len(arguments)):
			if arguments[argument] in flags:
				dictionary[arguments[argument]] = arguments[argument + 1]
		return temporary
	except TypeError:
		print("Error whilst populating parameters.")
		return

def Initialise():
	try:
		sys.path.append(SHELL_DIRECTORY)
		library = importlib.import_module('shell')

		shell = library.Shell(TITLE, dialogue=HELP, standalone=True)
		shell.Spawn()

		while shell.active:
			shell.UpdateShell()

			if shell.command: HandleCommand(shell.command, shell)
	except Exception as error:
		print(error)
		return