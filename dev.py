import http.server
import socketserver
import threading
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# Import main compile function from build.py
import build

PORT = 8080


class RebuildHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.last_rebuild = 0

    def on_any_event(self, event):
        if event.is_directory:
            return

        # Normalize path separators for comparison
        path = event.src_path.replace("\\", "/")

        # Only watch src/ or content/ to avoid infinite loops when output index.html changes
        if "src/" in path or "content/" in path:
            # Debounce events within 1 second to avoid duplicate triggers
            now = time.time()
            if now - self.last_rebuild > 1.0:
                print(f"\n[Watch] Change detected in {event.src_path}. Rebuilding...")
                try:
                    build.main()
                except Exception as e:
                    print(f"[ERR] Rebuild failed: {e}")
                self.last_rebuild = now


def start_server():
    handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            print(f"[Server] Serving static files at http://localhost:{PORT}/")
            httpd.serve_forever()
    except Exception as e:
        print(f"[ERR] Server failed to start: {e}")


def main():
    # Run initial build
    print("[Dev] Running initial site compilation...")
    build.main()

    # Start HTTP server in a background daemon thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Set up watchdog file observer
    event_handler = RebuildHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    print("[Dev] Development mode active.")
    print("[Dev] Watching for changes in content/ and src/... Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[Dev] Shutting down observer...")
        observer.stop()

    observer.join()


if __name__ == "__main__":
    main()
