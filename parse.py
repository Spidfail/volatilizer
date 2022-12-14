import argparse as agp


parser = agp.ArgumentParser()

parser = agp.ArgumentParser(prog="graph.py",
                            description="Build a graph from netstat output. Based on volatility output.",
                            epilog="This is a ongoing tool for volatility. Feel free to help by creating issues or make pull requests!")
parser.add_argument("filename", type=str, help='CSV filename to be parse')

group_netw = parser.add_mutually_exclusive_group()
group_netw.add_argument('-l', '--local', help='show communications on private networks', action="store_true")
group_netw.add_argument('-r', '--remote', help='show remote communications', action="store_true")

group_protocol = parser.add_mutually_exclusive_group()
group_protocol.add_argument('-u', '--udp',
                            nargs='?',
                            choices=['all', '4', '6'],
                            default=False,
                            metavar="PROTO",
                            help='show only lines associated with User Datagram Protocol only. Possible versions : all (default), 4 (IPv4), 6 (IPv6)')
group_protocol.add_argument('-t', '--tcp',
                            nargs='?',
                            choices=['all', '4', '6'],
                            default=False,
                            metavar="PROTO",
                            help='show only lines associated with Transmission Control Protocol only. Possible versions : all (default), 4 (IPv4), 6 (IPv6)')

args = parser.parse_args()

print(args)