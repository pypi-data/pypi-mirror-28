import ctypes
import random
import socket
import threading

from netaddr import IPNetwork, IPAddress
import socks
from scapy.all import IP, UDP, struct


class ICMP(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ubyte),
        ("code", ctypes.c_ubyte),
        ("checksum", ctypes.c_ushort),
        ("unused", ctypes.c_ushort),
        ("next_hop_mtu", ctypes.c_ushort)
    ]

    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        pass


class Scanner(object):
    def __init__(self, proxies=None, hosts=["127.0.0.1"], ports=[19],
                 timeout=1, recheck=0, src_int_address=None):
        self.proxies = proxies
        self.hosts = hosts
        self.ports = ports
        self.timeout = timeout
        self.recheck = recheck
        self.src_int_address = src_int_address
        self.sockets = {}
        self._init_sockets()

    def _init_sockets(self):
        """Initiate sockets throgh proxies"""

        if self.proxies is not None:
            for proxy in self.proxies:
                ip, port = proxy.split(":")
                port = int(port)

                self.sockets[proxy] = socks.socksocket(
                    socket.AF_INET, socket.SOCK_DGRAM)
                self.sockets[proxy].set_proxy(socks.SOCKS5, ip, port)
                self.sockets[proxy].setblocking(0)
                self.sockets[proxy].settimeout(self.timeout)
        else:
            self.sockets["default"] = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM)
            self.sockets["default"].setblocking(0)
            self.sockets["default"].settimeout(self.timeout)

    def _init_socket(self, proxy):
        """Initiate socket throgh proxy

        @param proxy: Proxy address in format ip:port
        @type proxy: `str`
        """

        if proxy != "default":
            self.sockets[proxy] = socks.socksocket(
                socket.AF_INET, socket.SOCK_DGRAM)
            ip, port = proxy.split(":")
            port = int(port)
            self.sockets[proxy].set_proxy(socks.SOCKS5, ip, port)
        else:
            self.sockets[proxy] = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM)

        self.sockets[proxy].setblocking(0)
        self.sockets[proxy].settimeout(self.timeout)

    def segmentation(self, subnet):
        """Split IP into segments

        @param subnet: IP or subnet
        @type subnet: `str`
        """

        segments = subnet.split(".")
        if "/" in segments[-1]:
            segments.extend(segments[-1].split("/"))
            del segments[-3]

        return segments

    def break_up_ip_ranges(self, segments):
        """Breaks up IP ranges

        Example:
        For ["192", "168", "0-1", "0"]
        would be ["192.168.0.0", "192.168.1.0"]
        """

        subnets = []
        tails = []
        head = ""
        idx = 0

        while "-" not in segments[idx]:
            if idx < len(segments) - 1:
                head += segments[idx] + "."
            else:
                head += segments[idx]
            if idx + 1 == len(segments):
                break
            idx += 1

        if "-" in segments[idx]:
            start, end = segments[idx].split("-")
            for el in xrange(int(start), int(end) + 1):
                tails.extend(self.break_up_ip_ranges(
                    [str(el)] + segments[idx+1:]))
            for el in tails:
                subnets.append(head + el)

        if not subnets:
            subnets.append(head)

        return subnets

    def parse_subnet(self, subnet):
        """Parse subnet into subnets"""

        segments = self.segmentation(subnet)
        if "/" in subnet:
            subnets = self.break_up_ip_ranges(segments[:-1])
            for idx in xrange(len(subnets)):
                subnets[idx] = subnets[idx] + "/" + segments[-1]
        else:
            subnets = self.break_up_ip_ranges(segments)

        return subnets

    def break_up_port_range(self, port_range):
        """Breaks up port ranges

        @param port_range: Port range to parse
        @type port_range: `str`
        """

        ports = []

        start, end = port_range.split("-")
        for idx in xrange(int(start), int(end) + 1):
            ports.append(idx)

        return ports

    def scan(self):
        """Scan hosts for ports status"""

        scan_data = {}
        threads = []

        def send_requests():
            """Send requests to hosts in subnet"""

            for net_ip in IPNetwork(subnet):
                ip = net_ip.format()
                for port in ports:
                    for i in xrange(self.recheck + 1):
                        proxy, s = random.choice(self.sockets.items())
                        packet = IP(dst=ip)/UDP(dport=port)/("")
                        try:
                            self._init_socket(proxy)
                            scan_data["current_ip"] = ip
                            scan_data["current_port"] = port
                            if proxy == "default":
                                s.sendto(bytes(packet), (ip, port))
                            else:
                                s.connect((ip, port))
                                s.send(bytes(packet))
                            s.recv(65565)
                            scan_data["{}:{}".format(ip, port)] = \
                                "Open"
                            s.close()
                        except socket.timeout:
                            if "{}:{}".format(ip, port) not in scan_data or \
                                scan_data["{}:{}".format(ip, port)] == \
                                    "Closed":
                                scan_data["{}:{}".format(ip, port)] = \
                                    "Open|Filtered"
                            s.close()
                        except socket.error:
                            s.close()

        def sniff_icmp():
            """Sniff for ICMP responses"""

            sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                socket.IPPROTO_ICMP)
            sniffer.bind((self.src_int_address, 0))
            sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

            while True:
                raw_buffer = sniffer.recvfrom(65565)[0]
                ip_header = raw_buffer[0:20]
                iph = struct.unpack('!BBHHHBBH4s4s', ip_header)

                # protocol = iph[6]
                version_ihl = iph[0]
                ihl = version_ihl & 0xF
                iph_length = ihl * 4
                src_addr = socket.inet_ntoa(iph[8])

                buf = raw_buffer[iph_length:iph_length + ctypes.sizeof(ICMP)]
                icmp_header = ICMP(buf)

                if self.proxies is not None and \
                    src_addr in [el.split(":")[0] for el in self.proxies] or \
                    self.proxies is None and any(IPAddress(src_addr)
                        in IPNetwork(subnet) for subnet in subnets):
                    if icmp_header.code == 3 and icmp_header.type == 3:
                        scan_data["{}:{}".format(scan_data["current_ip"],
                            scan_data["current_port"])] = "Closed"
                    else:
                        scan_data["{}:{}".format(scan_data["current_ip"],
                            scan_data["current_port"])] = "Filtered"

        subnets = []
        for host in self.hosts:
            subnets.extend(self.parse_subnet(host))

        ports = []
        for port in self.ports:
            if "-" in port:
                ports.extend(self.break_up_port_range(port))
            else:
                ports.append(int(port))

        sniff_thread = threading.Thread(target=sniff_icmp)
        sniff_thread.daemon = True
        sniff_thread.start()

        for subnet in subnets:
            t = threading.Thread(target=send_requests)
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

        return scan_data
