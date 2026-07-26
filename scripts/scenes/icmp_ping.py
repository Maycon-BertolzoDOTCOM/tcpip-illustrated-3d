#!/usr/bin/env python3
"""
icmp_ping.py — Generate ICMP Echo Request/Reply 3D scene (Chapter 11).

Visual representation of Stevens TCP/IP Illustrated Vol.1 §11.2:

    Host A ── Echo Request (type 8) ──▶ Host B
    Host A ◀── Echo Reply (type 0) ──── Host B

    RTT measured as round-trip time.

Output: chapters/11-icmp-ping/scenes/icmp_ping.glb
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from glb_factory import GLBScene


def build_scene() -> GLBScene:
    scene = GLBScene()

    HOST_A = (0.235, 0.510, 0.965)   # Blue
    HOST_B = (0.133, 0.773, 0.369)   # Green
    REQ_COLOR = (1.000, 0.843, 0.000)  # Yellow
    REPLY_COLOR = (0.302, 0.851, 0.388)  # Green
    RTT_COLOR = (0.902, 0.333, 0.333)   # Red
    GROUND = (0.059, 0.086, 0.165)

    # Hosts
    scene.add(scene.box(cx=-4, cy=0, cz=0, w=1.5, h=1.2, d=1.2, color=HOST_A, name="Host_A"))
    scene.add(scene.box(cx=-4, cy=0.85, cz=0, w=1.1, h=0.2, d=0.05, color=HOST_A, name="HostA_Label"))
    scene.add(scene.box(cx=4, cy=0, cz=0, w=1.5, h=1.2, d=1.2, color=HOST_B, name="Host_B"))
    scene.add(scene.box(cx=4, cy=0.85, cz=0, w=1.1, h=0.2, d=0.05, color=HOST_B, name="HostB_Label"))

    # Echo Request arrows (Host A → Host B, top)
    for i in range(3):
        y = 0.6 - i * 0.15
        scene.add(scene.arrow(
            x1=-3.2, y1=y, z1=0, x2=3.2, y2=y, z2=0,
            color=REQ_COLOR, shaft_radius=0.025, name=f"Request_{i}"
        ))

    # Echo Reply arrows (Host B → Host A, bottom)
    for i in range(3):
        y = -0.3 - i * 0.15
        scene.add(scene.arrow(
            x1=3.2, y1=y, z1=0, x2=-3.2, y2=y, z2=0,
            color=REPLY_COLOR, shaft_radius=0.025, name=f"Reply_{i}"
        ))

    # Request spheres
    for i in range(3):
        scene.add(scene.sphere(
            cx=-1.0 + i * 2, cy=0.7, cz=0, r=0.15,
            color=REQ_COLOR, emissive=(0.4, 0.35, 0.0),
            segments=12, rings=8, name=f"ReqSphere_{i}"
        ))

    # Reply spheres
    for i in range(3):
        scene.add(scene.sphere(
            cx=1.0 - i * 2, cy=-0.5, cz=0, r=0.15,
            color=REPLY_COLOR, emissive=(0.12, 0.34, 0.15),
            segments=12, rings=8, name=f"ReplySphere_{i}"
        ))

    # RTT meter (red torus at center)
    scene.add(scene.torus(
        cx=0, cy=0, cz=0, major_r=0.6, minor_r=0.06,
        color=RTT_COLOR, major_segments=24, minor_segments=8, name="RTT_Meter"
    ))

    # Glow rings
    scene.add(scene.torus(cx=-4, cy=-0.65, cz=0, major_r=0.5, minor_r=0.04, color=HOST_A, major_segments=20, minor_segments=6, name="Ring_A"))
    scene.add(scene.torus(cx=4, cy=-0.65, cz=0, major_r=0.5, minor_r=0.04, color=HOST_B, major_segments=20, minor_segments=6, name="Ring_B"))

    # Platform
    scene.add(scene.box(cx=0, cy=-1.0, cz=0, w=12, h=0.1, d=3, color=GROUND, name="Platform"))

    return scene


def main():
    scene = build_scene()
    stats = scene.stats()
    print(f"ICMP Ping scene: {stats['meshes']} meshes, {stats['vertices']} vertices, {stats['faces']} faces")
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out_dir = os.path.join(base, "chapters", "11-icmp-ping", "scenes")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "icmp_ping.glb")
    scene.save(out_path)
    print(f"Saved: {out_path} ({os.path.getsize(out_path):,} bytes)")
    return out_path

if __name__ == "__main__":
    main()
