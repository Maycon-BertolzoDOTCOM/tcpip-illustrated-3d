#!/usr/bin/env python3
"""
tcp_state_machine.py — Generate TCP State Machine 3D scene (Chapter 18).

11 TCP states arranged in a circle with transitions:

    CLOSED → LISTEN → SYN_SENT → SYN_RCVD → ESTABLISHED
      ↑                                            ↓
      └── TIME_WAIT ← FIN_WAIT_2 ← FIN_WAIT_1 ← CLOSE_WAIT
                          ↑                         ↓
                          └── CLOSING ←←←←←← LAST_ACK

Output: chapters/18-tcp-states/scenes/tcp_state_machine.glb
"""

import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from glb_factory import GLBScene


def build_scene() -> GLBScene:
    scene = GLBScene()

    GROUND = (0.059, 0.086, 0.165)
    STATES = [
        ("CLOSED",       (0.500, 0.500, 0.550)),  # Gray
        ("LISTEN",       (0.608, 0.439, 0.961)),  # Purple
        ("SYN_SENT",     (0.235, 0.510, 0.965)),  # Blue
        ("SYN_RCVD",     (0.400, 0.700, 1.000)),  # Light blue
        ("ESTABLISHED",  (0.133, 0.773, 0.369)),  # Green
        ("CLOSE_WAIT",   (1.000, 0.651, 0.000)),  # Orange
        ("LAST_ACK",     (1.000, 0.549, 0.000)),  # Dark orange
        ("FIN_WAIT_1",   (0.902, 0.333, 0.333)),  # Red
        ("FIN_WAIT_2",   (0.800, 0.200, 0.200)),  # Dark red
        ("CLOSING",      (0.700, 0.150, 0.150)),  # Darker red
        ("TIME_WAIT",    (0.961, 0.439, 0.608)),  # Pink
    ]

    RADIUS = 4.0
    n = len(STATES)

    # Arrange states in a circle (top-down view, Y=0)
    state_positions = []
    for i, (name, color) in enumerate(STATES):
        angle = 2 * math.pi * i / n - math.pi / 2  # start from top
        x = RADIUS * math.cos(angle)
        z = RADIUS * math.sin(angle)
        state_positions.append((x, z, name, color))

    # State nodes (spheres)
    for x, z, name, color in state_positions:
        scene.add(scene.sphere(
            cx=x, cy=0.3, cz=z, r=0.5,
            color=color, emissive=tuple(c * 0.3 for c in color),
            segments=16, rings=12, name=name
        ))

    # Transition arrows between consecutive states
    for i in range(n):
        x1, z1, _, _ = state_positions[i]
        x2, z2, _, _ = state_positions[(i + 1) % n]
        # Shorten arrow to not overlap spheres
        dx, dz = x2 - x1, z2 - z1
        dist = math.sqrt(dx*dx + dz*dz)
        ux, uz = dx/dist, dz/dist
        sx, sz = x1 + ux*0.6, z1 + uz*0.6
        ex, ez = x2 - ux*0.6, z2 - uz*0.6
        scene.add(scene.arrow(
            x1=sx, y1=0.3, z1=sz,
            x2=ex, y2=0.3, z2=ez,
            color=(0.4, 0.4, 0.5), shaft_radius=0.02,
            name=f"Transition_{i}"
        ))

    # ESTABLISHED → CLOSE_WAIT transition (special: active close)
    est_x, est_z = state_positions[4][0], state_positions[4][1]
    cw_x, cw_z = state_positions[5][0], state_positions[5][1]

    # Glow rings under each state
    for x, z, name, color in state_positions:
        scene.add(scene.torus(
            cx=x, cy=-0.2, cz=z, major_r=0.6, minor_r=0.04,
            color=color, major_segments=20, minor_segments=6,
            name=f"Ring_{name}"
        ))

    # Center label (ESTABLISHED is the goal)
    scene.add(scene.box(
        cx=0, cy=1.0, cz=0, w=2.0, h=0.3, d=0.1,
        color=(0.133, 0.773, 0.369), name="Center_Label"
    ))

    # Platform
    scene.add(scene.box(
        cx=0, cy=-0.5, cz=0, w=12, h=0.1, d=12,
        color=GROUND, name="Platform"
    ))

    return scene


def main():
    scene = build_scene()
    stats = scene.stats()
    print(f"TCP State Machine scene: {stats['meshes']} meshes, {stats['vertices']} vertices, {stats['faces']} faces")
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    out_dir = os.path.join(base, "chapters", "18-tcp-states", "scenes")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "tcp_state_machine.glb")
    scene.save(out_path)
    print(f"Saved: {out_path} ({os.path.getsize(out_path):,} bytes)")
    return out_path

if __name__ == "__main__":
    main()
