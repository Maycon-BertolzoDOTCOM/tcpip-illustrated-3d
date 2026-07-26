# TCP Sliding Window

Flow control mechanism for reliable data transmission.

## Concept

TCP uses a sliding window to control how much data can be in flight without overwhelming the receiver:

- **Sent & ACKed**: Data the receiver has confirmed (blue)
- **In Flight**: Data sent but not yet acknowledged (amber)
- **Can Send**: Window space available (dark)
- **Cannot Send**: Beyond the window (gray)

The window "slides" forward as ACKs arrive, allowing new data to be sent. This ensures the sender never transmits more than the receiver's buffer can handle.

## Reference

- Stevens, W. Richard. *TCP/IP Illustrated, Volume 1: The Protocols*. Chapter 20: TCP Bulk Data Flow
- RFC 9293 — Transmission Control Protocol

## How to View

Open `index.html` in a browser. No server required.

## Controls

- **Drag** to rotate
- **Scroll** to zoom
- **Auto-rotate** resumes after 3 seconds
