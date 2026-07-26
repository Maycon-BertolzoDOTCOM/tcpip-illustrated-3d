# Three-Way Handshake

TCP connection establishment between two hosts.

## Concept

Before two hosts can exchange data over TCP, they must establish a connection via the three-way handshake:

1. **SYN**: The client sends a SYN (synchronize) packet to the server, indicating it wants to connect
2. **SYN-ACK**: The server responds with SYN-ACK, acknowledging the request and sending its own synchronization
3. **ACK**: The client sends an ACK back, confirming the connection is established

After this exchange, both sides can begin sending data. This is defined in RFC 793.

## Reference

- Stevens, W. Richard. *TCP/IP Illustrated, Volume 1: The Protocols*. Chapter 18: TCP Connection Establishment and Termination
- RFC 793 — Transmission Control Protocol

## How to View

Open `index.html` in a browser. No server required — Three.js is vendored locally.

## Controls

- **Drag** to rotate the scene
- **Scroll** to zoom
- **Auto-rotate** resumes after 3 seconds of inactivity
