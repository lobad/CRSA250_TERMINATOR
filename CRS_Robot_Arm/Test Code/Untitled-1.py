
import serial
import serial.tools.list_ports
import time
import psutil
import os
import sys
import threading
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
from tkinter import *
 
def is_already_running():
    current_pid = os.getpid()
    for pid in psutil.pids():
        if pid == current_pid:
            continue
        try:
            p = psutil.Process(pid)
            if len(p.cmdline()) > 1 and os.path.basename(sys.argv[0]) == os.path.basename(p.cmdline()[0]):
                return True
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass
    return False
 
if is_already_running():
    print("Another instance of the script is already running.")
    exit()
 
class Application(tk.Frame):
 
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("CRS A250 Terminal")
        self.selected_port = tk.StringVar(value="COM5")
        self.baudrate = tk.IntVar(value=9600)
        self.gripper_closed = False  # add a variable to keep track of the gripper status
        self.create_widgets()
       # self.autoconnect()
 
        # bind the WM_DELETE_WINDOW event to the toggle_serial method
        #self.master.protocol("WM_DELETE_WINDOW", self.toggle_serial)
 
    def create_widgets(self):
 
 
        # Create Sliders and their button
        self.speed_slider = Scale(self.master, from_=0, to=100, orient=HORIZONTAL)
        self.speed_slider.grid(row=2, column=2, padx=5, pady=5, sticky="nw")
        self.speed_label = tk.Label(self.master, text="Speed")
        self.speed_label.grid(row=2, column=3, padx=0, pady=0, sticky="w") # Place the label to the right of the slider    
 
        self.send_button = Button(self.master, text="Send", command=self.send_parameters)
        self.send_button.grid(row=2, column=3, padx=5, pady=5, sticky="nsew")
 
        # Axis Control Button
        self.axis_button = tk.Button(self.master, text="Axis Control", command=self.axis_control_window)
        self.axis_button.grid(row=1, column=2, padx=5, pady=0, sticky="nw")
 
        # Create button for gripper control
        self.gripper_button = tk.Button(self.master, text="Open Gripper", command=self.toggle_gripper)
        self.gripper_button.grid(row=1, column=3, padx=5, pady=0, sticky="nw")
 
        # Create menu bar
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)
 
        # Create file menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As...", command=self.save_file_as)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
 
        # Create terminal window
        self.terminal = tk.Text(self.master, width=40, height=15)
        self.terminal.grid(row=0, column=0, padx=5, pady=35)
 
        # Create text box
        self.text_box = tk.Text(self.master, width=40, height=15)
        self.text_box.grid(row=0, column=1, padx=5, pady=35, sticky="n")
        
        # Create MDI box
        self.mdi_box = tk.Text(self.master, width=40, height=1)
        self.mdi_box.grid(row=1, column=0, padx=5, pady=0, sticky="w")
        self.mdi_box.bind('<Return>', self.send_mdi_to_terminal)
 
        # Create send button for the text box
        self.send_text_button = tk.Button(self.master, text="Send", command=self.send_text_to_serial)
        self.send_text_button.grid(row=1, column=1, padx=5, pady=5, sticky="nw")
 
        # Create serial port selection menu
        available_ports = self.get_available_ports()
        self.selected_port.set(available_ports[0] if available_ports else '')
        self.port_menu = ttk.Combobox(self.master, textvariable=self.selected_port, values=available_ports)
        self.port_menu.config(width=10)
        self.port_menu.grid(row=4, column=0, padx=5, pady=5, sticky="w")
 
        # Create Serial Connection Button
        self.serial_button = tk.Button(self.master, text="Connect", command=self.toggle_serial)
        self.serial_button.grid(row=4, column=1, padx=5, pady=5, sticky="w")
 
        # Create buttons
        self.home_button = tk.Button(self.master, text="HOME")
        self.home_button.grid(row=0, column=1, padx=5, pady=0, sticky="nw")
 
        self.manual_button = tk.Button(self.master, text="MANUAL")
        self.manual_button.grid(row=0, column=2, padx=5, pady=0, sticky="nw")
 
        self.auto_button = tk.Button(self.master, text="AUTO")
        self.auto_button.grid(row=0, column=3, padx=5, pady=0, sticky="nw")
 
        # Create baud rate selection button
        self.baud_button = tk.Button(self.master, text="Serial: A", command=self.toggle_baudrate)
        self.baud_button.grid(row=3, column=0, padx=5, pady=5, sticky="w")
 
        # Initialize serial port
        self.serial = None
        if self.serial:
            self.serial.close()
            self.serial = None
            self.serial_button.config(text="Connect")
            self.terminal.insert(tk.END, "Disconnected from serial port\n")
 
    def autoconnect(self):
        while True:
            if self.serial is None or not self.serial.is_open:
                port = self.get_available_ports()[0]
                baudrate = self.baudrate.get()
                try:
                    self.serial = serial.Serial(port, baudrate)
                    self.serial.timeout = 0.1
                    self.serial.flushInput()
                    self.serial.flushOutput()
                    self.serial_button.configure(text="Disconnect")
                    return
                except (IndexError, serial.serialutil.SerialException):
                    print("error")
                    pass
            print("Waiting for port")
            time.sleep(1)
 
    def connect_serial(self):
        port = self.selected_port.get()
        if port:
            try:
                self.serial = serial.Serial(port, baudrate=self.baudrate.get())
                self.serial_button.config(text="Disconnect", command=self.toggle_serial)
                self.write_to_terminal(f"Connected to {port} at {self.baudrate.get()} baud")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                return
 
            # Wait for data to be available to read
            time.sleep(2)
            if self.serial.in_waiting > 0:
                self.write_to_terminal(self.serial.read(self.serial.in_waiting).decode())
 
    def serial_thread(self):
        while self.serial_connected:
            if self.serial_port.in_waiting > 0:
                data = self.serial_port.readline().decode().strip()
                self.terminal.insert(tk.END, data + '\n')
                self.terminal.see(tk.END)
            if self.serial_queue.qsize() > 0:
                command = self.serial_queue.get()
                self.serial_port.write(command.encode())
 
 
    def write_to_serial(self, data):
        if self.serial:
            self.serial.write(data.encode())
 
    def disconnect_serial(self):
        if self.serial:
            self.serial.close()
            self.serial = None
            self.serial_button.config(text="Connect")
            self.terminal.insert(tk.END, "Disconnected from serial port\n")
 
    def toggle_serial(self):
        if self.serial is None:
            try:
                self.serial = serial.Serial(self.selected_port.get(), self.baudrate.get())
                self.serial_button.configure(text="Disconnect")
                self.serial_button.configure(bg="green")
            except serial.serialutil.SerialException:
                messagebox.showerror("Connection Error", "Could not connect to " + self.selected_port.get())
                self.serial = None
        else:
            self.serial.close()
            self.serial = None
            self.serial_button.configure(text="Connect")
            self.serial_button.configure(bg="red")

 
    def send_mdi_to_terminal(self, event=None):
        mdi_text = self.mdi_box.get('1.0', 'end').strip()
        if mdi_text:
            self.terminal.insert(END, f">>> {mdi_text} \n", "MDI")
        self.mdi_box.delete('1.0', 'end')
        self.terminal.tag_config("MDI", foreground="red")
 
    def write_to_terminal(self, message):
        self.terminal.insert(tk.END, message + "\n", "MDI")
        self.terminal.see(tk.END)
        self.terminal.tag_config("MDI", foreground="red")
        text = self.text_box.get("1.0", END).strip()
             
    def send_parameters(self):
        speed = self.speed_slider.get()
        command = f"M2120 V{speed}\r\n"
        self.serial_queue.put(command)
            
    def send_text_to_serial(self):
        text = self.text_box.get("1.0", END).strip()
        if text:
            self.serial.write(text.encode())
            self.terminal.insert(END, f">>> {text}\n", "sent")
            self.terminal.insert(END, self.serial.readline().decode(), "received")
            self.text_box.delete("1.0", END)
            self.text_box.focus_set()
    
            # Set color tags for sent and received text
            self.terminal.tag_config("sent", foreground="blue")
            self.terminal.tag_config("received", foreground="green")

    def toggle_gripper(self):
        # Toggle the gripper status and change the label and button text accordingly
        if self.gripper_closed:
            self.write_to_serial('G_OPEN\n')
            self.gripper_closed = False
            self.gripper_button.config(text="Open Gripper")
        else:
            self.write_to_serial('G_CLOSE\n')
            self.gripper_closed = True
            self.gripper_button.config(text="Close Gripper")
 
    def create_axis_control_window(self):
        axis_window = Toplevel(self.master)
        axis_window.title("Axis Control")
 
    def axis_control_window(self):
        window = Toplevel(self.master)
        window.title("Axis Control")
        axis_labels = ["Axis 1", "Axis 2", "Axis 3", "Axis 4", "Axis 5", "Axis 6"]
        for i, label in enumerate(axis_labels):
            axis_label = Label(window, text=label)
            axis_label.grid(row=i, column=0, padx=5, pady=5)
            plus_button = Button(window, text="+", width=5, command=lambda x=i: self.send_text(f"{axis_labels[x]} +"))
            plus_button.grid(row=i, column=1, padx=5, pady=5)
            minus_button = Button(window, text="-", width=5, command=lambda x=i: self.send_text(f"{axis_labels[x]} -"))
            minus_button.grid(row=i, column=2, padx=5, pady=5)
        interpolate_label = Label(window, text="Interpolated Motion")
        interpolate_label.grid(row=0, column=3, padx=5, pady=5, columnspan=2)
        move1_button = Button(window, text="Move 1", width=10, command=lambda: self.send_text("Move 1"))
        move1_button.grid(row=1, column=3, padx=5, pady=5)
        move2_button = Button(window, text="Move 2", width=10, command=lambda: self.send_text("Move 2"))
        move2_button.grid(row=2, column=3, padx=5, pady=5)
        move3_button = Button(window, text="Move 3", width=10, command=lambda: self.send_text("Move 3"))
        move3_button.grid(row=3, column=3, padx=5, pady=5)
 
    def save_file(self):
        if self.filename:
            with open(self.filename, 'w') as f:
                f.write(self.text_box.get("1.0", tk.END))
        else:
            self.save_file_as()
 
    def save_file_as(self):
        self.filename = tk.filedialog.asksaveasfilename(defaultextension=".txt")
        if self.filename:
            self.save_file()            
 
    def open_file(self):
        self.filename = tk.filedialog.askopenfilename(defaultextension=".txt")
        if self.filename:
            with open(self.filename, 'r') as f:
                self.text_box.delete("1.0", tk.END)
                self.text_box.insert(tk.END, f.read())
 
    def toggle_baudrate(self):
        baudrate_options = [(9600, 'Serial: A'), (2400, 'Serial: B')]
        current_baudrate = self.baudrate.get()
        for baudrate, label in baudrate_options:
            if current_baudrate == baudrate:
                self.baudrate.set(baudrate_options[(baudrate_options.index((baudrate, label)) + 1) % 2][0])
                self.baud_button.config(text=baudrate_options[(baudrate_options.index((baudrate, label)) + 1) % 2][1])
                break
 
    def get_available_ports(self):
        return [port.device for port in serial.tools.list_ports.comports()]
 
    def connect_serial(self):
        port = self.selected_port.get()
        if port:
            try:
                self.serial = serial.Serial(port, baudrate=self.baudrate.get())
                self.serial_button.config(text="Disconnect")
                self.read_serial()
            except serial.SerialException:
                messagebox.showerror("Error", "Could not connect to serial port {}".format(port))
        else:
            messagebox.showerror("Error", "No serial port selected")
 
    def read_serial(self):
        if self.serial and self.serial.is_open:
            try:
                data = self.serial.readline().decode('utf-8')
                self.terminal.insert(tk.END, data)
            except UnicodeDecodeError:
                messagebox.showerror("Error", "Could not decode serial data")
        self.master.after(100, self.read_serial)
 
    def disconnect_serial(self):
        if self.serial:
            self.serial.close()
            self.serial = None
            self.terminal.insert(tk.END, "Disconnected\n")
 
    def send_text(self):
        if self.serial:
            text = self.text_box.get("1.0", tk.END).encode()
            self.serial.write(text)
        self.terminal.insert(tk.END, f"{text}\n")
        self.terminal.see(tk.END)    
 
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()