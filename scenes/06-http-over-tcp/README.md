# HTTP over TCP

How the web works, from the packet's perspective.

## Concept

HTTP is an application protocol that runs over TCP. Each web page load involves:

1. **TCP Handshake** (3 yellow packets): SYN &rarr; SYN-ACK &rarr; ACK
2. **HTTP Request** (blue box): Client sends `GET /index.html HTTP/1.1`
3. **Server Processing** (pause): Server reads request, fetches resource
4. **HTTP Response** (green box): Server sends `HTTP/1.1 200 OK` with the page

The HTTP request and response are carried inside TCP segments, which are carried inside IP packets, which are carried inside Ethernet frames. This is the protocol stack in action.

## Reference

- Stevens, W. Richard. *TCP/IP Illustrated, Volume 1: The Protocols*. Chapter 27: HTTP
- RFC 7230 — HTTP/1.1 Message Syntax and Routing
- RFC 2616 — HTTP/1.1 (original)

## How to View

Open `index.html` in a browser. No server required.

## Controls

- **Drag** to rotate
- **Scroll** to zoom
