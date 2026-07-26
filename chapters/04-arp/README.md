# Chapter 4 — ARP: Address Resolution Protocol

> "ARP provides a mapping between IP addresses and hardware addresses.
>  It is used on Ethernet networks to find the MAC address of a host
>  given its IP address." — Stevens, TCP/IP Illustrated, Vol.1 §4.5

## How ARP Works

```
    Sender (192.168.1.1)              All hosts on LAN
      │                                    │
      │── ARP Request (broadcast) ───────▶│
      │   "Who has 192.168.1.2?           │
      │    Tell 192.168.1.1"              │
      │                                    │
      │◀── ARP Reply (unicast) ───────────│ Target (192.168.1.2)
      │   "192.168.1.2 is at             │
      │    aa:bb:cc:dd:ee:ff"             │
```

### Steps

1. **ARP Request** — Sender broadcasts to all hosts on the LAN segment
2. **Processing** — All hosts receive, only the target responds
3. **ARP Reply** — Target sends unicast reply with its MAC address
4. **Cache** — Sender caches the mapping (typically 20 minutes)

## 3D Scene

| Element | Color | Description |
|---------|-------|-------------|
| Sender | Blue | Host sending ARP request |
| Target | Green | Host responding with MAC |
| Other hosts | Gray | Background hosts (ignore request) |
| Yellow arrows | Broadcast | ARP request to all |
| Green arrow | Unicast | ARP reply from target |

### View the scene

Drag `arp_resolution.glb` into [gltf-viewer.donmccurdy.com](https://gltf-viewer.donmccurdy.com/)

## References

- Stevens, W.R. (1994). *TCP/IP Illustrated, Volume 1*. §4.5
- RFC 826 — An Ethernet Address Resolution Protocol
