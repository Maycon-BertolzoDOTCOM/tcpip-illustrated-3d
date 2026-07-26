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
| 6 | [HTTP over TCP](scenes/06-http-over-tcp/) | HTTP | Handshake, GET request, 200 OK response in one loop |

## Planned

- ARP Protocol
- TCP State Machine
- Routing and TTL
- UDP Datagram
- ICMP Ping / Traceroute

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
