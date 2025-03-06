# a simple python server to transfer files over windows, Linux and Mac machines easily.
# created by: glitcher
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import signal
import sys

# Global variable to track if the server has been requested
server_requested = False

def color_message(message, color):
    colors = {
        "red": "\033[31m",
        "blue": "\033[34m",
        "green": "\033[32m",
        "reset": "\033[0m",
    }
    return f"{colors.get(color, colors['reset'])}{message}{colors['reset']}"

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_PUT(self):
        global server_requested
        server_requested = True  # Set the flag to indicate the server was requested

        try:
            file_length = int(self.headers['Content-Length'])
            file_path = self.path.strip("/") or "uploaded_file"  # Use default name if no file name is provided
            directory = os.path.dirname(file_path)

            # Ensure the directory exists
            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            with open(file_path, 'wb') as output_file:
                output_file.write(self.rfile.read(file_length))

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'File uploaded successfully.')

            # Log request status
            print(color_message(f"[+] PUT request received. Status: 200. File saved at: {file_path}", "green"))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())

            # Log request status
            print(color_message(f"[-] PUT request failed. Status: 500. Error: {str(e)}", "red"))

    def do_GET(self):
        global server_requested
        server_requested = True  # Set the flag to indicate the server was requested

        try:
            file_path = self.path.strip("/") or "index.html"
            if os.path.exists(file_path) and os.path.isfile(file_path):
                self.send_response(200)
                self.end_headers()
                with open(file_path, 'rb') as file:
                    self.wfile.write(file.read())

                # Log GET request status
                print(color_message(f"[+] GET request received. Status: 200. File served: {file_path}", "green"))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File not found.")

                # Log file not found
                print(color_message(f"[-] GET request received. Status: 404. File not found: {file_path}", "red"))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())

            # Log GET request error
            print(color_message(f"[-] GET request failed. Status: 500. Error: {str(e)}", "red"))

    def log_message(self, format, *args):
        # Suppress default logging to avoid cluttering the console
        return

def signal_handler(sig, frame):
    print(color_message("[-] Server shutting down gracefully due to interrupt.", "red"))
    sys.exit(0)

def run_server(port):
    try:
        server_address = ('0.0.0.0', port)
        httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
        print(color_message(f"[+] Server started on port {port}. Press Ctrl+C to stop.", "blue"))

        while True:
            httpd.handle_request()
    except KeyboardInterrupt:
        print(color_message("[-] Server interrupted by user. Shutting down.", "red"))
    except Exception as e:
        print(color_message(f"[-] Error occurred: {str(e)}. Shutting down.", "red"))

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    # Get port from command-line arguments or use default
    port = 80
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
            if port < 1 or port > 65535:
                raise ValueError("Invalid port range. Use a port between 1 and 65535.")
        except ValueError as ve:
            print(color_message(f"[-] {ve}. Falling back to default port {port}.", "red"))

    run_server(port)