import tkinter as tk
from tkinter import scrolledtext
from queue import Queue


class PoopStrapGUI:
    def __init__(self, manager):
        self.manager = manager
        self.root = tk.Tk()
        self.root.title("PoopStrap")
        self.root.configure(bg="#2c2f33")
        self.root.geometry("600x400")

        # Main frame with padding and border
        self.main_frame = tk.Frame(self.root, bg="#2c2f33", padx=10, pady=10, borderwidth=3, relief="solid")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Left column (app list)
        self.app_list_frame = tk.Frame(self.main_frame, bg="#23272a", padx=5, pady=5)
        self.app_list_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.app_buttons = {}

        # Right side (app output and controls)
        self.right_frame = tk.Frame(self.main_frame, bg="#2c2f33", padx=5, pady=5)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Label for selected app
        self.selected_app_label = tk.Label(self.right_frame, text="SELECT AN APP", bg="#2c2f33", fg="white",
                                           font=("Arial Black", 14, "bold"))
        self.selected_app_label.pack(pady=5)

        # Output text box
        self.output_box = scrolledtext.ScrolledText(self.right_frame, bg="#23272a", fg="white", wrap=tk.WORD, height=15,
                                                    borderwidth=2, relief="solid")
        self.output_box.pack(fill=tk.BOTH, expand=True)
        self.output_box.config(state=tk.DISABLED)
        self.output_box.config(yscrollcommand=lambda *args: None)  # Hide scrollbar
        self.output_box.vbar.pack_forget()  # Remove scrollbar from view

        # Controls frame
        self.controls_frame = tk.Frame(self.right_frame, bg="#2c2f33")
        self.controls_frame.pack(fill=tk.X, pady=5)

        # Start/Stop/Restart buttons
        self.start_button = tk.Button(self.controls_frame, text="START", command=self.start_app, bg="#43b581",
                                      fg="white", width=8, font=("Arial Black", 10, "bold"))
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.controls_frame, text="STOP", command=self.stop_app, bg="#f04747", fg="white",
                                     width=8, font=("Arial Black", 10, "bold"))
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.restart_button = tk.Button(self.controls_frame, text="RESTART", command=self.restart_app, bg="#faa61a",
                                        fg="white", width=8, font=("Arial Black", 10, "bold"))
        self.restart_button.pack(side=tk.LEFT, padx=5)

        # Command input and button
        self.command_frame = tk.Frame(self.right_frame, bg="#2c2f33")
        self.command_frame.pack(fill=tk.X, pady=5)

        self.command_entry = tk.Entry(self.command_frame, bg="#40444b", fg="white", width=30)
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.command_entry.bind("<Return>", lambda event: self.send_command())  # Enter key sends command

        self.send_button = tk.Button(self.command_frame, text="SEND", command=self.send_command, bg="#7289da",
                                     fg="white", width=8, font=("Arial Black", 10, "bold"))
        self.send_button.pack(side=tk.RIGHT, padx=5)

        # Store output logs
        self.output_logs = {}

        # Populate app list
        self.selected_app = None
        for app_name in self.manager.apps.keys():
            self.add_app_button(app_name)

        self.update_output()
        self.root.mainloop()

    def add_app_button(self, app_name):
        button = tk.Button(self.app_list_frame, text=app_name, width=15, command=lambda: self.select_app(app_name),
                           font=("Arial", 10, "bold"))
        button.pack(pady=2, fill=tk.X)
        self.app_buttons[app_name] = button
        self.update_app_status(app_name)

    def select_app(self, app_name):
        self.selected_app = app_name
        self.selected_app_label.config(text=app_name.upper())
        self.output_box.config(state=tk.NORMAL)
        self.output_box.delete(1.0, tk.END)
        if app_name in self.output_logs:
            self.output_box.insert(tk.END, self.output_logs[app_name])
        self.output_box.config(state=tk.DISABLED)

    def update_app_status(self, app_name):
        status = "Running" if app_name in self.manager.processes and self.manager.processes[
            app_name].poll() is None else "Stopped"
        color = "#43b581" if status == "Running" else "#f04747"
        self.app_buttons[app_name].config(bg=color, fg="white")

    def start_app(self):
        if self.selected_app:
            self.manager.start_process(self.selected_app, self.manager.apps[self.selected_app]["command"],
                                       self.manager.apps[self.selected_app]["cwd"])
            self.update_app_status(self.selected_app)

    def stop_app(self):
        if self.selected_app:
            self.manager.stop_process(self.selected_app)
            self.update_app_status(self.selected_app)

    def restart_app(self):
        if self.selected_app:
            self.manager.restart_process(self.selected_app, self.manager.apps[self.selected_app]["command"],
                                         self.manager.apps[self.selected_app]["cwd"])
            self.update_app_status(self.selected_app)

    def send_command(self):
        if self.selected_app:
            command = self.command_entry.get()
            if command:
                self.manager.send_command(self.selected_app, command)
                self.command_entry.delete(0, tk.END)

    def update_output(self):
        for app_name in self.manager.output_queues:
            if app_name not in self.output_logs:
                self.output_logs[app_name] = ""
            while not self.manager.output_queues[app_name].empty():
                line = self.manager.output_queues[app_name].get() + "\n"
                self.output_logs[app_name] += line
                if self.selected_app == app_name:
                    self.output_box.config(state=tk.NORMAL)
                    self.output_box.insert(tk.END, line)
                    self.output_box.config(state=tk.DISABLED)
                    self.output_box.yview(tk.END)  # Auto-scroll to the bottom
        self.root.after(500, self.update_output)  # Check every 500ms
