# DNS Resolution

The hierarchical domain name system in action.

## Concept

When a client types `example.com` in the browser, DNS resolves it through a chain of servers:

1. **Client → Resolver**: Query for `example.com` A record
2. **Resolver → Root Server**: Where is `.com`?
3. **Root → Resolver**: Referral to `.com` TLD servers
4. **Resolver → TLD Server**: Where is `example.com`?
5. **TLD → Resolver**: Referral to `ns1.example.com` (authoritative)
6. **Resolver → Authoritative**: What is the A record for `example.com`?
7. **Authoritative → Resolver**: `93.184.216.34`
8. **Resolver → Client**: `93.184.216.34`

Each step is shown as a glowing packet traveling between DNS nodes. The entire chain is recursive — the resolver does the work on behalf of the client.

## Reference

- Stevens, W. Richard. *TCP/IP Illustrated, Volume 1: The Protocols*. Chapter 14: DNS
- RFC 1034 — Domain Names — Concepts and Facilities
- RFC 1035 — Domain Names — Implementation and Specification

## How to View

Open `index.html` in a browser. No server required.

## Controls

- **Drag** to rotate
- **Scroll** to zoom
