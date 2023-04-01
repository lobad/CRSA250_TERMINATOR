import tkinter as tk
import serial

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Serial port configuration widgets
        self.port_label = tk.Label(self, text="Serial Port:")
        self.port_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

        self.port_entry = tk.Entry(self, width=10)
        self.port_entry.grid(row=0, column=1, padx=5, pady=5)

        self.baud_label = tk.Label(self, text="Baud Rate:")
        self.baud_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)

        self.baud_entry = tk.Entry(self, width=10)
        self.baud_entry.grid(row=0, column=3, padx=5, pady=5)

        self.connect_button = tk.Button(self, text="Connect", command=self.connect_serial)
        self.connect_button.grid(row=0, column=4, padx=5, pady=5)

        # Terminal window
        self.terminal_text = tk.Text(self, width=80, height=24)
        self.terminal_text.grid(row=1, column=0, columnspan=5, padx=5, pady=5)

        # Home, Manual, and Auto buttons
        self.home_button = tk.Button(self, text="HOME", command=self.send_home)
        self.home_button.grid(row=2, column=0, padx=5, pady=5)

        self.manual_button = tk.Button(self, text="MANUAL", command=self.send_manual)
        self.manual_button.grid(row=2, column=1, padx=5, pady=5)

        self.auto_button = tk.Button(self, text="AUTO", command=self.send_auto)
        self.auto_button.grid(row=2, column=2, padx=5, pady=5)
        
        # Create text box
        self.text_box = tk.Text(self, width=40, height=24)
        self.text_box.grid(row=1, column=5, padx=5, pady=5)

        # Create buttons
        self.send_button = tk.Button(self, text="Send", command=self.send_text)
        self.send_button.grid(row=2, column=5, padx=5, pady=5)

        self.save_button = tk.Button(self, text="Save", command=self.save_text)
        self.save_button.grid(row=3, column=5, padx=5, pady=5)

        self.load_button = tk.Button(self, text="Load", command=self.load_text)
        self.load_button.grid(row=4, column=5, padx=5, pady=5)
        
        # Functions for the buttons
    def send_text(self):
        text = self.text_box.get("1.0", tk.END).encode()
        self.serial.write(text)

    def save_text(self):
        filename = tk.filedialog.asksaveasfilename(defaultextension=".txt")
        if filename:
            with open(filename, "w") as f:
                f.write(self.text_box.get("1.0", tk.END))

    def load_text(self):
        filename = tk.filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, "r") as f:
                self.text_box.delete("1.0", tk.END)
                self.text_box.insert(tk.END, f.read())
        
    def connect_serial(self):
        # Connect to the serial port
        port = self.port_entry.get()
        baud = int(self.baud_entry.get())
        try:
            self.serial = serial.Serial(port, baud)
            self.terminal_text.insert(tk.END, f"Connected to {port} at {baud} baud\n")
            self.master.after(100, self.read_serial)
        except serial.SerialException:
            self.terminal_text.insert(tk.END, f"Error: Could not connect to {port}\n")

    def read_serial(self):
        # Read data from the serial port and display it in the terminal window
        if self.serial.in_waiting > 0:
            data = self.serial.read(self.serial.in_waiting)
            self.terminal_text.insert(tk.END, data.decode())
        self.master.after(100, self.read_serial)

    def send_home(self):
        # Send the HOME command to the serial port
        self.serial.write(b"HOME\n")

    def send_manual(self):
        # Send the MANUAL command to the serial port
        self.serial.write(b"MANUAL\n")

    def send_auto(self):
        # Send the AUTO command to the serial port
        self.serial.write(b"AUTO\n")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
