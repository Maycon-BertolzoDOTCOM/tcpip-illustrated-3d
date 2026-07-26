# Chapter 8 — TCP Connection Establishment

> "The TCP three-way handshake is the process by which a TCP connection is established.
>  It involves three messages: a synchronization request, a synchronization acknowledgment,
>  and an acknowledgment." — Stevens, TCP/IP Illustrated, Vol.1 §18.4

## The Three-Way Handshake

```
    Cliente                              Servidor
      │                                    │
      │──── SYN (seq=x) ────────────────▶│
      │      [1/3]                        │
      │                                    │
      │◀─── SYN-ACK (seq=y, ack=x+1) ───│
      │      [2/3]                        │
      │                                    │
      │──── ACK (seq=x+1, ack=y+1) ─────▶│
      │      [3/3]                        │
      │                                    │
      │◀═══════ CONEXÃO ESTABELECIDA ════▶│
```

### Steps

1. **SYN** — Client sends a TCP segment with SYN flag set and initial sequence number `x`
2. **SYN-ACK** — Server responds with SYN + ACK flags, its own sequence number `y`, and acknowledgment `x+1`
3. **ACK** — Client sends ACK with sequence `x+1` and acknowledgment `y+1`

Connection is now established. Both sides have agreed on initial sequence numbers and can begin data transfer.

## 3D Scene

The GLB file `scenes/handshake.glb` is a procedural 3D model generated with `glb_factory.py`:

- **Blue box** — Client (left)
- **Green box** — Server (right)
- **Yellow sphere** — SYN packet
- **Orange sphere** — SYN-ACK packet
- **Green sphere** — ACK packet
- **Light blue bar** — Established connection

### View the scene

1. Drag `handshake.glb` into [gltf-viewer.donmccurdy.com](https://gltf-viewer.donmccurdy.com/)
2. Or open in Three.js Editor: https://threejs.org/editor/
3. Or use `<model-viewer>` in an HTML page

### Forensic Protection

| File | Size | Status |
|------|------|--------|
| `handshake.glb` | 78 KB | Original (unsigned) |
| `handshake_blinded.glb` | 111 KB | Blinded (FAT32 + Ed25519) |

The blinded file contains a FAT32 partition with an embedded manifest signed with Ed25519.
The file is still fully functional — any GLTF viewer will load it normally.

To verify:
```bash
pixelguardctl verify --image scenes/handshake_blinded.glb
```

To re-blind:
```bash
PIXELGUARD_API_KEY=<key> bash ../../scripts/blind_scene.sh scenes/handshake.glb
```

## References

- Stevens, W.R. (1994). *TCP/IP Illustrated, Volume 1*. Addison-Wesley. §18.4
- RFC 793 — Transmission Control Protocol
- [glTF 2.0 Specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
