# TCP/IP Illustrated in 3D

Interactive 3D visualizations of core networking concepts from Stevens' *TCP/IP Illustrated*.

Each scene is a standalone HTML file powered by Three.js — no build tools, no server required. Open any `index.html` in a browser to explore.

## Scenes

| # | Scene | Protocol | Controls |
|---|-------|----------|----------|
| 1 | [TCP Three-Way Handshake](scenes/01-three-way-handshake/) | TCP | SYN &rarr; SYN-ACK &rarr; ACK |
| 2 | [IP Fragmentation](scenes/02-ip-fragmentation/) | IP | Packet splits at MTU boundary |
| 3 | [TCP Sliding Window](scenes/03-tcp-window/) | TCP | Window slides with ACKs |

## Planned

- TCP Congestion Control (slow start, congestion avoidance)
- DNS Resolution
- ARP Protocol
- HTTP over TCP
- TCP State Machine
- Routing and TTL

## Usage

```bash
# Clone
git clone https://github.com/Maycon-BertolzoDOTCOM/tcpip-illustrated-3d.git
cd tcpip-illustrated-3d

# Open any scene
open scenes/01-three-way-handshake/index.html
# or
firefox scenes/02-ip-fragmentation/index.html
# or just double-click the file
```

No server. No dependencies. Three.js is vendored locally.

## Scene Template

Use `template/index.html` as a starting point for new scenes. It includes the full Three.js scaffold with OrbitControls, lighting, auto-rotate, and fog.

## Reference

- Stevens, W. Richard. *TCP/IP Illustrated, Volume 1: The Protocols*. Addison-Wesley, 1994.
- RFC 793 — TCP
- RFC 791 — IP

## License

MIT
