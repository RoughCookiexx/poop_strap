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
        """Continuously fetch output from the process queue and display it."""
        if self.app_var.get() in self.manager.output_queues:
            queue_out = self.manager.output_queues[self.app_var.get()]
            while not queue_out.empty():
                line = queue_out.get_nowait()
                self.output_text.insert(tk.END, line + "\n")
                self.output_text.see(tk.END)  # Scroll to the bottom

        # Call this method again after a short delay
        self.root.after(100, self.update_output)

    def run(self):
        self.root.mainloop()
