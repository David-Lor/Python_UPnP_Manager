import miniupnpc

upnp = miniupnpc.UPnP()
upnp.discoverdelay = 10
upnp.discover()
upnp.selectigd()


class PortMapping(object):
	def __init__(self, tpl): #Receive a tuple returned by upnp.getgenericportmapping(x), format: (56614, 'TCP', ('192.168.0.210', 56614), 'name of port mapping', '1', '', 0)
		self.ip = tpl[2][0]
		self.external_port = tpl[0]
		self.internal_port = tpl[2][1]
		self.name = tpl[3]
		if tpl[1] == "TCP":
			self.udp = False
		else:
			self.udp = True
	def remove(self):
		removePort(self.external_port, self.udp)


def addPort(external_port, ip, name="UPnP Mapping added by MiniUPnPc @ Python", udp=False, internal_port=False):
	if udp:
		protocol = "UDP"
	else:
		protocol = "TCP"
	if internal_port == False:
		internal_port = external_port
	upnp.addportmapping(external_port, protocol, ip, internal_port, name, "") #External port, protocol, Target IP, internal port, name, ¿? (empty str)


def removePort(external_port, udp=False):
	if udp:
		protocol = "UDP"
	else:
		protocol = "TCP"
	upnp.deleteportmapping(external_port, protocol) #External Port, Protocol


def getAllPorts():
	i=0
	results = list()
	while True:
		mapping = upnp.getgenericportmapping(i) # (56614, 'TCP', ('192.168.0.210', 56614), 'name of port mapping', '1', '', 0)
		if mapping is None:
			break
		results.append(mapping)
		i+=1
	return [PortMapping(tpl) for tpl in results]


def removeAllPorts():
	mappings = getAllPorts()
	for mp in mappings:
		mp.remove()
