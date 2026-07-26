"""
glb_factory.py — Procedural GLB (glTF 2.0 Binary) generator for TCP/IP Illustrated 3D.

Zero dependencies. Pure Python. Generates valid .glb files that open in
any GLTF viewer (gltf-viewer.donmccurdy.com, Three.js GLTFLoader, Blender).

Usage:
    from glb_factory import GLBScene
    scene = GLBScene()
    scene.add(scene.box(0, 0, 0, 2, 1, 1, color=(0.2, 0.6, 1.0)))
    scene.add(scene.sphere(5, 0, 0, 0.5, color=(1, 0.8, 0)))
    scene.save("output.glb")
"""

import json
import math
import struct
import uuid
from dataclasses import dataclass, field
from typing import List, Tuple, Optional


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Material:
    name: str
    base_color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    metallic: float = 0.0
    roughness: float = 0.4
    emissive: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    alpha_mode: str = "OPAQUE"


@dataclass
class MeshData:
    name: str
    positions: List[float]     # flat [x,y,z, x,y,z, ...]
    normals: List[float]       # flat [nx,ny,nz, ...]
    colors: List[float]        # flat [r,g,b, ...]  (0-1 floats)
    indices: List[int]         # face indices [i0,i1,i2, ...]
    material_idx: int = 0


@dataclass
class Node:
    name: str
    mesh_idx: int
    translation: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)  # quaternion xyzw
    scale: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    children: List[int] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Geometry primitives
# ---------------------------------------------------------------------------

def _normalize(v):
    length = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
    if length < 1e-12:
        return (0.0, 1.0, 0.0)
    return (v[0] / length, v[1] / length, v[2] / length)


def _box_geometry(w: float, h: float, d: float, color: Tuple[float, float, float]):
    hw, hh, hd = w / 2, h / 2, d / 2
    r, g, b = color

    # 6 faces × 4 vertices = 24 vertices
    faces = [
        # Front (+Z)
        ((-hw, -hh, hd), (hw, -hh, hd), (hw, hh, hd), (-hw, hh, hd), (0, 0, 1)),
        # Back (-Z)
        ((hw, -hh, -hd), (-hw, -hh, -hd), (-hw, hh, -hd), (hw, hh, -hd), (0, 0, -1)),
        # Top (+Y)
        ((-hw, hh, hd), (hw, hh, hd), (hw, hh, -hd), (-hw, hh, -hd), (0, 1, 0)),
        # Bottom (-Y)
        ((-hw, -hh, -hd), (hw, -hh, -hd), (hw, -hh, hd), (-hw, -hh, hd), (0, -1, 0)),
        # Right (+X)
        ((hw, -hh, hd), (hw, -hh, -hd), (hw, hh, -hd), (hw, hh, hd), (1, 0, 0)),
        # Left (-X)
        ((-hw, -hh, -hd), (-hw, -hh, hd), (-hw, hh, hd), (-hw, hh, -hd), (-1, 0, 0)),
    ]

    positions, normals, colors, indices = [], [], [], []
    for i, (v0, v1, v2, v3, n) in enumerate(faces):
        base = i * 4
        for v in (v0, v1, v2, v3):
            positions.extend(v)
            normals.extend(n)
            colors.extend([r, g, b])
        indices.extend([base, base + 1, base + 2, base, base + 2, base + 3])

    return positions, normals, colors, indices


def _sphere_geometry(r: float, segments: int, rings: int, color: Tuple[float, float, float]):
    cr, cg, cb = color
    positions, normals, colors, indices = [], [], [], []

    for ring in range(rings + 1):
        phi = math.pi * ring / rings
        for seg in range(segments + 1):
            theta = 2 * math.pi * seg / segments
            nx = math.sin(phi) * math.cos(theta)
            ny = math.cos(phi)
            nz = math.sin(phi) * math.sin(theta)
            positions.extend([r * nx, r * ny, r * nz])
            normals.extend([nx, ny, nz])
            colors.extend([cr, cg, cb])

    for ring in range(rings):
        for seg in range(segments):
            a = ring * (segments + 1) + seg
            b = a + segments + 1
            indices.extend([a, b, a + 1, a + 1, b, b + 1])

    return positions, normals, colors, indices


def _cylinder_geometry(r: float, h: float, segments: int, color: Tuple[float, float, float]):
    cr, cg, cb = color
    positions, normals, colors, indices = [], [], [], []
    hh = h / 2

    # Side vertices: 2 rings (top + bottom)
    for ring_y in (hh, -hh):
        ny = 0.0 if ring_y == 0 else (1.0 if ring_y > 0 else -1.0)
        for seg in range(segments + 1):
            theta = 2 * math.pi * seg / segments
            nx = math.cos(theta)
            nz = math.sin(theta)
            positions.extend([r * nx, ring_y, r * nz])
            normals.extend([nx, ny, nz])
            colors.extend([cr, cg, cb])

    side_base = 0
    for seg in range(segments):
        a = side_base + seg
        b = a + segments + 1
        indices.extend([a, b, a + 1, a + 1, b, b + 1])

    # Top cap
    top_center = len(positions) // 3
    positions.extend([0, hh, 0])
    normals.extend([0, 1, 0])
    colors.extend([cr, cg, cb])
    for seg in range(segments + 1):
        theta = 2 * math.pi * seg / segments
        positions.extend([r * math.cos(theta), hh, r * math.sin(theta)])
        normals.extend([0, 1, 0])
        colors.extend([cr, cg, cb])
    for seg in range(segments):
        indices.extend([top_center, top_center + 1 + seg, top_center + 2 + seg])

    # Bottom cap
    bot_center = len(positions) // 3
    positions.extend([0, -hh, 0])
    normals.extend([0, -1, 0])
    colors.extend([cr, cg, cb])
    for seg in range(segments + 1):
        theta = 2 * math.pi * seg / segments
        positions.extend([r * math.cos(theta), -hh, r * math.sin(theta)])
        normals.extend([0, -1, 0])
        colors.extend([cr, cg, cb])
    for seg in range(segments):
        indices.extend([bot_center, bot_center + 2 + seg, bot_center + 1 + seg])

    return positions, normals, colors, indices


def _cone_geometry(r: float, h: float, segments: int, color: Tuple[float, float, float]):
    cr, cg, cb = color
    positions, normals, colors, indices = [], [], [], []
    hh = h / 2

    # Apex
    positions.extend([0, hh, 0])
    normals.extend([0, 1, 0])
    colors.extend([cr, cg, cb])

    # Base ring
    for seg in range(segments + 1):
        theta = 2 * math.pi * seg / segments
        nx = math.cos(theta)
        nz = math.sin(theta)
        positions.extend([r * nx, -hh, r * nz])
        normals.extend([nx, 0, nz])
        colors.extend([cr, cg, cb])

    for seg in range(segments):
        indices.extend([0, 1 + seg, 2 + seg])

    # Bottom cap
    bot_center = len(positions) // 3
    positions.extend([0, -hh, 0])
    normals.extend([0, -1, 0])
    colors.extend([cr, cg, cb])
    for seg in range(segments + 1):
        theta = 2 * math.pi * seg / segments
        positions.extend([r * math.cos(theta), -hh, r * math.sin(theta)])
        normals.extend([0, -1, 0])
        colors.extend([cr, cg, cb])
    for seg in range(segments):
        indices.extend([bot_center, bot_center + 2 + seg, bot_center + 1 + seg])

    return positions, normals, colors, indices


def _torus_geometry(major_r: float, minor_r: float, major_segments: int,
                    minor_segments: int, color: Tuple[float, float, float]):
    cr, cg, cb = color
    positions, normals, colors, indices = [], [], [], []

    for i in range(major_segments + 1):
        theta = 2 * math.pi * i / major_segments
        ct, st = math.cos(theta), math.sin(theta)
        for j in range(minor_segments + 1):
            phi = 2 * math.pi * j / minor_segments
            cp, sp = math.cos(phi), math.sin(phi)
            nx = ct * cp
            ny = sp
            nz = st * cp
            x = (major_r + minor_r * cp) * ct
            y = minor_r * sp
            z = (major_r + minor_r * cp) * st
            positions.extend([x, y, z])
            normals.extend([nx, ny, nz])
            colors.extend([cr, cg, cb])

    for i in range(major_segments):
        for j in range(minor_segments):
            a = i * (minor_segments + 1) + j
            b = a + minor_segments + 1
            indices.extend([a, b, a + 1, a + 1, b, b + 1])

    return positions, normals, colors, indices


def _arrow_geometry(length: float, head_r: float, shaft_r: float,
                    head_ratio: float, segments: int, color: Tuple[float, float, float]):
    """Arrow pointing along +X axis. Origin at center of shaft."""
    cr, cg, cb = color
    positions, normals, colors, indices = [], [], [], []

    shaft_len = length * (1 - head_ratio)
    head_len = length * head_ratio
    shaft_half = shaft_len / 2

    # Shaft (cylinder along X, rotated -90° around Z)
    # We build it along Y then the node rotation handles orientation
    shaft_hh = shaft_len / 2
    for ring_y in (shaft_hh, -shaft_hh):
        for seg in range(segments + 1):
            theta = 2 * math.pi * seg / segments
            positions.extend([shaft_r * math.cos(theta), ring_y, shaft_r * math.sin(theta)])
            normals.extend([math.cos(theta), 0, math.sin(theta)])
            colors.extend([cr, cg, cb])

    base = 0
    for seg in range(segments):
        a = base + seg
        b = a + segments + 1
        indices.extend([a, b, a + 1, a + 1, b, b + 1])

    # Head (cone on top)
    cone_base = len(positions) // 3
    cone_top = shaft_hh + head_len
    positions.extend([0, cone_top, 0])
    normals.extend([0, 1, 0])
    colors.extend([cr, cg, cb])

    for seg in range(segments + 1):
        theta = 2 * math.pi * seg / segments
        positions.extend([head_r * math.cos(theta), shaft_hh, head_r * math.sin(theta)])
        normals.extend([math.cos(theta), 0, math.sin(theta)])
        colors.extend([cr, cg, cb])

    for seg in range(segments):
        indices.extend([cone_base, cone_base + 1 + seg, cone_base + 2 + seg])

    return positions, normals, colors, indices


# ---------------------------------------------------------------------------
# GLB builder
# ---------------------------------------------------------------------------

class GLBScene:
    """
    Procedural GLB generator.

    Usage:
        scene = GLBScene()
        scene.add(scene.box(0, 0, 0, 2, 1, 1, color=(0.2, 0.6, 1.0)))
        scene.add(scene.sphere(5, 0, 0, 0.5, color=(1, 0.8, 0)))
        scene.save("output.glb")
    """

    def __init__(self):
        self._meshes: List[MeshData] = []
        self._materials: List[Material] = []
        self._nodes: List[Node] = []
        self._root_nodes: List[int] = []
        self._default_material = Material(
            name="default",
            base_color=(0.8, 0.8, 0.8, 1.0),
            metallic=0.0,
            roughness=0.5,
        )
        self._materials.append(self._default_material)

    def add(self, node: Node) -> Node:
        """Add a node to the scene graph (root level). Returns the node."""
        idx = len(self._nodes) - 1  # node was already appended by primitive
        self._root_nodes.append(idx)
        return node

    # -- Material management --------------------------------------------------

    def add_material(self, name: str, color: Tuple[float, float, float],
                     metallic: float = 0.0, roughness: float = 0.4,
                     emissive: Tuple[float, float, float] = (0, 0, 0)) -> int:
        mat = Material(name=name, base_color=(*color, 1.0),
                       metallic=metallic, roughness=roughness, emissive=emissive)
        self._materials.append(mat)
        return len(self._materials) - 1

    def _get_material(self, color: Optional[Tuple[float, float, float]],
                      emissive: Optional[Tuple[float, float, float]] = None) -> int:
        if color is None:
            return 0
        mat = Material(
            name=f"mat_{uuid.uuid4().hex[:8]}",
            base_color=(*color, 1.0),
            emissive=emissive or (0, 0, 0),
        )
        self._materials.append(mat)
        return len(self._materials) - 1

    # -- Geometry primitives --------------------------------------------------

    def box(self, cx: float, cy: float, cz: float,
            w: float, h: float, d: float,
            color: Optional[Tuple[float, float, float]] = None,
            name: str = "box") -> Node:
        positions, normals, colors, indices = _box_geometry(w, h, d, color or (0.8, 0.8, 0.8))
        mat_idx = self._get_material(color)
        mesh = MeshData(name=name, positions=positions, normals=normals,
                        colors=colors, indices=indices, material_idx=mat_idx)
        self._meshes.append(mesh)
        node = Node(name=name, mesh_idx=len(self._meshes) - 1,
                    translation=(cx, cy, cz))
        self._nodes.append(node)
        return node

    def sphere(self, cx: float, cy: float, cz: float, r: float,
               color: Optional[Tuple[float, float, float]] = None,
               segments: int = 24, rings: int = 16,
               emissive: Optional[Tuple[float, float, float]] = None,
               name: str = "sphere") -> Node:
        positions, normals, colors, indices = _sphere_geometry(r, segments, rings, color or (0.8, 0.8, 0.8))
        mat_idx = self._get_material(color, emissive)
        mesh = MeshData(name=name, positions=positions, normals=normals,
                        colors=colors, indices=indices, material_idx=mat_idx)
        self._meshes.append(mesh)
        node = Node(name=name, mesh_idx=len(self._meshes) - 1,
                    translation=(cx, cy, cz))
        self._nodes.append(node)
        return node

    def cylinder(self, cx: float, cy: float, cz: float,
                 r: float, h: float,
                 color: Optional[Tuple[float, float, float]] = None,
                 segments: int = 24, name: str = "cylinder") -> Node:
        positions, normals, colors, indices = _cylinder_geometry(r, h, segments, color or (0.8, 0.8, 0.8))
        mat_idx = self._get_material(color)
        mesh = MeshData(name=name, positions=positions, normals=normals,
                        colors=colors, indices=indices, material_idx=mat_idx)
        self._meshes.append(mesh)
        node = Node(name=name, mesh_idx=len(self._meshes) - 1,
                    translation=(cx, cy, cz))
        self._nodes.append(node)
        return node

    def cone(self, cx: float, cy: float, cz: float,
             r: float, h: float,
             color: Optional[Tuple[float, float, float]] = None,
             segments: int = 24, name: str = "cone") -> Node:
        positions, normals, colors, indices = _cone_geometry(r, h, segments, color or (0.8, 0.8, 0.8))
        mat_idx = self._get_material(color)
        mesh = MeshData(name=name, positions=positions, normals=normals,
                        colors=colors, indices=indices, material_idx=mat_idx)
        self._meshes.append(mesh)
        node = Node(name=name, mesh_idx=len(self._meshes) - 1,
                    translation=(cx, cy, cz))
        self._nodes.append(node)
        return node

    def arrow(self, x1: float, y1: float, z1: float,
              x2: float, y2: float, z2: float,
              color: Optional[Tuple[float, float, float]] = None,
              shaft_radius: float = 0.03, head_ratio: float = 0.25,
              segments: int = 12, name: str = "arrow") -> Node:
        dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
        length = math.sqrt(dx * dx + dy * dy + dz * dz)
        if length < 1e-6:
            return self.box(x1, y1, z1, 0.01, 0.01, 0.01, color=color, name=name)

        head_r = shaft_radius * 2.5
        positions, normals, colors_list, indices = _arrow_geometry(
            length, head_r, shaft_radius, head_ratio, segments, color or (0.8, 0.8, 0.8))

        # Rotate arrow from +Y to direction vector
        # Arrow is built along +Y axis, we need to orient it
        up = (0, 1, 0)
        direction = (dx / length, dy / length, dz / length)

        # Quaternion from up to direction
        dot = up[0] * direction[0] + up[1] * direction[1] + up[2] * direction[2]
        if dot < -0.9999:
            # Nearly opposite — rotate 180° around X
            quat = (1, 0, 0, 0)
        elif dot > 0.9999:
            quat = (0, 0, 0, 1)
        else:
            ax = up[1] * direction[2] - up[2] * direction[1]
            ay = up[2] * direction[0] - up[0] * direction[2]
            az = up[0] * direction[1] - up[1] * direction[0]
            s = math.sqrt((1 + dot) * 2)
            inv_s = 1 / s
            quat = (ax * inv_s, ay * inv_s, az * inv_s, s / 2)
            # Normalize
            ql = math.sqrt(quat[0]**2 + quat[1]**2 + quat[2]**2 + quat[3]**2)
            quat = tuple(q / ql for q in quat)

        mat_idx = self._get_material(color)
        mesh = MeshData(name=name, positions=positions, normals=normals,
                        colors=colors_list, indices=indices, material_idx=mat_idx)
        self._meshes.append(mesh)

        # Place at midpoint, oriented
        mx, my, mz = (x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2
        node = Node(name=name, mesh_idx=len(self._meshes) - 1,
                    translation=(mx, my, mz), rotation=quat)
        self._nodes.append(node)
        return node

    def torus(self, cx: float, cy: float, cz: float,
              major_r: float, minor_r: float,
              color: Optional[Tuple[float, float, float]] = None,
              major_segments: int = 32, minor_segments: int = 12,
              name: str = "torus") -> Node:
        positions, normals, colors, indices = _torus_geometry(
            major_r, minor_r, major_segments, minor_segments, color or (0.8, 0.8, 0.8))
        mat_idx = self._get_material(color)
        mesh = MeshData(name=name, positions=positions, normals=normals,
                        colors=colors, indices=indices, material_idx=mat_idx)
        self._meshes.append(mesh)
        node = Node(name=name, mesh_idx=len(self._meshes) - 1,
                    translation=(cx, cy, cz))
        self._nodes.append(node)
        return node

    # -- GLB serialization ----------------------------------------------------

    def save(self, path: str) -> str:
        """Serialize scene to GLB file. Returns the output path."""
        glb_data = self._build_glb()
        with open(path, "wb") as f:
            f.write(glb_data)
        return path

    def to_bytes(self) -> bytes:
        """Serialize scene to GLB bytes."""
        return self._build_glb()

    def _build_glb(self) -> bytes:
        # Build binary buffer from all meshes
        bin_chunks = []
        buffer_views = []
        accessors = []
        meshes = []
        current_offset = 0

        for mesh_data in self._meshes:
            # Pack positions (float32 × 3)
            pos_bytes = struct.pack(f"<{len(mesh_data.positions)}f", *mesh_data.positions)
            pos_count = len(mesh_data.positions) // 3
            pos_min = [min(mesh_data.positions[i::3]) for i in range(3)]
            pos_max = [max(mesh_data.positions[i::3]) for i in range(3)]

            pos_bv_idx = len(buffer_views)
            buffer_views.append({
                "buffer": 0,
                "byteOffset": current_offset,
                "byteLength": len(pos_bytes),
                "target": 34962,  # ARRAY_BUFFER
            })
            pos_acc_idx = len(accessors)
            accessors.append({
                "bufferView": pos_bv_idx,
                "componentType": 5126,  # FLOAT
                "count": pos_count,
                "type": "VEC3",
                "min": pos_min,
                "max": pos_max,
            })
            bin_chunks.append(pos_bytes)
            # Pad to 4-byte alignment
            pad = (4 - len(pos_bytes) % 4) % 4
            if pad:
                bin_chunks.append(b"\x00" * pad)
                current_offset += len(pos_bytes) + pad
            else:
                current_offset += len(pos_bytes)

            # Pack normals (float32 × 3)
            norm_bytes = struct.pack(f"<{len(mesh_data.normals)}f", *mesh_data.normals)
            norm_count = len(mesh_data.normals) // 3

            norm_bv_idx = len(buffer_views)
            buffer_views.append({
                "buffer": 0,
                "byteOffset": current_offset,
                "byteLength": len(norm_bytes),
                "target": 34962,
            })
            norm_acc_idx = len(accessors)
            accessors.append({
                "bufferView": norm_bv_idx,
                "componentType": 5126,
                "count": norm_count,
                "type": "VEC3",
            })
            bin_chunks.append(norm_bytes)
            pad = (4 - len(norm_bytes) % 4) % 4
            if pad:
                bin_chunks.append(b"\x00" * pad)
                current_offset += len(norm_bytes) + pad
            else:
                current_offset += len(norm_bytes)

            # Pack colors (float32 × 3, converted from 0-1 floats)
            col_bytes = struct.pack(f"<{len(mesh_data.colors)}f", *mesh_data.colors)
            col_count = len(mesh_data.colors) // 3

            col_bv_idx = len(buffer_views)
            buffer_views.append({
                "buffer": 0,
                "byteOffset": current_offset,
                "byteLength": len(col_bytes),
                "target": 34962,
            })
            col_acc_idx = len(accessors)
            accessors.append({
                "bufferView": col_bv_idx,
                "componentType": 5126,
                "count": col_count,
                "type": "VEC3",
            })
            bin_chunks.append(col_bytes)
            pad = (4 - len(col_bytes) % 4) % 4
            if pad:
                bin_chunks.append(b"\x00" * pad)
                current_offset += len(col_bytes) + pad
            else:
                current_offset += len(col_bytes)

            # Pack indices (uint16)
            idx_bytes = struct.pack(f"<{len(mesh_data.indices)}H", *mesh_data.indices)

            idx_bv_idx = len(buffer_views)
            buffer_views.append({
                "buffer": 0,
                "byteOffset": current_offset,
                "byteLength": len(idx_bytes),
                "target": 34963,  # ELEMENT_ARRAY_BUFFER
            })
            idx_acc_idx = len(accessors)
            accessors.append({
                "bufferView": idx_bv_idx,
                "componentType": 5123,  # UNSIGNED_SHORT
                "count": len(mesh_data.indices),
                "type": "SCALAR",
            })
            bin_chunks.append(idx_bytes)
            pad = (4 - len(idx_bytes) % 4) % 4
            if pad:
                bin_chunks.append(b"\x00" * pad)
                current_offset += len(idx_bytes) + pad
            else:
                current_offset += len(idx_bytes)

            meshes.append({
                "name": mesh_data.name,
                "primitives": [{
                    "attributes": {
                        "POSITION": pos_acc_idx,
                        "NORMAL": norm_acc_idx,
                        "COLOR_0": col_acc_idx,
                    },
                    "indices": idx_acc_idx,
                    "material": mesh_data.material_idx,
                }],
            })

        # Build node list
        gltf_nodes = []
        for node in self._nodes:
            n = {
                "name": node.name,
                "mesh": node.mesh_idx,
            }
            if node.translation != (0, 0, 0):
                n["translation"] = list(node.translation)
            if node.rotation != (0, 0, 0, 1):
                n["rotation"] = list(node.rotation)
            if node.scale != (1, 1, 1):
                n["scale"] = list(node.scale)
            if node.children:
                n["children"] = node.children
            gltf_nodes.append(n)

        # Build materials
        gltf_materials = []
        for mat in self._materials:
            m = {
                "name": mat.name,
                "pbrMetallicRoughness": {
                    "baseColorFactor": list(mat.base_color),
                    "metallicFactor": mat.metallic,
                    "roughnessFactor": mat.roughness,
                },
            }
            if mat.emissive != (0, 0, 0):
                m["emissiveFactor"] = list(mat.emissive)
            if mat.alpha_mode != "OPAQUE":
                m["alphaMode"] = mat.alpha_mode
            gltf_materials.append(m)

        # Assemble GLTF JSON
        gltf = {
            "asset": {
                "generator": "glb_factory v1.0 (TCP/IP Illustrated 3D)",
                "version": "2.0",
            },
            "scene": 0,
            "scenes": [{"name": "Scene", "nodes": self._root_nodes}],
            "nodes": gltf_nodes,
            "meshes": meshes,
            "materials": gltf_materials,
            "accessors": accessors,
            "bufferViews": buffer_views,
            "buffers": [{"byteLength": current_offset}],
        }

        # Encode JSON chunk
        json_bytes = json.dumps(gltf, separators=(",", ":")).encode("utf-8")
        # Pad JSON to 4-byte alignment with spaces
        json_pad = (4 - len(json_bytes) % 4) % 4
        if json_pad:
            json_bytes += b" " * json_pad

        # Encode binary chunk
        bin_data = b"".join(bin_chunks)
        bin_pad = (4 - len(bin_data) % 4) % 4
        if bin_pad:
            bin_data += b"\x00" * bin_pad

        # GLB header
        total_length = 12 + 8 + len(json_bytes) + 8 + len(bin_data)
        header = struct.pack("<III", 0x46546C67, 2, total_length)  # glTF 2.0

        # JSON chunk
        json_chunk = struct.pack("<II", len(json_bytes), 0x4E4F534A) + json_bytes  # "JSON"

        # Binary chunk
        bin_chunk = struct.pack("<II", len(bin_data), 0x004E4942) + bin_data  # "BIN\0"

        return header + json_chunk + bin_chunk

    def stats(self) -> dict:
        """Return scene statistics."""
        total_verts = sum(len(m.positions) // 3 for m in self._meshes)
        total_faces = sum(len(m.indices) // 3 for m in self._meshes)
        return {
            "meshes": len(self._meshes),
            "nodes": len(self._nodes),
            "materials": len(self._materials),
            "vertices": total_verts,
            "faces": total_faces,
        }


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    print("glb_factory.py — GLB scene generator")
    print("Import and use: from glb_factory import GLBScene")
    print()
    print("Quick demo:")

    scene = GLBScene()
    scene.add(scene.box(0, 0, 0, 1, 1, 1, color=(0.2, 0.6, 1.0), name="cube"))
    scene.add(scene.sphere(2.5, 0, 0, 0.5, color=(1, 0.8, 0), name="ball"))
    scene.add(scene.cylinder(-2.5, 0, 0, 0.3, 1.0, color=(0.2, 0.8, 0.3), name="pole"))
    stats = scene.stats()
    print(f"  {stats['meshes']} meshes, {stats['vertices']} vertices, {stats['faces']} faces")

    out = "/tmp/demo.glb"
    scene.save(out)
    import os
    size = os.path.getsize(out)
    print(f"  Saved to {out} ({size:,} bytes)")
    print()
    print("Open in: https://gltf-viewer.donmccurdy.com/")
