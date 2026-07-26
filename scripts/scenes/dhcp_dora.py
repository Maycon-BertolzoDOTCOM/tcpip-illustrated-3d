#!/usr/bin/env python3
"""
dhcp_dora.py — Generate DHCP DORA 3D scene (Chapter 6).

Visual representation of Stevens TCP/IP Illustrated Vol.1 §16.9:

    Client                Server
      │                     │
      │── DISCOVER ────────▶│  (broadcast, 0.0.0.0 → 255.255.255.255)
      │                     │
      │◀── OFFER ───────────│  (unicast or broadcast, offer IP)
      │                     │
      │── REQUEST ─────────▶│  (broadcast, accepted IP)
      │                     │
      │◀── ACK ─────────────│  (broadcast, lease confirmed)

Output: chapters/06-dhcp-dora/scenes/dhcp_dora.glb
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from glb_factory import GLBScene


def build_scene() -> GLBScene:
    scene = GLBScene()

    # ── Colors ──────────────────────────────────────────────────────
    CLIENT_COLOR    = (0.235, 0.510, 0.965)   # Blue
    SERVER_COLOR    = (0.133, 0.773, 0.369)   # Green
    DISCOVER_COLOR  = (1.000, 0.843, 0.000)   # Yellow — DISCOVER
    OFFER_COLOR     = (0.608, 0.439, 0.961)   # Purple — OFFER
    REQUEST_COLOR   = (1.000, 0.549, 0.000)   # Orange — REQUEST
    ACK_COLOR       = (0.302, 0.851, 0.388)   # Green — ACK
    GROUND_COLOR    = (0.059, 0.086, 0.165)

    # ── Hosts ──
    scene.add(scene.box(
        cx=-4, cy=0, cz=0, w=1.5, h=1.2, d=1.2,
        color=CLIENT_COLOR, name="Client"
    ))
    scene.add(scene.box(
        cx=-4, cy=0.85, cz=0, w=1.1, h=0.2, d=0.05,
        color=CLIENT_COLOR, name="Client_Label"
    ))

    scene.add(scene.box(
        cx=4, cy=0, cz=0, w=1.5, h=1.2, d=1.2,
        color=SERVER_COLOR, name="DHCP_Server"
    ))
    scene.add(scene.box(
        cx=4, cy=0.85, cz=0, w=1.1, h=0.2, d=0.05,
        color=SERVER_COLOR, name="Server_Label"
    ))

    # ── DORA packets (4 arrows, staggered vertically) ──
    # DISCOVER (Client → Server, top)
    scene.add(scene.arrow(
        x1=-3.2, y1=0.5, z1=0,
        x2=3.2, y2=0.5, z2=0,
        color=DISCOVER_COLOR, shaft_radius=0.035,
        name="DISCOVER"
    ))
    scene.add(scene.sphere(
        cx=0, cy=0.7, cz=0, r=0.18,
        color=DISCOVER_COLOR, emissive=(0.4, 0.35, 0.0),
        segments=12, rings=8, name="DISCOVER_Packet"
    ))

    # OFFER (Server → Client)
    scene.add(scene.arrow(
        x1=3.2, y1=0.15, z1=0,
        x2=-3.2, y2=0.15, z2=0,
        color=OFFER_COLOR, shaft_radius=0.035,
        name="OFFER"
    ))
    scene.add(scene.sphere(
        cx=0, cy=0.35, cz=0, r=0.18,
        color=OFFER_COLOR, emissive=(0.24, 0.18, 0.38),
        segments=12, rings=8, name="OFFER_Packet"
    ))

    # REQUEST (Client → Server)
    scene.add(scene.arrow(
        x1=-3.2, y1=-0.2, z1=0,
        x2=3.2, y2=-0.2, z2=0,
        color=REQUEST_COLOR, shaft_radius=0.035,
        name="REQUEST"
    ))
    scene.add(scene.sphere(
        cx=0, cy=0.0, cz=0, r=0.18,
        color=REQUEST_COLOR, emissive=(0.4, 0.22, 0.0),
        segments=12, rings=8, name="REQUEST_Packet"
    ))

    # ACK (Server → Client, bottom)
    scene.add(scene.arrow(
        x1=3.2, y1=-0.55, z1=0,
        x2=-3.2, y2=-0.55, z2=0,
        color=ACK_COLOR, shaft_radius=0.035,
        name="ACK"
    ))
    scene.add(scene.sphere(
        cx=0, cy=-0.35, cz=0, r=0.18,
        color=ACK_COLOR, emissive=(0.12, 0.34, 0.15),
        segments=12, rings=8, name="ACK_Packet"
    ))

    # ── Step labels (small cubes) ──
    for i, (name, color, y) in enumerate([
        ("Step1", DISCOVER_COLOR, 0.9),
        ("Step2", OFFER_COLOR, 0.55),
        ("Step3", REQUEST_COLOR, 0.2),
        ("Step4", ACK_COLOR, -0.15),
    ]):
        scene.add(scene.box(
            cx=0, cy=y, cz=-0.8, w=0.4, h=0.15, d=0.05,
            color=color, name=name
        ))

    # ── IP address icon (yellow cube near ACK) ──
    scene.add(scene.box(
        cx=-4, cy=-0.9, cz=0, w=0.5, h=0.15, d=0.15,
        color=(1.0, 1.0, 0.0), name="IP_Assigned"
    ))

    # ── Glow rings ──
    scene.add(scene.torus(
        cx=-4, cy=-0.65, cz=0, major_r=0.5, minor_r=0.04,
        color=CLIENT_COLOR, major_segments=20, minor_segments=6,
        name="Ring_Client"
    ))
    scene.add(scene.torus(
        cx=4, cy=-0.65, cz=0, major_r=0.5, minor_r=0.04,
        color=SERVER_COLOR, major_segments=20, minor_segments=6,
        name="Ring_Server"
    ))

    # ── Base platform ──
    scene.add(scene.box(
        cx=0, cy=-1.0, cz=0, w=12, h=0.1, d=3,
        color=GROUND_COLOR, name="Platform"
    ))

    return scene


def main():
    scene = build_scene()
    stats = scene.stats()
    print(f"DHCP DORA scene: {stats['meshes']} meshes, "
          f"{stats['vertices']} vertices, {stats['faces']} faces")

    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out_dir = os.path.join(base, "chapters", "06-dhcp-dora", "scenes")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "dhcp_dora.glb")

    scene.save(out_path)
    size = os.path.getsize(out_path)
    print(f"Saved: {out_path} ({size:,} bytes)")
    return out_path


if __name__ == "__main__":
    main()
