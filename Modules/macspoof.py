#!/usr/bin/python3
# All software written by Tomas. (https://github.com/shelbenheimer/ata-shell)

import subprocess
import platform
import sys
import re

os = platform.system()

def ValidateMAC(address):
	valid = "FF:FF:FF:FF:FF:FF"
	pattern = r'^[0-9a-fA-F]$'

	if not len(address) == len(valid):
		return False

	for character in range(0, len(list(valid))):
		if valid[character] == ':': continue

		if not re.match(pattern, address[character]):
			return False
	return True

def Spoof(address, adapter):
	match os:
		case "Linux":
			subprocess.run(["ip", "link", "set", adapter, "down"], text=True)
			subprocess.run(["ip", "link", "set", adapter, "address", address], text=True)
			subprocess.run(["ip", "link", "set", adapter, "up"], text=True)
		case "Windows":
			print("Support for Windows is not currently available.")
			sys.exit()

try:
	if not os == "Linux":
		print("This tool is only available on Linux.")
		sys.exit()

	address = input("enter> ")

	if not ValidateMAC(address):
		print("The MAC address provided was invalid.")
		sys.exit()

	adapter = input("adapter> ")

	Spoof(address, adapter)
except KeyboardInterrupt:
	print("Caught interruption. Exiting gracefully.")