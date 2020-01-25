# Ethical-hacking-concept-arp-spoofer


While there are several apr spoofing tools available on the net, I wanted to create a low-level one that will work for linux machines and is written using python and scapy. 

This tool is just a proof of concept and not intended to be used for any illegal or unethical activity. It should only be used on machines and networks that you as a user own and/or have written permission to use and access. 

# Notes of use:
1.) User will need to enable port forwarding in terminal. This will allow the linux machine to pass the data packets through it. Failure to do so will result in the target machine no being able to access the internet. 
 
   `echo 1 > /proc/sys/net/ipv4/ip_forward`

 2.) This is intended to be used for just HTTP targets, however you can try to use SSLStrip as well to bypass HTTPS but in my experience SSLstrip has been VERY hit or miss on a lot of sites and therefore new methods of bypassing HTTPS should be explored. 

 So in one terminal run this program, in another terminal run SSLstrip, and in a third run this command for your iptables to work (port 10000 is used by SSLstrip, but the destination port should be changed to whatever you need it to be, though port 80 should be what you need most of the time for this)

 `iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000`

 3.) This progam should be run using python3, not python2.

 4.) I used argparse to allow for command line use of specifying the target IP address and the IP address of what you are trying to spoof.

     "-t", "--target",  help="specify the target IP address you want to hit: Example - 10.0.2.5. don't forget quotes around the numbers")

    "-s", "--spoof", help="specify the IP address you want to spoof: Example - 10.0.2.1. don't forget quotes around the numbers")

5.) reminder, this should not be used against real targets. Its not very stealthy and thus most IDS will (or at least should) pick up on this. This is for understanding purposes only. 


