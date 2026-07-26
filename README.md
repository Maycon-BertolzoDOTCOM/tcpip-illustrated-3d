# TCP/IP Illustrated in 3D

Interactive 3D visualizations of core networking concepts from Stevens' *TCP/IP Illustrated*.

Each scene is a standalone HTML file powered by Three.js — no build tools, no server required. Open any `index.html` in a browser to explore.

## Scenes

| # | Scene | Protocol | What you see |
|---|-------|----------|--------------|
| 1 | [TCP Three-Way Handshake](scenes/01-three-way-handshake/) | TCP | SYN &rarr; SYN-ACK &rarr; ACK packets between hosts |
| 2 | [IP Fragmentation](scenes/02-ip-fragmentation/) | IP | Large packet splits at router MTU, 3 fragments travel, reassemble |
| 3 | [TCP Sliding Window](scenes/03-tcp-window/) | TCP | 10-segment window slides forward as ACKs arrive |
| 4 | [TCP Congestion Control](scenes/04-congestion-control/) | TCP | 30-bar sawtooth: slow start (blue) &rarr; avoidance (green) &rarr; loss (red) |
| 5 | [DNS Resolution](scenes/05-dns-resolution/) | DNS | Query packet chains through Resolver &rarr; Root &rarr; TLD &rarr; Auth |
| 7 | [ARP Protocol](scenes/07-arp/) | ARP | Broadcast request, unicast reply — IP to Ethernet MAC resolution |
| 8 | [TCP State Machine](scenes/08-tcp-state-machine/) | TCP | 11-state diagram: CLOSED &rarr; LISTEN &rarr; ... &rarr; TIME-WAIT &rarr; CLOSED |
| 9 | [ICMP Traceroute](scenes/09-icmp-traceroute/) | ICMP | TTL probes mapped hop-by-hop through 3 routers to destination |
| 10 | [UDP Datagram](scenes/10-udp-datagram/) | UDP | Connectionless datagrams: fire, forget, and lost packets with no retransmit |
| 11 | [Routing & TTL](scenes/11-routing-ttl/) | IP | TTL counter decrements across 3 router hops from 64 to 61 |
| 12 | [ICMP Ping](scenes/12-icmp-ping/) | ICMP | Echo Request &rarr; Echo Reply; 5 pings with RTT meter |
| 13 | [DHCP DORA](scenes/13-dhcp-dora/) | DHCP | Discover &rarr; Offer &rarr; Request &rarr; Acknowledge |

## Usage

```bash
git clone https://github.com/Maycon-BertolzoDOTCOM/tcpip-illustrated-3d.git
cd tcpip-illustrated-3d
open scenes/01-three-way-handshake/index.html
```

No server. No dependencies. Three.js is vendored locally (1.4 MB). Opens directly in any browser via `file://`.

## Scene Template

Use `template/index.html` as a starting point for new scenes. It includes the full Three.js scaffold with OrbitControls, lighting, auto-rotate, fog, and resize handling.

## Reference

- Stevens, W. Richard. *TCP/IP Illustrated, Volume 1: The Protocols*. Addison-Wesley, 1994. ISBN 0-201-63346-9
- RFC 793 — Transmission Control Protocol
- RFC 791 — Internet Protocol
- RFC 1034/1035 — Domain Name System
- RFC 5681 — TCP Congestion Control

## License

MIT &copy; Maycon Bertolzo
