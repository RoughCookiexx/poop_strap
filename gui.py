import tkinter as tk
from tkinter import scrolledtext


class PoopStrapGUI:
    def __init__(self, manager):
        self.manager = manager
        self.root = tk.Tk()
        self.root.title("PoopStrap")

        # App selection dropdown
        self.app_var = tk.StringVar(self.root)
        self.app_dropdown = tk.OptionMenu(self.root, self.app_var, *self.manager.apps.keys())
        self.app_dropdown.pack()

        # Start/Stop buttons
        self.start_button = tk.Button(self.root, text="Start", command=self.start_app)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_app)
        self.stop_button.pack()

        # Output display
        self.output_text = scrolledtext.ScrolledText(self.root, height=20, width=80)
        self.output_text.pack()

        # Command input
        self.command_entry = tk.Entry(self.root)
        self.command_entry.pack()

        self.send_button = tk.Button(self.root, text="Send Command", command=self.send_command)
        self.send_button.pack()

        # Update output periodically
        self.update_output()

    def start_app(self):
        app_name = self.app_var.get()
        if app_name:
            self.manager.start_process(app_name, self.manager.apps[app_name]["command"],
                                       self.manager.apps[app_name]["cwd"])

    def stop_app(self):
        app_name = self.app_var.get()
        if app_name:
            self.manager.stop_process(app_name)

    def send_command(self):
        app_name = self.app_var.get()
        command = self.command_entry.get()
        if app_name and command:
            self.manager.send_command(app_name, command)
            self.command_entry.delete(0, tk.END)

    def update_output(self):
        self.output_text.delete(1.0, tk.END)
        for name, process in self.manager.processes.items():
            if process.poll() is None:
                self.output_text.insert(tk.END, f"[{name}]: Running\n")
            else:
                self.output_text.insert(tk.END, f"[{name}]: Stopped\n")
        self.root.after(1000, self.update_output)

    def run(self):
        self.root.mainloop()
