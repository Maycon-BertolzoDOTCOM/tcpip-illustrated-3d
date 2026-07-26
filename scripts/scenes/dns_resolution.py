#!/usr/bin/env python3
"""
dns_resolution.py — Generate DNS Resolution 3D scene (Chapter 12).

Visual representation of Stevens TCP/IP Illustrated Vol.1 §14.5:

    Client → Resolver → Root → TLD → Authoritative
                                      ↓
                                   IP Address
                                      ↓
    Client ← Resolver ← ← ← ← ← ← ← ←

5 nodes in a resolution chain with query/response flow.

Output: chapters/12-dns-resolution/scenes/dns_resolution.glb
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from glb_factory import GLBScene


def build_scene() -> GLBScene:
    scene = GLBScene()

    # ── Colors ──────────────────────────────────────────────────────
    CLIENT_COLOR     = (0.235, 0.510, 0.965)   # Blue
    RESOLVER_COLOR   = (0.608, 0.439, 0.961)   # Purple (#9B59B6)
    ROOT_COLOR       = (0.902, 0.333, 0.333)   # Red (#E74C3C)
    TLD_COLOR        = (1.000, 0.651, 0.000)   # Orange (#F39C12)
    AUTH_COLOR       = (0.133, 0.773, 0.369)   # Green (#22C55E)
    QUERY_COLOR      = (0.400, 0.700, 1.000)   # Light blue — query
    RESPONSE_COLOR   = (0.302, 0.851, 0.388)   # Green — response
    GROUND_COLOR     = (0.059, 0.086, 0.165)   # Dark

    # ── Layout: 5 nodes in a zigzag chain ──────────────────────────
    # Positions: left to right with vertical offset for visual depth
    positions = [
        (-6, 0, 0),     # Client
        (-3, 0, 1.5),   # Resolver
        (0, 0, 0),      # Root
        (3, 0, 1.5),    # TLD
        (6, 0, 0),      # Authoritative
    ]
    colors = [CLIENT_COLOR, RESOLVER_COLOR, ROOT_COLOR, TLD_COLOR, AUTH_COLOR]
    names = ["Client", "Resolver", "Root", "TLD", "Authoritative"]
    labels = ["Client", "Resolver", "Root Server", ".com TLD", "Authoritative"]

    # ── Host boxes ──────────────────────────────────────────────────
    for i, (pos, color, name) in enumerate(zip(positions, colors, names)):
        scene.add(scene.box(
            cx=pos[0], cy=pos[1], cz=pos[2],
            w=1.4, h=1.2, d=1.2,
            color=color, name=name
        ))
        # Label plate
        scene.add(scene.box(
            cx=pos[0], cy=pos[1] + 0.9, cz=pos[2],
            w=1.2, h=0.25, d=0.05,
            color=color, name=f"{name}_Label"
        ))

    # ── Query chain (blue arrows: Client → Resolver → Root → TLD → Auth) ──
    for i in range(len(positions) - 1):
        x1, y1, z1 = positions[i]
        x2, y2, z2 = positions[i + 1]
        scene.add(scene.arrow(
            x1 + 0.8, y1 + 0.3, z1,
            x2 - 0.8, y2 + 0.3, z2,
            color=QUERY_COLOR, shaft_radius=0.025,
            name=f"Query_{i}"
        ))

    # ── Response chain (green arrows: Auth → TLD → Root → Resolver → Client) ──
    for i in range(len(positions) - 1, 0, -1):
        x1, y1, z1 = positions[i]
        x2, y2, z2 = positions[i - 1]
        scene.add(scene.arrow(
            x1 - 0.8, y1 - 0.3, z1,
            x2 + 0.8, y2 - 0.3, z2,
            color=RESPONSE_COLOR, shaft_radius=0.025,
            name=f"Response_{i}"
        ))

    # ── Query spheres (moving along the chain) ──
    # Small spheres between each pair representing DNS queries
    for i in range(len(positions) - 1):
        x1, y1, z1 = positions[i]
        x2, y2, z2 = positions[i + 1]
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2 + 0.3
        mz = (z1 + z2) / 2
        scene.add(scene.sphere(
            cx=mx, cy=my, cz=mz, r=0.15,
            color=QUERY_COLOR, emissive=(0.16, 0.28, 0.4),
            segments=12, rings=8, name=f"QuerySphere_{i}"
        ))

    # ── Response spheres ──
    for i in range(len(positions) - 1, 0, -1):
        x1, y1, z1 = positions[i]
        x2, y2, z2 = positions[i - 1]
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2 - 0.3
        mz = (z1 + z2) / 2
        scene.add(scene.sphere(
            cx=mx, cy=my, cz=mz, r=0.15,
            color=RESPONSE_COLOR, emissive=(0.12, 0.34, 0.15),
            segments=12, rings=8, name=f"ResponseSphere_{i}"
        ))

    # ── Glow rings at each node ──
    for i, (pos, color) in enumerate(zip(positions, colors)):
        scene.add(scene.torus(
            cx=pos[0], cy=-0.65, cz=pos[2],
            major_r=0.5, minor_r=0.04,
            color=color, major_segments=20, minor_segments=6,
            name=f"Ring_{names[i]}"
        ))

    # ── Base platform ──
    scene.add(scene.box(
        cx=0, cy=-1.0, cz=0.75, w=16, h=0.1, d=4,
        color=GROUND_COLOR, name="Platform"
    ))

    # ── DNS record icon (small cube at Authoritative) ──
    scene.add(scene.box(
        cx=6, cy=1.2, cz=0, w=0.3, h=0.3, d=0.3,
        color=(1.0, 1.0, 0.0), name="DNS_Record"
    ))

    return scene


def main():
    scene = build_scene()
    stats = scene.stats()
    print(f"DNS Resolution scene: {stats['meshes']} meshes, "
          f"{stats['vertices']} vertices, {stats['faces']} faces")

    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out_dir = os.path.join(base, "chapters", "12-dns-resolution", "scenes")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "dns_resolution.glb")

    scene.save(out_path)
    size = os.path.getsize(out_path)
    print(f"Saved: {out_path} ({size:,} bytes)")
    return out_path


if __name__ == "__main__":
    main()
