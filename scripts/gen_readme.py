#!/usr/bin/env python3
"""Generate README.md with embedded scene screenshots."""
from pathlib import Path

REPO = Path("/tmp/tcpip-3d")
OUT = REPO / "README.md"

SCENES = [
    ("splat-handshake",        "01", "3DGS",    "1,040 pts",  "Three-Way Handshake point cloud"),
    ("splat-topology",         "02", "3DGS",    "966 pts",    "2 hosts + 3 routers network topology"),
    ("splat-dns",              "03", "3DGS",    "560 pts",    "5-node DNS resolution chain"),
    ("splat-tcp-state",        "04", "3DGS",    "792 pts",    "11-state circular diagram"),
    ("splat-dhcp",             "05", "3DGS",    "985 pts",    "DHCP DORA sequence"),
    ("splat-ping",             "06", "3DGS",    "905 pts",    "ICMP Echo between two hosts"),
    ("hybrid-handshake",       "07", "Hybrid",  "1,040 pts",  "Point cloud + animated SYN/SYN-ACK/ACK"),
    ("01-three-way-handshake", "08", "TCP",     "Animated",  "SYN → SYN-ACK → ACK"),
    ("02-ip-fragmentation",    "09", "IP",      "Animated",  "Packet → 3 fragments → reassembly"),
    ("03-tcp-window",          "10", "TCP",     "Animated",  "10-segment sliding window"),
    ("04-congestion-control",  "11", "TCP",     "Animated",  "30-bar sawtooth diagram"),
    ("05-dns-resolution",      "12", "DNS",     "Animated",  "Resolver → Root → TLD → Auth"),
    ("06-http-over-tcp",       "13", "HTTP",    "Animated",  "Handshake → GET → 200 OK"),
    ("07-arp",                 "14", "ARP",     "Animated",  "Broadcast → Reply → MAC"),
    ("08-tcp-state-machine",   "15", "TCP",     "Animated",  "11-state circular diagram"),
    ("09-icmp-traceroute",     "16", "ICMP",    "Animated",  "TTL probes across 3 hops"),
    ("10-udp-datagram",        "17", "UDP",     "Animated",  "Connectionless fire-and-forget"),
    ("11-routing-ttl",         "18", "IP",      "Animated",  "TTL 64 → 61 across 3 hops"),
    ("12-icmp-ping",           "19", "ICMP",    "Animated",  "5 pings with RTT meter"),
    ("13-dhcp-dora",           "20", "DHCP",    "Animated",  "Discover → Offer → Request → ACK"),
]

def gen():
    lines = []
    a = lines.append

    a('<div align="center">')
    a('')
    a('# TCP/IP Illustrated in 3D')
    a('')
    a('[![Live Demo](https://img.shields.io/badge/LIVE-DEMO-34d399?style=for-the-badge&logo=githubpages&logoColor=white)](https://maycon-bertolzodotcom.github.io/tcpip-illustrated-3d/)')
    a('[![Scenes](https://img.shields.io/badge/20-SCENES-60a5fa?style=for-the-badge)](#-scenes)')
    a('[![Three.js](https://img.shields.io/badge/Three.js-1.4MB-a78bfa?style=for-the-badge&logo=threedotjs&logoColor=white)](https://threejs.org)')
    a('[![Zero Deps](https://img.shields.io/badge/0-RUNTIME%20DEPS-34d399?style=for-the-badge)](#)')
    a('')
    a('Interactive 3D visualizations of networking protocols from Stevens\' *TCP/IP Illustrated*.')
    a('Each scene is a standalone HTML file — open directly in any browser, no server needed.')
    a('')
    a('</div>')
    a('')
    a('---')
    a('')
    a('## Splat Scenes (3DGS Point Cloud)')
    a('')
    a('Procedural point clouds generated via `splat_factory.py` — drag to orbit, scroll to zoom.')
    a('')

    # Splat scenes grid
    splat = [s for s in SCENES if s[2] in ("3DGS", "Hybrid")]
    for i in range(0, len(splat), 3):
        row = splat[i:i+3]
        a('<table>')
        a('<tr>')
        for folder, num, proto, pts, desc in row:
            a(f'<td align="center" width="33%">')
            a(f'<a href="scenes/{folder}/index.html">')
            a(f'<img src="screenshots/{num}_{folder}.png" width="400" alt="{desc}" />')
            a(f'</a>')
            a(f'<br /><b>{num}</b> — {desc}')
            a(f'<br /><sub>{pts} • <code>{proto}</code></sub>')
            a(f'</td>')
        a('</tr>')
        a('</table>')
        a('')

    a('---')
    a('')
    a('## Animated Scenes (Three.js)')
    a('')
    a('Each scene has real-time protocol animation — drag to orbit, watch packets flow.')
    a('')

    # Animated scenes grid
    anim = [s for s in SCENES if s[2] not in ("3DGS", "Hybrid")]
    for i in range(0, len(anim), 3):
        row = anim[i:i+3]
        a('<table>')
        a('<tr>')
        for folder, num, proto, pts, desc in row:
            a(f'<td align="center" width="33%">')
            a(f'<a href="scenes/{folder}/index.html">')
            a(f'<img src="screenshots/{num}_{folder}.png" width="400" alt="{desc}" />')
            a(f'</a>')
            a(f'<br /><b>{num}</b> — {desc}')
            a(f'<br /><sub><code>{proto}</code></sub>')
            a(f'</td>')
        a('</tr>')
        a('</table>')
        a('')

    a('---')
    a('')
    a('## Quick Start')
    a('')
    a('```bash')
    a('git clone https://github.com/Maycon-BertolzoDOTCOM/tcpip-illustrated-3d.git')
    a('cd tcpip-illustrated-3d')
    a('open scenes/01-three-way-handshake/index.html')
    a('```')
    a('')
    a('> **No server. No dependencies.** Three.js vendored (1.4 MB). Open via `file://`.')
    a('')
    a('---')
    a('')
    a('<div align="center">')
    a('')
    a('| Stat | Value |')
    a('|------|-------|')
    a('| Scenes | 20 (6 splat + 1 hybrid + 13 animated) |')
    a('| Point Cloud Vertices | 5,248 |')
    a('| Lines of Code | 6,300+ |')
    a('| Runtime Size | 1.4 MB (vendored Three.js) |')
    a('| Dependencies | 0 |')
    a('')
    a('</div>')
    a('')
    a('---')
    a('')
    a('## Reference')
    a('')
    a('- Stevens, W. Richard. *TCP/IP Illustrated, Volume 1: The Protocols*. Addison-Wesley, 1994.')
    a('- RFC 793, 791, 1034/1035, 5681')
    a('')
    a('## License')
    a('')
    a('MIT © Maycon Bertolzo')

    OUT.write_text('\n'.join(lines))
    print(f"README written: {len(lines)} lines")

if __name__ == "__main__":
    gen()
