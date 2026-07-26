#!/bin/bash
# blind_scene.sh — Blind a GLB/PLY file with Sigil (FAT32 + Ed25519)
#
# Usage:
#   bash blind_scene.sh input.glb [output_blinded.glb]
#   bash blind_scene.sh --all  (blind all .glb in chapters/)
#
# Requires: Sigil server running on :8080 (or set SIGIL_URL)

set -euo pipefail

SIGIL_URL="${SIGIL_URL:-http://127.0.0.1:8080}"
AUTHOR="${AUTHOR:-Maycon Bertolzo}"
PROJECT="${PROJECT:-tcpip-3d}"

# Get API key from environment or Sigil log
if [ -z "${PIXELGUARD_API_KEY:-}" ]; then
    PIXELGUARD_API_KEY=$(head -1 /tmp/sigil.log 2>/dev/null | grep -oP 'Generated API key: \K.*' || true)
fi

if [ -z "$PIXELGUARD_API_KEY" ]; then
    echo "Error: Set PIXELGUARD_API_KEY or ensure Sigil server is running"
    echo "  export PIXELGUARD_API_KEY=<your-key>"
    exit 1
fi

blind_file() {
    local input="$1"
    local output="${2:-${input%.glb}_blinded.glb}"
    
    echo "Blinding: $input"
    echo "  Author:   $AUTHOR"
    echo "  Project:  $PROJECT"
    
    HTTP_CODE=$(curl -s -o "$output" -w "%{http_code}" \
        -X POST "$SIGIL_URL/blind" \
        -H "Authorization: Bearer $PIXELGUARD_API_KEY" \
        -F "image=@$input" \
        -F "author=$AUTHOR" \
        -F "project_id=$PROJECT")
    
    if [ "$HTTP_CODE" = "200" ]; then
        ORIGINAL_SIZE=$(stat -c%s "$input" 2>/dev/null || stat -f%z "$input")
        BLINDED_SIZE=$(stat -c%s "$output" 2>/dev/null || stat -f%z "$output")
        OVERHEAD=$((BLINDED_SIZE - ORIGINAL_SIZE))
        echo "  OK → $output (${BLINDED_SIZE} bytes, +${OVERHEAD} FAT32)"
    else
        echo "  FAILED (HTTP $HTTP_CODE)"
        rm -f "$output"
        return 1
    fi
}

if [ "${1:-}" = "--all" ]; then
    echo "Blinding all .glb files in chapters/..."
    find chapters/ -name "*.glb" ! -name "*_blinded*" | while read -r f; do
        blind_file "$f"
        echo
    done
elif [ -n "${1:-}" ]; then
    blind_file "$1" "${2:-}"
else
    echo "Usage:"
    echo "  $0 input.glb [output_blinded.glb]"
    echo "  $0 --all"
    echo
    echo "Environment:"
    echo "  PIXELGUARD_API_KEY  Sigil API key"
    echo "  SIGIL_URL           Sigil server URL (default: http://127.0.0.1:8080)"
    echo "  AUTHOR              Author name (default: Maycon Bertolzo)"
    echo "  PROJECT             Project ID (default: tcpip-3d)"
fi
