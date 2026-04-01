import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox

# Common ports with names (you can add more)
PORT_SERVICES = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS"
}

# -----------------------
# Scanner Logic
# -----------------------
class SimpleScanner:
    def __init__(self, target, start_port, end_port):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.open_ports = []
        self.stop_flag = False

    def scan_port(self, port):
        if self.stop_flag:
            return
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)

            result = sock.connect_ex((self.target, port))

            if result == 0:
                service = PORT_SERVICES.get(port, "Unknown")
                self.open_ports.append((port, service))
                print(f"Port {port} is open ({service})")

            sock.close()

        except Exception as e:
            print("Error:", e)

    def start_scan(self):
        threads = []

        for port in range(self.start_port, self.end_port + 1):
            t = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(t)
            t.start()

            # limit threads (beginner friendly)
            if len(threads) >= 100:
                for th in threads:
                    th.join()
                threads = []

        for th in threads:
            th.join()


# -----------------------
# GUI
# -----------------------
class ScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Port Scanner")

        self.scanner = None

        # Target
        tk.Label(root, text="Target IP").grid(row=0, column=0)
        self.target_entry = tk.Entry(root)
        self.target_entry.grid(row=0, column=1)

        # Start port
        tk.Label(root, text="Start Port").grid(row=1, column=0)
        self.start_entry = tk.Entry(root)
        self.start_entry.insert(0, "1")
        self.start_entry.grid(row=1, column=1)

        # End port
        tk.Label(root, text="End Port").grid(row=2, column=0)
        self.end_entry = tk.Entry(root)
        self.end_entry.insert(0, "100")
        self.end_entry.grid(row=2, column=1)

        # Buttons
        tk.Button(root, text="Start Scan", command=self.run_scan).grid(row=3, column=0)
        tk.Button(root, text="Stop", command=self.stop_scan).grid(row=3, column=1)

        # Output box
        self.output = tk.Text(root, height=15, width=50)
        self.output.grid(row=4, column=0, columnspan=2)

    def run_scan(self):
        target = self.target_entry.get()

        try:
            start_port = int(self.start_entry.get())
            end_port = int(self.end_entry.get())
        except:
            messagebox.showerror("Error", "Enter valid ports")
            return

        self.output.insert(tk.END, f"Scanning {target}...\n")

        self.scanner = SimpleScanner(target, start_port, end_port)

        thread = threading.Thread(target=self.perform_scan)
        thread.start()

    def perform_scan(self):
        self.scanner.start_scan()

        self.output.insert(tk.END, "\nScan Complete!\n")

        for port, service in self.scanner.open_ports:
            self.output.insert(tk.END, f"Port {port} open ({service})\n")

    def stop_scan(self):
        if self.scanner:
            self.scanner.stop_flag = True
            self.output.insert(tk.END, "\nScan Stopped\n")


# Run app
root = tk.Tk()
app = ScannerApp(root)
root.mainloop()