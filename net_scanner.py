import scapy.all as scapy
import optparse

def get_arguements():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target IP / IP range.")
    (options, arguments) = parser.parse_args()
    return options

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1,verbose=False)[0]

    client_list = []

    for element in answered_list:
        client_dict = {"ip":element[1].psrc, "mac":element[1].hwsrc}
        client_list.append(client_dict)
    return client_list

def print_result(result_list):
    print('IP\t\t\tMAC Adddress\n' + '-' * 50)
    for client in result_list:
        print(client['ip'] + "\t\t" + client['mac'])

options = get_arguements()
scan_result = scan(options.target)
print_result(scan_result)