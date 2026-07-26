#!/usr/bin/env python3
"""
tcp_handshake.py — Generate TCP Three-Way Handshake 3D scene (Chapter 8).

Visual representation of Stevens TCP/IP Illustrated Vol.1 §18.4:

    Cliente                              Servidor
      │                                    │
      │──── SYN (seq=x) ────────────────▶│
      │                                    │
      │◀─── SYN-ACK (seq=y, ack=x+1) ───│
      │                                    │
      │──── ACK (seq=x+1, ack=y+1) ─────▶│
      │                                    │
      │◀═══════ CONEXÃO ESTABELECIDA ════▶│

Output: chapters/08-tcp-connection/scenes/handshake.glb
"""

import os
import sys

# Add parent dir to path for glb_factory import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from glb_factory import GLBScene


def build_scene() -> GLBScene:
    scene = GLBScene()

    # ── Colors ──────────────────────────────────────────────────────
    CLIENT_COLOR    = (0.235, 0.510, 0.965)   # #3B82F6 blue
    SERVER_COLOR    = (0.133, 0.773, 0.369)   # #22C55E green
    SYN_COLOR       = (1.000, 0.843, 0.000)   # #FFD700 yellow — SYN
    SYNACK_COLOR    = (1.000, 0.549, 0.000)   # #FF8C00 orange — SYN-ACK
    ACK_COLOR       = (0.302, 0.851, 0.388)   # #4ADE80 green — ACK
    CONNECT_COLOR   = (0.500, 0.800, 1.000)   # light blue — established
    LABEL_COLOR     = (1.000, 1.000, 1.000)   # white
    GROUND_COLOR    = (0.059, 0.086, 0.165)   # #0F172A dark

    # ── Hosts ───────────────────────────────────────────────────────
    # Cliente (left side)
    scene.add(scene.box(
        cx=-5, cy=0, cz=0, w=2.0, h=1.5, d=1.5,
        color=CLIENT_COLOR, name="Cliente"
    ))
    # Monitor screen on client
    scene.add(scene.box(
        cx=-5, cy=0.9, cz=0, w=1.4, h=0.6, d=0.1,
        color=(0.1, 0.1, 0.15), name="ClientScreen"
    ))

    # Servidor (right side)
    scene.add(scene.box(
        cx=5, cy=0, cz=0, w=2.0, h=1.5, d=1.5,
        color=SERVER_COLOR, name="Servidor"
    ))
    # Server rack lights
    for i in range(3):
        scene.add(scene.box(
            cx=5, cy=0.3 + i * 0.35, cz=0.76, w=0.8, h=0.1, d=0.05,
            color=(0.2, 1.0, 0.3) if i % 2 == 0 else (1.0, 0.3, 0.2),
            name=f"ServerLED{i}"
        ))

    # ── Connection cable (ground line) ──────────────────────────────
    scene.add(scene.cylinder(
        cx=0, cy=-0.75, cz=0, r=0.02, h=10.0,
        color=(0.3, 0.3, 0.4), name="Cable"
    ))

    # ── SYN packet (yellow sphere — Client → Server) ────────────────
    scene.add(scene.sphere(
        cx=-2.5, cy=0.3, cz=0, r=0.25,
        color=SYN_COLOR, emissive=(0.4, 0.35, 0.0),
        segments=16, rings=12, name="SYN"
    ))

    # ── SYN label (small box as placeholder) ────────────────────────
    scene.add(scene.box(
        cx=-2.5, cy=0.8, cz=0, w=0.6, h=0.2, d=0.05,
        color=SYN_COLOR, name="SYN_Label"
    ))

    # ── SYN-ACK packet (orange sphere — Server → Client) ────────────
    scene.add(scene.sphere(
        cx=0, cy=0.3, cz=0, r=0.25,
        color=SYNACK_COLOR, emissive=(0.4, 0.22, 0.0),
        segments=16, rings=12, name="SYNACK"
    ))

    scene.add(scene.box(
        cx=0, cy=0.8, cz=0, w=0.8, h=0.2, d=0.05,
        color=SYNACK_COLOR, name="SYNACK_Label"
    ))

    # ── ACK packet (green sphere — Client → Server) ─────────────────
    scene.add(scene.sphere(
        cx=2.5, cy=0.3, cz=0, r=0.25,
        color=ACK_COLOR, emissive=(0.12, 0.35, 0.15),
        segments=16, rings=12, name="ACK"
    ))

    scene.add(scene.box(
        cx=2.5, cy=0.8, cz=0, w=0.5, h=0.2, d=0.05,
        color=ACK_COLOR, name="ACK_Label"
    ))

    # ── Established connection bar (double arrow) ───────────────────
    # Left half
    scene.add(scene.cylinder(
        cx=-2.5, cy=-0.3, cz=0, r=0.04, h=4.5,
        color=CONNECT_COLOR, name="EstablishedLeft"
    ))
    # Right half
    scene.add(scene.cylinder(
        cx=2.5, cy=-0.3, cz=0, r=0.04, h=4.5,
        color=CONNECT_COLOR, name="EstablishedRight"
    ))
    # Center glow ring
    scene.add(scene.torus(
        cx=0, cy=-0.3, cz=0, major_r=0.4, minor_r=0.05,
        color=CONNECT_COLOR, major_segments=24, minor_segments=8,
        name="EstablishedRing"
    ))

    # ── Base platform ───────────────────────────────────────────────
    scene.add(scene.box(
        cx=0, cy=-1.0, cz=0, w=14, h=0.1, d=3,
        color=GROUND_COLOR, name="Platform"
    ))

    return scene


def main():
    scene = build_scene()
    stats = scene.stats()
    print(f"TCP Handshake scene: {stats['meshes']} meshes, "
          f"{stats['vertices']} vertices, {stats['faces']} faces")

    # Determine output path
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out_dir = os.path.join(base, "chapters", "08-tcp-connection", "scenes")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "handshake.glb")

    scene.save(out_path)
    size = os.path.getsize(out_path)
    print(f"Saved: {out_path} ({size:,} bytes)")

    # Also save a copy in root for quick testing
    root_copy = os.path.join(base, "handshake_demo.glb")
    scene.save(root_copy)
    print(f"Copy:  {root_copy} ({os.path.getsize(root_copy):,} bytes)")

    return out_path


if __name__ == "__main__":
    main()
