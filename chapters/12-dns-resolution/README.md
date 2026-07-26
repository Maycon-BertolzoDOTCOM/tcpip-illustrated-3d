# Chapter 12 — DNS: Domain Name System

> "DNS is a distributed database that maps domain names to IP addresses.
>  It uses a hierarchy of servers: root, TLD, and authoritative." — Stevens, TCP/IP Illustrated, Vol.1 §14.5

## DNS Resolution Chain

```
    Client → Resolver → Root → .com TLD → Authoritative
                                              ↓
                                           93.184.216.34
                                              ↓
    Client ← Resolver ← ← ← ← ← ← ← ← ← ← ←
```

### Steps

1. **Query to Resolver** — Client asks local resolver for `example.com`
2. **Root Query** — Resolver asks Root server (returns .com TLD)
3. **TLD Query** — Resolver asks .com TLD (returns authoritative NS)
4. **Authoritative Query** — Resolver asks authoritative server (returns IP)
5. **Response** — Resolver returns `93.184.216.34` to client

## 3D Scene

| Node | Color | Role |
|------|-------|------|
| Client | Blue | Initiates DNS query |
| Resolver | Purple | Recursive resolver |
| Root | Red | Root name server |
| .com TLD | Orange | Top-level domain server |
| Authoritative | Green | Final answer |

| Arrows | Color | Meaning |
|--------|-------|---------|
| Blue (top) | Query | DNS queries flowing right |
| Green (bottom) | Response | DNS responses flowing left |

### View the scene

Drag `dns_resolution.glb` into [gltf-viewer.donmccurdy.com](https://gltf-viewer.donmccurdy.com/)

## References

- Stevens, W.R. (1994). *TCP/IP Illustrated, Volume 1*. §14.5
- RFC 1034/1035 — Domain Names
