# IP Fragmentation

How IP splits large packets to fit network MTU constraints.

## Concept

When an IP packet exceeds the Maximum Transmission Unit (MTU) of a network link, it is fragmented into smaller pieces:

1. A large packet leaves the source host
2. A router with a smaller MTU fragments the packet into 2+ pieces
3. Each fragment travels independently to the destination
4. The destination reassembles fragments using the Identification, Fragment Offset, and MF flags in the IP header

Fragmentation is defined in RFC 791 (Internet Protocol).

## Reference

- Stevens, W. Richard. *TCP/IP Illustrated, Volume 1: The Protocols*. Chapter 8: IP Fragmentation
- RFC 791 — Internet Protocol

## How to View

Open `index.html` in a browser. No server required.

## Controls

- **Drag** to rotate
- **Scroll** to zoom
- **Auto-rotate** resumes after 3 seconds
