#!/usr/bin/python3
from scapy.all import ARP, srp, Ether
import sys, socket, importlib, re, os

HELP = "SCAN - When provided with a subnet and network interface will trigger a host scan."

TITLE = 'discovery'

TARGET_FLAG = "-t"
INTERFACE_FLAG = "-i"

REQUIRED = [ TARGET_FLAG, INTERFACE_FLAG ]
CONFIGURABLE = [ TARGET_FLAG, INTERFACE_FLAG ]

class Discovery:
	def __init__(self, target, interface):
		self.target = target
		self.interface = interface

	def GetHosts(self):
		packet = Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(pdst=self.target)
		replies = srp(packet, iface=self.interface, timeout=1, verbose=False)[0]

		if not replies: return []

		hosts = []
		for reply in range(0, len(replies)):
			information = (replies[reply][1].psrc, replies[reply][1].hwsrc)
			hosts.append(information)
		return hosts

	def ReverseDNS(self, host):
		try:
			hostname = socket.gethostbyaddr(host)[0]
			return hostname
		except:
			return "N/A"

def FormatArguments(string):
	pattern = r'\"(.*?)\"|(\S+)'
	matches = re.findall(pattern, string)

	words = [quoted if quoted else non_quoted for quoted, non_quoted in matches]
	return words

def VerifyRequired(arguments, required):
	for flag in required:
		if flag not in arguments:
			return False
	return True

def HandleCommand(command, shell):
	arguments = FormatArguments(command)
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

		for host in hosts:
			print(f"{host[0]}   {host[1]}   {discovery.ReverseDNS(host)}")
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
		main_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		sys.path.append(main_path)
		library = importlib.import_module('shell')

		shell = library.Shell(TITLE, dialogue=HELP, standalone=True)
		shell.Spawn()

		while shell.active:
			shell.UpdateShell()

			if shell.command: HandleCommand(shell.command, shell)
	except Exception as error:
		print(error)
		return