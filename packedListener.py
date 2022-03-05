import scapy.all as scapy
from scapy_http import http
import optparse

def option():
    opt = optparse.OptionParser()
    opt.add_option("-i","--interface",dest="interface",help="enter interface!")
    userInput = opt.parse_args()[0]
    return userInput


def listenPackets(interface = "eth0"):
    scapy.sniff(iface=interface,store=False,prn=analyzePackets)

def analyzePackets(packet):
    #packet.show()
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            print(packet[scapy.Raw].load)

user = option()
userInterface = user.interface
listenPackets(userInterface)