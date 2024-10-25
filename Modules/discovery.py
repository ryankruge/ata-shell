#!/usr/bin/python3
# All software written by Tomas. (https://github.com/shelbenheimer/ata-shell)

from scapy.all import ARP, srp, Ether
import sys
import importlib
import re
import os
import requests

HELP = """SCAN - Requires `-t` and `-i` flags to function.
-T - Specify the target, single address or subnet in 0.0.0.0/24 format.
-I - Specify the desired network interface to use for the scan."""

BANNER = "Software written by Tomas. Available on GitHub. (https://github.com/ryankruge/ata-shell)"
VENDOR_PATH = "/Resources/manuf"

TITLE = 'discovery'

TARGET_FLAG = "-t"
INTERFACE_FLAG = "-i"

REQUIRED = [ TARGET_FLAG, INTERFACE_FLAG ]
CONFIGURABLE = [ TARGET_FLAG, INTERFACE_FLAG ]

class Discovery:
	def __init__(self, target, interface):
		self.target    = target
		self.interface = interface

		self.path    = f"{os.path.dirname(os.path.abspath(__file__))}{VENDOR_PATH}"
		self.vendors = {}

	def GetHosts(self):
		packet = Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(pdst=self.target)
		replies = srp(packet, iface=self.interface, timeout=2, verbose=False)[0]

		if not replies: return []

		hosts = []
		for reply in range(0, len(replies)):
			information = (replies[reply][1].psrc, replies[reply][1].hwsrc)
			hosts.append(information)
		return hosts

	def PopulateVendors(self):
		try:
			with open(self.path, encoding="utf8") as file:
				temporary = {}
				for line in file:
					split = line.split()
					temporary[split[0]] = split[1]
				return temporary
			return
		except Exception as error:
			print(error)
			sys.exit()

	def FormatOUI(self, address):
		formatted = address[:8].replace("-", ":")
		return formatted

	def GetVendor(self, address):
		if not self.vendors:
			self.vendors = self.PopulateVendors()
		if not self.vendors:
			return "Unobtainable"

		formatted = self.FormatOUI(address).upper()
		try:
			return self.vendors[formatted]
		except:
			return "Unknown Vendor"

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
	shell.buffer = None

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

		print(BANNER)

		if not discovery.PopulateVendors():
			print("Failed to populate manufacturer database.")

		hosts = discovery.GetHosts()
		if not hosts:
			print("There was an error whilst attempting to scan the network.")
			return

		for host in hosts:
			vendor = discovery.GetVendor(host[1])
			print(f"{host[0]:<18} {host[1]:<20} {vendor:<20}")
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
		shell_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		sys.path.append(shell_path)
		library = importlib.import_module('shell')

		shell = library.Shell(TITLE, dialogue=HELP, standalone=True)
		shell.Spawn()

		while shell.active:
			shell.UpdateShell()

			if shell.buffer: HandleCommand(shell.buffer, shell)
	except Exception as error:
		print(error)
		return