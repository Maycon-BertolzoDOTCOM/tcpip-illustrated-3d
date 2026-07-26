#!/usr/bin/env python3
"""Take screenshots of all scenes via local HTTP server + Playwright."""
import os, http.server, threading, time
from pathlib import Path
from playwright.sync_api import sync_playwright

REPO = Path("/tmp/tcpip-3d")
SCENES_DIR = REPO / "scenes"
OUT = REPO / "screenshots"
OUT.mkdir(exist_ok=True)

PORT = 9876

SCENES = [
    ("splat-handshake",        "01"),
    ("splat-topology",         "02"),
    ("splat-dns",              "03"),
    ("splat-tcp-state",        "04"),
    ("splat-dhcp",             "05"),
    ("splat-ping",             "06"),
    ("hybrid-handshake",       "07"),
    ("01-three-way-handshake", "08"),
    ("02-ip-fragmentation",    "09"),
    ("03-tcp-window",          "10"),
    ("04-congestion-control",  "11"),
    ("05-dns-resolution",      "12"),
    ("06-http-over-tcp",       "13"),
    ("07-arp",                 "14"),
    ("08-tcp-state-machine",   "15"),
    ("09-icmp-traceroute",     "16"),
    ("10-udp-datagram",        "17"),
    ("11-routing-ttl",         "18"),
    ("12-icmp-ping",           "19"),
    ("13-dhcp-dora",           "20"),
]

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

def start_server():
    os.chdir(str(REPO))
    httpd = http.server.HTTPServer(("127.0.0.1", PORT), QuietHandler)
    httpd.serve_forever()

def screenshot_all():
    import os
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    time.sleep(0.5)

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        for folder, idx in SCENES:
            url = f"http://127.0.0.1:{PORT}/scenes/{folder}/index.html"
            name = f"{idx}_{folder}.png"
            print(f"  [{idx}/20] {folder}...", end=" ", flush=True)
            try:
                page.goto(url, wait_until="networkidle", timeout=20000)
                time.sleep(4)
                page.screenshot(path=str(OUT / name), type="png")
                size = (OUT / name).stat().st_size / 1024
                print(f"OK ({size:.0f} KB)")
            except Exception as e:
                print(f"FAIL: {e}")
        browser.close()

if __name__ == "__main__":
    screenshot_all()
