import http.server
import socketserver
import socket
import threading
import time

HTTP_PORT = 8081
RTSP_PORT = 554
DAHUA_PORT = 37777

class MockCameraHTTPHandler(http.server.SimpleHTTPRequestHandler):
    """Responds with realistic CCTV web management headers and HTML."""
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Server", "Embedded-Web-Server/3.1 (Hikvision-IPCam)")
        self.end_headers()
        html_content = """
        <html>
            <head><title>Hikvision Web Management Portal</title></head>
            <body>
                <h2>Hikvision IP Camera System</h2>
                <p>Status: Active | Firmware: v5.5.0 build 240829</p>
                <form method="POST">
                    <label>Username: <input type="text" name="user"/></label><br/>
                    <label>Password: <input type="password" name="pass"/></label><br/>
                    <input type="submit" value="Login"/>
                </form>
            </body>
        </html>
        """
        self.wfile.write(html_content.encode("utf-8"))

    def log_message(self, format, *args):
        # Suppress verbose standard console logging
        pass

def run_http_service():
    """Launches the mock HTTP administrative portal."""
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", HTTP_PORT), MockCameraHTTPHandler) as httpd:
        print(f"[*] Mock HTTP Service running on port {HTTP_PORT} (Web Management)")
        httpd.serve_forever()

def run_raw_port_listener(port: int, service_name: str):
    """Listens on non-HTTP ports (RTSP / Proprietary) to accept socket handshakes."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(("0.0.0.0", port))
        sock.listen(5)
        print(f"[*] Mock {service_name} Listener active on port {port}")
        while True:
            conn, _ = sock.accept()
            conn.close()
    except Exception as e:
        print(f"[-] Could not bind port {port} ({service_name}): {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("    STARTING MOCK CCTV / DVR SIMULATION APPLIANCE")
    print("=" * 60)

    # 1. Start HTTP Management thread
    http_thread = threading.Thread(target=run_http_service, daemon=True)
    http_thread.start()

    # 2. Start RTSP Listener thread
    rtsp_thread = threading.Thread(target=run_raw_port_listener, args=(RTSP_PORT, "RTSP Streaming"), daemon=True)
    rtsp_thread.start()

    # 3. Start Proprietary Port thread
    dahua_thread = threading.Thread(target=run_raw_port_listener, args=(DAHUA_PORT, "Dahua Management"), daemon=True)
    dahua_thread.start()

    print("\n[+] Mock Surveillance Device online! Press Ctrl+C to terminate.\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Shutting down mock device...")