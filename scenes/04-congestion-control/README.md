# TCP Congestion Control

How TCP manages network congestion to avoid collapse.

## Concept

TCP uses a combination of slow start and congestion avoidance to probe network capacity:

- **Slow Start** (blue bars): cwnd doubles every RTT (exponential growth)
- **ssthresh** (yellow line): threshold between slow start and congestion avoidance
- **Congestion Avoidance** (green bars): cwnd increases by 1 MSS per RTT (linear growth)
- **Packet Loss** (red bars): cwnd drops to 1 (or to ssthresh), creating the classic "sawtooth" pattern

The bars animate one by one, building the congestion window evolution in real time.

## Reference

- Stevens, W. Richard. *TCP/IP Illustrated, Volume 1: The Protocols*. Chapter 21: TCP Congestion Control
- RFC 5681 — TCP Congestion Control
- RFC 2001 — TCP Slow Start, Congestion Avoidance, Fast Retransmit

## How to View

Open `index.html` in a browser. No server required.

## Controls

- **Drag** to rotate
- **Scroll** to zoom
