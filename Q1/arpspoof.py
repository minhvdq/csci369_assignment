from scapy.layers.l2 import Ether,ARP,srp

broadcast_mac = Ether(dst="ff:ff:ff:ff:ff:ff")
arp_ip = ARP(pdst="192.168.64.3")
# arp_ip  = ARP(pdst="10.0.0.1")
print("Preparing to send")
answered, unanswered = srp(broadcast_mac/arp_ip)
print("Sent ARP successfully")
if answered:
    for sent, received in answered:
        print(f"IP: {sent.psrc} and MAC: {sent.hwsrc}")
        print(f"IP: {received.psrc} and MAC: {received.hwsrc}")
else:
    print("No answer")