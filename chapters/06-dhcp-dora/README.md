# Chapter 6 — DHCP: Dynamic Host Configuration Protocol

> "DHCP provides a framework for passing configuration information to hosts
>  on a TCP/IP network. It uses UDP and is built on BOOTP." — Stevens, TCP/IP Illustrated, Vol.1 §16.9

## The DORA Process

```
    Client                     DHCP Server
      │                            │
      │── DISCOVER ──────────────▶│  (broadcast: 0.0.0.0 → 255.255.255.255)
      │   "Is there a DHCP server?"│
      │                            │
      │◀── OFFER ─────────────────│  (offers IP: 192.168.1.100)
      │   "Here's an IP for you"   │
      │                            │
      │── REQUEST ───────────────▶│  (broadcast: "I'll take 192.168.1.100")
      │   "I accept the offer"     │
      │                            │
      │◀── ACK ───────────────────│  (lease confirmed)
      │   "Confirmed. Lease: 24h"  │
```

### Steps

1. **DISCOVER** — Client broadcasts looking for DHCP servers
2. **OFFER** — Server offers an IP address with lease time
3. **REQUEST** — Client formally requests the offered IP
4. **ACK** — Server confirms, lease begins

## 3D Scene

| Packet | Color | Direction |
|--------|-------|-----------|
| DISCOVER | Yellow | Client → Server |
| OFFER | Purple | Server → Client |
| REQUEST | Orange | Client → Server |
| ACK | Green | Server → Client |

### View the scene

Drag `dhcp_dora.glb` into [gltf-viewer.donmccurdy.com](https://gltf-viewer.donmccurdy.com/)

## References

- Stevens, W.R. (1994). *TCP/IP Illustrated, Volume 1*. §16.9
- RFC 2131 — Dynamic Host Configuration Protocol
