#!/usr/bin/env python3
"""
arp_resolution.py — Generate ARP Resolution 3D scene (Chapter 4).

Visual representation of Stevens TCP/IP Illustrated Vol.1 §4.5:

    Sender (Broadcast) → All hosts on LAN
    Target (Unicast) ← Target host responds with MAC

    "Who has 192.168.1.2? Tell 192.168.1.1"
    "192.168.1.2 is at aa:bb:cc:dd:ee:ff"

Output: chapters/04-arp/scenes/arp_resolution.glb
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from glb_factory import GLBScene


def build_scene() -> GLBScene:
    scene = GLBScene()

    # ── Colors ──────────────────────────────────────────────────────
    SENDER_COLOR     = (0.235, 0.510, 0.965)   # Blue
    TARGET_COLOR     = (0.133, 0.773, 0.369)   # Green
    OTHER_COLOR      = (0.500, 0.500, 0.550)   # Gray (other hosts)
    BROADCAST_COLOR  = (1.000, 0.843, 0.000)   # Yellow (broadcast)
    UNICAST_COLOR    = (0.302, 0.851, 0.388)   # Green (response)
    MAC_COLOR        = (0.902, 0.333, 0.333)   # Red (MAC address)
    GROUND_COLOR     = (0.059, 0.086, 0.165)

    # ── Sender (left) ──
    scene.add(scene.box(
        cx=-4, cy=0, cz=0, w=1.5, h=1.2, d=1.2,
        color=SENDER_COLOR, name="Sender"
    ))
    scene.add(scene.box(
        cx=-4, cy=0.85, cz=0, w=1.1, h=0.2, d=0.05,
        color=SENDER_COLOR, name="Sender_Label"
    ))

    # ── Target (right) ──
    scene.add(scene.box(
        cx=4, cy=0, cz=0, w=1.5, h=1.2, d=1.2,
        color=TARGET_COLOR, name="Target"
    ))
    scene.add(scene.box(
        cx=4, cy=0.85, cz=0, w=1.1, h=0.2, d=0.05,
        color=TARGET_COLOR, name="Target_Label"
    ))

    # ── Other hosts (background, dimmed) ──
    for i, x in enumerate([-1.5, 1.5]):
        scene.add(scene.box(
            cx=x, cy=0, cz=2, w=0.8, h=0.7, d=0.8,
            color=OTHER_COLOR, name=f"Host_{i}"
        ))

    # ── Broadcast arrow (yellow, fan-shaped concept) ──
    # Sender → all hosts (broadcast)
    scene.add(scene.arrow(
        x1=-3.2, y1=0.4, z1=0,
        x2=0, y2=0.4, z2=0,
        color=BROADCAST_COLOR, shaft_radius=0.04,
        name="Broadcast_ARP_Request"
    ))
    # Fan out to other hosts
    scene.add(scene.arrow(
        x1=-3.2, y1=0.4, z1=0,
        x2=-1.5, y2=0.4, z2=2,
        color=BROADCAST_COLOR, shaft_radius=0.025,
        name="Broadcast_Host0"
    ))
    scene.add(scene.arrow(
        x1=-3.2, y1=0.4, z1=0,
        x2=1.5, y2=0.4, z2=2,
        color=BROADCAST_COLOR, shaft_radius=0.025,
        name="Broadcast_Host1"
    ))
    scene.add(scene.arrow(
        x1=-3.2, y1=0.4, z1=0,
        x2=3.2, y2=0.4, z2=0,
        color=BROADCAST_COLOR, shaft_radius=0.04,
        name="Broadcast_Target"
    ))

    # ── Unicast response (green, Target → Sender) ──
    scene.add(scene.arrow(
        x1=3.2, y1=-0.4, z1=0,
        x2=-3.2, y2=-0.4, z2=0,
        color=UNICAST_COLOR, shaft_radius=0.04,
        name="Unicast_ARP_Reply"
    ))

    # ── Broadcast sphere ──
    scene.add(scene.sphere(
        cx=-1.5, cy=0.6, cz=0, r=0.2,
        color=BROADCAST_COLOR, emissive=(0.4, 0.35, 0.0),
        segments=12, rings=8, name="Broadcast_Packet"
    ))

    # ── Unicast sphere ──
    scene.add(scene.sphere(
        cx=1.5, cy=-0.6, cz=0, r=0.2,
        color=UNICAST_COLOR, emissive=(0.12, 0.34, 0.15),
        segments=12, rings=8, name="Unicast_Packet"
    ))

    # ── MAC address icon (small red cube at Target) ──
    scene.add(scene.box(
        cx=4, cy=-0.9, cz=0, w=0.6, h=0.15, d=0.15,
        color=MAC_COLOR, name="MAC_Address"
    ))

    # ── Glow rings ──
    scene.add(scene.torus(
        cx=-4, cy=-0.65, cz=0, major_r=0.5, minor_r=0.04,
        color=SENDER_COLOR, major_segments=20, minor_segments=6,
        name="Ring_Sender"
    ))
    scene.add(scene.torus(
        cx=4, cy=-0.65, cz=0, major_r=0.5, minor_r=0.04,
        color=TARGET_COLOR, major_segments=20, minor_segments=6,
        name="Ring_Target"
    ))

    # ── LAN cable (ground line) ──
    scene.add(scene.cylinder(
        cx=0, cy=-0.75, cz=1, r=0.02, h=8,
        color=(0.3, 0.3, 0.4), name="LAN_Cable"
    ))

    # ── Base platform ──
    scene.add(scene.box(
        cx=0, cy=-1.0, cz=1, w=12, h=0.1, d=5,
        color=GROUND_COLOR, name="Platform"
    ))

    return scene


def main():
    scene = build_scene()
    stats = scene.stats()
    print(f"ARP Resolution scene: {stats['meshes']} meshes, "
          f"{stats['vertices']} vertices, {stats['faces']} faces")

    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out_dir = os.path.join(base, "chapters", "04-arp", "scenes")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "arp_resolution.glb")

    scene.save(out_path)
    size = os.path.getsize(out_path)
    print(f"Saved: {out_path} ({size:,} bytes)")
    return out_path


if __name__ == "__main__":
    main()
