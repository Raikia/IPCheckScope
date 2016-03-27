IPCheckScope
==============

Simple script to check if a list of IPs are within the provided network scopes


## Usage:
    python3 ./IPCheckScope.py args

## Example Usage:
    python3 ./IPCheckScope.py -s scope.txt -i ips_to_test.txt
    python3 ./IPCheckScope.py -s 192.168.1.0/24 -i ips_to_test.txt
    python3 ./IPCheckScope.py -s scope.txt -i 192.168.1.1
    python3 ./IPCheckScope.py -s 192.168.1.0/24 -i 192.168.1.1
    echo list_of_ips.txt | python3 ./IPCheckScope.py -s scope.txt

## Options:
    -s, --scope         Single or file of IP ranges in CIDR notation
                        Ex: 192.168.1.0/24

    -i, --ip            Single or file of IP addresses to check

    -o, --out-range     Display IPs that are not within the specified range
                        (Without this, only IPs within the range will print)

## Support:
   * raikiasec@gmail.com
   * [@raikiasec](https://twitter.com/raikiasec)
   * https://github.com/raikia
    
