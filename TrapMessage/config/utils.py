from pysnmp import hlapi


class SNMPTrap:
    def __init__(self, retrieveraddress, retrieverport, community):
        self.retrieveraddress = retrieveraddress
        self.retrieverport = retrieverport
        self.community = community

        self.snmpengine = hlapi.SnmpEngine()
        self.contextdata = hlapi.ContextData()

        self.notificationtype = hlapi.NotificationType(hlapi.ObjectIdentity("1.3.6.1.4.1.19398.100.8"))
        self.notificationtype.addVarBinds(hlapi.ObjectType(hlapi.ObjectIdentity("1.3.6.1.4.1.19398.100.1"),
                                                           hlapi.Integer32(12345)))
        self.notificationtype.addVarBinds(hlapi.ObjectType(hlapi.ObjectIdentity("1.3.6.1.4.1.19398.100.6"),
                                                           hlapi.OctetString("Test string")))

    def send(self):
        next(hlapi.sendNotification(self.snmpengine,
                                    hlapi.CommunityData(self.community),
                                    hlapi.UdpTransportTarget((self.retrieveraddress, self.retrieverport)),
                                    self.contextdata,
                                    "trap",
                                    self.notificationtype,
                                    lookupMib=False))