from threading import Thread
import serial
import tkinter as tk
from tkinter import ttk
from datetime import datetime

def __init__(self):
    super().__init__()
    self.title("Terminal")

class GUIClass(tk.Tk):
    self.serial_conn = None
    self.is_connected = False
    # Connection settings
    settings_frame = ttk.Frame(self)
    settings_frame.pack(padx=5, pady=5)

    ttk.Label(settings_frame, text="Port:").grid(row=0, column=0)
    self.port_entry = ttk.Entry(settings_frame)
    self.port_entry.grid(row=0, column=1)

    ttk.Label(settings_frame, text="Baud Rate:").grid(row=1, column=0)
    self.baudrate_entry = ttk.Entry(settings_frame)
    self.baudrate_entry.grid(row=1, column=1)

    self.connect_button = ttk.Button(settings_frame, text="Connect", command=self.connect)
    self.connect_button.grid(row=2, column=0, pady=5)
    self.disconnect_button = ttk.Button(settings_frame, text="Disconnect", command=self.disconnect, state="disabled")
    self.disconnect_button.grid(row2, column=1, pady=5)


    terminal_frame = tk.Frame(self)
    terminal_frame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    self.terminal = tk.Text(terminal_frame, wrap=tk.WORD, state="disabled")
    self.terminal.pack(fill=tk.BOTH, expand=True)

    input_frame = ttk.Frame(self)
    input_frame.pack(padx=5, pady=5, fill=tk.X, expand=False)

    self.input_entry = ttk.Entry(input_frame)
    self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    self.send_button = ttk.Button(input_frame, text="Send", command=self.send_data, state="disabled")
    self.send_button.pack(side=tk.RIGHT)

    def connect(self):
        port = self.port_entry.get()
        baudrate = int(self.baudrate_entry.get())

        try:
            self.serial_conn = serial.Serial(port, baudrate)
            self.is_connected = True
            self.connect_button.config(state="disabled")
            self.disconnect_button.config(state="normal")
            self.send_button.config(state="normal")

            Thread(target=self.read_data).start()
            self.write_to_terminal("Connected to: " + port + " at " + str(baudrate) + " baud rate.\n")
        except Exception as e:
            self.write_to_terminal("Error connecting: " + str(e) + "\n")

    def disconnect(self):
        if self.serial_conn and self.is_connected:
            self.is_connected = False
            self.serial_conn.close()
            self.connect_button.config(state="normal")
            self.disconnect_button.config(state="disabled")
            self.send_button.config(state="disabled")
            self.write_to_terminal("Disconnected from: " + self.port_entry.get() + "\n")

    def read_data(self):
        while self.is_connected:
            try:
                self.write_to_terminal(self.serial_conn.read_until())
            except Exception as e:
                self.disconnect()
                Thread(target=self.read_data).start()
                #if the port is closing then ignore it, to prevent possible Exceptions1221989348@
                if "could not be configured" in str(e) or "is closed" in str(e) or "disconnected" in str(e):
                    break

    def write_to_terminal(self):
        self.terminal.config(state="normal")
        self.terminal.insert(tk.END, text)
        self.terminal.see(tk.END)
        self.terminal.config(state="disabled")

    def send_data(self):
        input = self.input_entry.get()
        if self.serial_conn and self.is_connected:
            boole = True
            out = self.ser.values
            for byte in out:
                for code in byte:
                    if b'\x18' == code:
                        self.ser.write(b'echo1_recieved')
                        boole = False
                        return boole
                #this will return when it receives echo_code
                #...
                if not input:
                    return
                self.input_entry.delete(0, tk.END)
                self.write_to_terminal("> ") 

    def main():
        guiexample = GUIClass()
        guiexample.mainloop()

    if __name__ == '__main__':
        main()