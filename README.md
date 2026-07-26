<div align="center">

# TCP/IP Illustrated in 3D

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-34d399?style=for-the-badge&logo=github&logoColor=white)](https://maycon-bertolzodotcom.github.io/tcpip-illustrated-3d/)
[![Scenes](https://img.shields.io/badge/Scenes-20-60a5fa?style=for-the-badge)](#-scenes)
[![Tech](https://img.shields.io/badge/Three.js-1.4MB-a78bfa?style=for-the-badge&logo=threedotjs&logoColor=white)](https://threejs.org)
[![License](https://img.shields.io/badge/License-MIT-f59e0b?style=for-the-badge)](LICENSE)

**Interactive 3D visualizations of core networking concepts**  
from Stevens' *TCP/IP Illustrated* — 20 scenes, zero dependencies, no server required.

</div>

## 🔗 Live Demo

**[→ Open on GitHub Pages](https://maycon-bertolzodotcom.github.io/tcpip-illustrated-3d/)**  
Browse all 20 scenes online — point cloud splats and animated 3D alike.

## 📡 3D Splat Scenes (Point Cloud)

Procedural point clouds generated via `splat_factory.py`. Navigate in 3D with drag + zoom.

| # | Scene | Points | Preview |
|---|-------|-------:|---------|
| [S1](scenes/splat-handshake) | Three-Way Handshake | 1 040 | [Open](scenes/splat-handshake) |
| [S2](scenes/splat-topology) | Network Topology | 966 | [Open](scenes/splat-topology) |
| [S3](scenes/splat-dns) | DNS Resolution Chain | 560 | [Open](scenes/splat-dns) |
| [S4](scenes/splat-tcp-state) | TCP State Machine | 792 | [Open](scenes/splat-tcp-state) |
| [S5](scenes/splat-dhcp) | DHCP DORA | 985 | [Open](scenes/splat-dhcp) |
| [S6](scenes/splat-ping) | ICMP Ping | 905 | [Open](scenes/splat-ping) |
| [H1](scenes/hybrid-handshake) | **Hybrid**: Splat + Animated Packets | 1 040 | [Open](scenes/hybrid-handshake) |

## 🎬 Animated 3D Scenes (Three.js)

Each scene is a standalone HTML with embedded Three.js — drag, zoom, and watch the protocol come to life.

| # | Scene | Protocol |
|---|-------|----------|
| 01 | [TCP Three-Way Handshake](scenes/01-three-way-handshake) | `SYN → SYN-ACK → ACK` |
| 02 | [IP Fragmentation](scenes/02-ip-fragmentation) | Packet → 3 fragments → reassembly |
| 03 | [TCP Sliding Window](scenes/03-tcp-window) | 10-segment window slides on ACK |
| 04 | [TCP Congestion Control](scenes/04-congestion-control) | 30-bar sawtooth: slow start + avoidance |
| 05 | [DNS Resolution](scenes/05-dns-resolution) | Resolver → Root → TLD → Auth |
| 06 | [HTTP over TCP](scenes/06-http-over-tcp) | Handshake → GET → 200 OK |
| 07 | [ARP Protocol](scenes/07-arp) | Broadcast → Reply → MAC resolution |
| 08 | [TCP State Machine](scenes/08-tcp-state-machine) | 11-state circular diagram |
| 09 | [ICMP Traceroute](scenes/09-icmp-traceroute) | TTL probes → 3 hops → destination |
| 10 | [UDP Datagram](scenes/10-udp-datagram) | Connectionless fire-and-forget |
| 11 | [Routing & TTL](scenes/11-routing-ttl) | TTL 64 → 61 across 3 hops |
| 12 | [ICMP Ping](scenes/12-icmp-ping) | Echo Request → Reply, 5 pings |
| 13 | [DHCP DORA](scenes/13-dhcp-dora) | Discover → Offer → Request → ACK |

## ⚡ Quick Start

```bash
git clone https://github.com/Maycon-BertolzoDOTCOM/tcpip-illustrated-3d.git
cd tcpip-illustrated-3d
open scenes/01-three-way-handshake/index.html
```

> **No server. No dependencies.** Three.js is vendored (1.4 MB). Open directly via `file://`.

## 🧱 Scene Template

Use [`template/index.html`](template/index.html) as a starting point for new scenes. It includes the full Three.js scaffold with OrbitControls, lighting, auto-rotate, fog, and resize handling.

## 📚 Reference

- Stevens, W. Richard. *TCP/IP Illustrated, Volume 1: The Protocols*. Addison-Wesley, 1994. ISBN 0-201-63346-9
- RFC 793 — Transmission Control Protocol
- RFC 791 — Internet Protocol
- RFC 1034/1035 — Domain Name System
- RFC 5681 — TCP Congestion Control

## 📊 Project Stats

```
Scenes:     20 (13 animated + 6 splat + 1 hybrid)
Points:     5,248 (splat cloud vertices)
Code:       6,300+ lines (Three.js + splat factory)
Size:       1.4 MB (vendored Three.js)
Deps:       0 (vanilla JS, self-contained)
```

## 📜 License

MIT &copy; Maycon Bertolzo
