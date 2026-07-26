# Chapter 11 — ICMP: Internet Control Message Protocol

> "ICMP is used to send error and control messages between hosts and routers.
>  The ping utility uses ICMP Echo Request/Reply to measure reachability." — Stevens, §11.2

## ICMP Echo (Ping)

```
    Host A                          Host B
      │                               │
      │── Echo Request (type 8) ────▶│
      │   seq=1, id=0x1234            │
      │                               │
      │◀── Echo Reply (type 0) ──────│
      │   seq=1, id=0x1234            │
      │                               │
      RTT = time between request and reply
```

## 3D Scene

| Element | Color | Description |
|---------|-------|-------------|
| Host A | Blue | Ping sender |
| Host B | Green | Ping responder |
| Yellow arrows | Echo Request | type=8 |
| Green arrows | Echo Reply | type=0 |
| Red ring | RTT meter | Round-trip time |

### View

Drag `icmp_ping.glb` into [gltf-viewer.donmccurdy.com](https://gltf-viewer.donmccurdy.com/)

## References

- Stevens, W.R. (1994). §11.2
- RFC 792 — Internet Control Message Protocol
