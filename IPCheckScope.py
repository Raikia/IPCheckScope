#!/usr/bin/env python3

import sys,os,getopt
import ipaddress

def main(argv):
    # Define variables
    scope = ""
    check_ips = ""
    return_inrange = True
    pipped_ips = []
    range_info = []
    return_ips = set()
    
    # Allow for pipped in data
    if not sys.stdin.isatty():
        for line in sys.stdin:
            pipped_ips.append(line.rstrip('\n'))
    
    # Get command line arguments
    try:
        opts, args = getopt.getopt(argv, "s:i:o", ["scope=", "ip=", "out-range"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-s", "--scope"):
            scope = arg
        elif opt in ("-i", "--ip"):
            check_ips = arg
        elif opt in ("-o", "--out-range"):
            return_inrange = False
        else:
            assert False, "Invalid arguments"
    
    # Make sure (ips or pipped data) and scope are supplied
    if (not check_ips and not pipped_ips) or not scope:
        usage()
        sys.exit(2)

    # Get information about the ranges, whether its a file or a single one
    if os.path.isfile(scope):
        with open(scope) as scopefile:
            for line in scopefile:
                range_info.append(getRangeInfo(line.rstrip('\n')))
    else:
        range_info.append(getRangeInfo(scope))

    # Process pipped data first
    for ip in pipped_ips:
        addIfValid(ip, range_info, return_ips, return_inrange)

    # Go through the inputted IPs and check if they are in the range
    if os.path.isfile(check_ips):
        with open(check_ips) as ipfile:
            for line in ipfile:
                ip = line.rstrip('\n')
                addIfValid(ip, range_info, return_ips, return_inrange)

    else:
        addIfValid(check_ips, range_info, return_ips, return_inrange)

    # Print resulting IP addresses
    for ip in return_ips:
        print(ip)
     
# getRangeInfo returns a list of [int(netmask), int(network_address)]
def getRangeInfo(r):
    try:
        robj = ipaddress.IPv4Network(r, strict=False)
        return [int(robj.netmask), int(robj.network_address)]
    except:
        print("[!] Error: Invalid IP Network Range: " + str(line))
        sys.exit(2)

# AddIfValid checks if an IP is within the range info given and will add it to return_ips
def addIfValid(ip, range_info, return_ips, return_inrange):
    try:
        ipobj = int(ipaddress.IPv4Address(ip))
    except:
        print("[!] Error: Invalid IP address: " + str(ip))
        sys.exit(2)
    inrange = False
    for rinfo in range_info:
        inrange = (((ipobj & rinfo[0]) == rinfo[1]) or inrange)
    if inrange and return_inrange:
        return_ips.add(ip)
    elif not inrange and not return_inrange:
        return_ips.add(ip)




def usage():
    scriptname = sys.argv[0]
    print('''
IPCheckScope
---------------
Simple script to check if a list of IPs are within the provided network scopes


Usage:
    python3 %s args

Example Usage:
    python3 %s -s scope.txt -i ips_to_test.txt
    python3 %s -s 192.168.1.0/24 -i ips_to_test.txt
    python3 %s -s scope.txt -i 192.168.1.1
    python3 %s -s 192.168.1.0/24 -i 192.168.1.1
    echo list_of_ips.txt | python3 %s -s scope.txt

Options:
    -s, --scope         Single or file of IP ranges in CIDR notation
                        Ex: 192.168.1.0/24

    -i, --ip            Single or file of IP addresses to check

    -o, --out-range     Display IPs that are not within the specified range
                        (Without this, only IPs within the range will print)

Support:
    raikiasec@gmail.com
    @raikiasec
    https://github.com/raikia
    ''' % (scriptname, scriptname, scriptname, scriptname, scriptname, scriptname))

if __name__ == "__main__":
    main(sys.argv[1:])

