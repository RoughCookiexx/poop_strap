import subprocess
import threading
import time
import sys

from pront import pront

print(f"Running Python from: {sys.executable}")

class ProcessManager:
    def __init__(self):
        self.processes = {}

    def start_process(self, name, cmd):
        """Start a process if it’s not already running."""
        if name in self.processes and self.processes[name].poll() is None:
            print(f"{name} is already running.")
            return

        print(f"Starting {name}...")
        try:
            self.processes[name] = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True
            )
            threading.Thread(target=self._monitor_process, args=(name,), daemon=True).start()
        except Exception as e:
            print(f"Failed to start {name}: {e}")

    def _monitor_process(self, name):
        """Monitors process output and restarts it if it crashes."""
        process = self.processes.get(name)
        if not process:
            return

        for line in process.stdout:
            print(f"[{name}]: {line.strip()}")

        for line in process.stderr:
            print(f"[{name}]: {line.strip()}")

        print(f"{name} has stopped.")
        self.processes.pop(name, None)

    def stop_process(self, name):
        """Stops a running process."""
        if name not in self.processes or self.processes[name].poll() is not None:
            print(f"{name} is not running.")
            return

        print(f"Stopping {name}...")
        self.processes[name].terminate()
        self.processes[name].wait()
        self.processes.pop(name, None)

    def restart_process(self, name, command):
        """Restarts a process."""
        self.stop_process(name)
        time.sleep(1)
        self.start_process(name, command)

    def send_command(self, name, cmd):
        """Send a command to a running process."""
        if name not in self.processes or self.processes[name].poll() is not None:
            print(f"{name} is not running.")
            return

        try:
            self.processes[name].stdin.write(cmd + "\n")
            self.processes[name].stdin.flush()
        except Exception as e:
            pront("error", f"Failed to send command to {name}: {e}")

    def get_status(self):
        """Prints the status of all processes."""
        for name, process in self.processes.items():
            status = "Running" if process.poll() is None else "Stopped"
            pront("info", f"{name}: {status}")


# Make sure each app has a unique key
if __name__ == "__main__":
    manager = ProcessManager()

    python_path = sys.executable  # Use the same Python PoopStrap is running

    apps = {
        "twitch_jam_sesh": [python_path, "C:\\Users\\Tommy\\PycharmProjects\\twitch_jam_sesh\\twitch.py"],
        "trombone": [python_path, "C:\\Users\\Tommy\\PycharmProjects\\trombone\\twitch.py"],
        "sierra": [python_path, "C:\\Users\\Tommy\\PycharmProjects\\sierra-v3\\sierra.py"]
    }
    #
    # manager.start_process("twitch_bot", apps["twitch_bot"])

    while True:
        manager.get_status()
        command = input("Enter command ([app_name] [start|stop|restart|custom] or 'exit'): ").strip().split(maxsplit=1)

        if not command:
            continue

        if command[0].lower() == "exit":
            print("Shutting down PoopStrap...")
            for app in list(manager.processes.keys()):
                manager.stop_process(app)
            break

        app_name = command[0]
        action = command[1] if len(command) > 1 else ""

        if app_name not in apps:
            print(f"Unknown application: {app_name}")
            continue

        if action == "start":
            manager.start_process(app_name, apps[app_name])
        elif action == "stop":
            manager.stop_process(app_name)
        elif action == "restart":
            manager.restart_process(app_name, apps[app_name])
        elif action:
            manager.send_command(app_name, action)
        else:
            print("Invalid command format.")