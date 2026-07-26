# Chapter 18 — TCP State Machine

> "A TCP connection is a state machine with 11 states. Transitions are driven
>  by user calls, segment arrivals, and timeouts." — Stevens, §18.2

## TCP States

```
                    ┌──────────────────────────────────────────┐
                    │                                          │
    CLOSED ──▶ LISTEN ──▶ SYN_RCVD ──▶ ESTABLISHED ──▶ CLOSE_WAIT
       ↑           │           │                            │
       │           └───────────┤                            ▼
       │                       └──▶ SYN_SENT ──▶ LAST_ACK ─┘
       │                                                    │
       └── TIME_WAIT ◀── FIN_WAIT_2 ◀── FIN_WAIT_1 ◀───────┘
                    ↑                   │
                    └───── CLOSING ◀────┘
```

## 3D Scene

11 states arranged in a circle, each a colored sphere with transitions as arrows.

| State | Color | Description |
|-------|-------|-------------|
| CLOSED | Gray | No connection |
| LISTEN | Purple | Server waiting |
| SYN_SENT | Blue | Client sent SYN |
| SYN_RCVD | Light blue | Server received SYN |
| ESTABLISHED | Green | Connection active |
| CLOSE_WAIT | Orange | Passive close |
| LAST_ACK | Dark orange | Waiting for final ACK |
| FIN_WAIT_1 | Red | Active close, FIN sent |
| FIN_WAIT_2 | Dark red | Waiting for peer FIN |
| CLOSING | Darker red | Both closing simultaneously |
| TIME_WAIT | Pink | Waiting for old segments |

### View

Drag `tcp_state_machine.glb` into [gltf-viewer.donmccurdy.com](https://gltf-viewer.donmccurdy.com/)

## References

- Stevens, W.R. (1994). §18.2
- RFC 793 — Transmission Control Protocol
