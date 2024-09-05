#!/usr/bin/env python3


import argparse
import ipaddress
import os
import socket
import sys


# getRangeInfo returns a list of [int(netmask), int(network_address)]
def getRangeInfo(r):
    try:
        robj = ipaddress.IPv4Network(r, strict=False)
        return [int(robj.netmask), int(robj.network_address)]
    except ipaddress.AddressValueError:
        try:
            ip_addresses = getIpAddressesFromHostname(r)
            for ip in ip_addresses[2]:
                robj = ipaddress.IPv4Network(ip, strict=False)
                return [int(robj.netmask), int(robj.network_address)]
        except:
            print(f"[!] Error: Invalid IP Network Range:{r}")
            sys.exit(2)


# AddIfValid checks if an IP is within the range info
# given and will add it to return_ips
def addIfValid(ip, range_info, return_ips, return_inrange):
    try:
        ipobj = int(ipaddress.IPv4Address(ip))
        inrange = False
        for rinfo in range_info:
            inrange = (((ipobj & rinfo[0]) == rinfo[1]) or inrange)
        if inrange and return_inrange:
            return_ips.add(ip)
        elif not inrange and not return_inrange:
            return_ips.add(ip)
    except ipaddress.AddressValueError:
        try:
            ip_addresses = getIpAddressesFromHostname(ip)
            for ip in ip_addresses[2]:
                ipobj = int(ipaddress.IPv4Address(ip))
                inrange = False
                for rinfo in range_info:
                    inrange = (((ipobj & rinfo[0]) == rinfo[1]) or inrange)
                if inrange and return_inrange:
                    return_ips.add(ip)
                elif not inrange and not return_inrange:
                    return_ips.add(ip)
        except:
                sys.exit(2)


def getIpAddressesFromHostname(hostname):
    ip_addresses = []
    try:
        resolutions = socket.gethostbyname_ex(hostname)
        for ip in resolutions:
            ip_addresses.append(ip)
    except Exception as e:
        print(f"[!] Error resolving {hostname}: {e}")
        sys.exit(2)

    return ip_addresses

if __name__ == "__main__":
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

    parser = argparse.ArgumentParser(
        add_help=False, description='Simple script to check if a list of IPs\
            are within the provided network scopes.')
    parser.add_argument('-h', '-?', '--h', '-help',
                        '--help', action="store_true", help=argparse.SUPPRESS)

    protocols = parser.add_argument_group('Actions')
    protocols.add_argument('-s', '--scope', default=False, metavar='scope.txt',
                           help='Single or file of IP ranges in CIDR notation')
    protocols.add_argument('-i', '--ip', default=False, metavar='iplist.txt',
                           help='Single or file of IP addresses to check')
    protocols.add_argument('-o', '--out-range', default=False, action='store_true',
                           help='Display IPs that are not within the specified range.')

    args = parser.parse_args()
    if args.h:
        parser.print_help()
        sys.exit()

    scope = args.scope
    check_ips = args.ip
    if args.out_range:
        return_inrange = False
    else:
        return_inrange = True

    # Make sure (ips or pipped data) and scope are supplied
    if (not check_ips and not pipped_ips) or not scope:
        sys.exit(2)

    # Get information about the ranges, whether its a file or a single one
    if os.path.isfile(scope):
        with open(scope) as scopefile:
            for line in scopefile:
                if line.strip():
                    range_info.append(getRangeInfo(line.rstrip('\n')))
    else:
        range_info.append(getRangeInfo(scope))

    # Process pipped data first
    for ip in pipped_ips:
        if ip.strip():
            addIfValid(ip, range_info, return_ips, return_inrange)

    # Go through the inputted IPs and check if they are in the range
    if check_ips and os.path.isfile(check_ips):
        with open(check_ips) as ipfile:
            for line in ipfile:
                ip = line.strip()
                if ip:
                    addIfValid(ip, range_info, return_ips, return_inrange)

    elif check_ips:
        addIfValid(check_ips, range_info, return_ips, return_inrange)

    # Print resulting IP addresses
    for ip in return_ips:
        print(ip)
