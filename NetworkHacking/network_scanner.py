import scapy.all as scapy
import pprint

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    ether = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    final_request = ether / arp_request
    answered = scapy.srp(final_request, timeout=1.5)[0]
    data = {}
    for element in answered:
        data[element[1].psrc] = element[1].hwsrc

    pprint.pprint(data)

scan('192.168.29.1/24')