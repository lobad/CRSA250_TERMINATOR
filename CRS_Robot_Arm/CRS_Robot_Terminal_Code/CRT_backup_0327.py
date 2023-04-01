import serial
import serial.tools.list_ports
import time
import psutil
import os
import sys
import threading
import queue
import error_codes #Library Containing CRS A250 Error Codes
import command_list #Library Containing CRS A250 Command List
import cv2
import PIL
import json
import numpy as np
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk
from tkinter import *
from tkinter import Menu
from tkinter.simpledialog import Dialog
from PIL import ImageTk, Image
 
 
# Check if another instance is already running 
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
 
# Create a class for the application
class Application(tk.Frame):
    # Initialize the application
    def __init__(self, parent, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("CRS A250 Terminal")
        self.selected_port = tk.StringVar(value="COM5")
        self.baudrate = tk.IntVar(value=9600)
        self.gripper_closed = False  # add a variable to keep track of the gripper status
        self.serial_connected = False       
        self.serial = None
        self.error_codes_window = None
        self.filename = None
        self.after_id = None
        self.cap = None
        self.thread = None
        self.camera_port = 0
        self.camthread = None
        self.webcam_running = False
        self.parent = parent
        self.image_path_var = tk.StringVar(value="")
        self.video_path_var = tk.StringVar(value="")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.create_widgets()
        
# Create the User Interface    
    def create_widgets(self):
    # Create GUI

        # Create the webcam frame
        self.webcam_frame = tk.Frame(self.parent, borderwidth=2, width=200, height=100)
        self.webcam_frame.grid(row=1, column=0, padx=5, pady=0, sticky="se")
        # Create the frame for live view
        self.live_view_frame = tk.Frame(self.webcam_frame, borderwidth=2, bg='black')
        self.live_view_frame.grid(row=0, column=0,)
        live_view_width = 200
        live_view_height = 100
        self.live_view = tk.Label(self.live_view_frame, text="'Webcam' Button to Connect \n\n Config Cettings in Connection Menu", font=("Helvetica", 8), pady=20, fg="white", bg="black") #width=live_view_width, height=live_view_height,
        self.live_view.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.live_view_frame.grid_propagate(False)
        self.live_view_frame.config(width=live_view_width, height=live_view_height)
        self.live_view.bind("<Double-Button-1>", self.cam_pop_up)
        # Create the frame for camera buttons
        self.cam_buttons_frame = tk.Frame(self.webcam_frame, borderwidth=0)
        self.cam_buttons_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nwse")
        self.webcam_button = tk.Button(self.cam_buttons_frame, text="Webcam", command=self.show_webcam, bg='red')
        self.webcam_button.grid(row=0, column=0, padx=5, pady=5)
        self.capture_button = tk.Button(self.cam_buttons_frame, text="Capture", command=self.capture_image, bg='gray')
        self.capture_button.grid(row=0, column=1, padx=5, pady=5)
        self.record_button = tk.Button(self.cam_buttons_frame, text="Record", command=self.record_video, bg='gray')
        self.record_button.grid(row=0, column=2, padx=5, pady=5)
        self.after_id = None
        self.cap = None
        
        # Create terminal frame and window
        terminal_frame = tk.Frame(self.master)
        terminal_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.terminal = tk.Text(terminal_frame, width=40, height=15, font=('Courier', 10))
        self.terminal.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.terminal.configure(background="black", foreground="white")
        self.terminal.config(yscrollcommand=self.send_command_serial)
        self.scrollbar = tk.Scrollbar(terminal_frame, command=self.terminal.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.terminal.config(yscrollcommand=self.scrollbar.set)
        self.mdi_box = tk.Text(terminal_frame, width=40, height=0.15)
        self.mdi_box.grid(row=1, column=0, padx=5, pady=5, sticky="sw")
        self.mdi_box.bind('<Return>', self.send_command)
        #create a frame for the serial connection
        serial_frame = tk.Frame(terminal_frame, relief="ridge", borderwidth=1)
        serial_frame.grid(row=0, column=3, padx=5, pady=5, sticky="nw")
        available_serports = self.get_available_ports()
        self.selected_port.set(available_serports[0] if available_serports else '')
        self.port_menu = ttk.Combobox(serial_frame, textvariable=self.selected_port, values=available_serports)
        self.port_menu.config(width=10)
        self.port_menu.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.serial_button = tk.Button(serial_frame, text="Connect", command=self.toggle_connection, bg='red')
        self.serial_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.baud_label = tk.Label(serial_frame, text="9600")
        self.baud_label.grid(row=1, column=1, padx=0, pady=5, sticky="w")
        self.baud_button = tk.Button(serial_frame, text="Serial: A", command=self.toggle_baudrate)
        self.baud_button.grid(row=1, column=0, padx=0, pady=5, sticky="w")
        # Create the frame for the programming window
        programming_window_frame = tk.Frame(terminal_frame)
        programming_window_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        self.text_box = tk.Text(programming_window_frame, width=40, height=15)
        self.text_box.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.load_text()
        # Create the frame for the programming buttons
        programming_button_frame = tk.Frame(terminal_frame)
        programming_button_frame.grid(row=1, column=2, padx=5, pady=0, sticky="nsew")
        self.send_text_button = tk.Button(programming_button_frame, text="Send Program", command=self.send_program)
        self.send_text_button.grid(row=0, column=4, padx=25, pady=5, sticky="se")
        self.command_list_button = tk.Button(programming_button_frame, text="Command List", command=self.command_list_list)
        self.command_list_button.grid(row=0, column=0, padx=5, pady=5, sticky="sw")
        self.save_button = tk.Button(programming_button_frame, text="Save", command=self.save_file)
        self.save_button.grid(row=0, column=3, padx=5, pady=5)
        self.load_button = tk.Button(programming_button_frame, text="Load", command=self.open_file)
        self.load_button.grid(row=0, column=2, padx=5, pady=5)
        # Set Spacing of frames
        terminal_frame.grid_rowconfigure(0, weight=5)
        terminal_frame.grid_rowconfigure(1, weight=1)
        terminal_frame.grid_rowconfigure(2, weight=1)
        terminal_frame.grid_columnconfigure(0, weight=5)
        terminal_frame.grid_columnconfigure(1, weight=0)
        terminal_frame.grid_columnconfigure(2, weight=5)
        programming_window_frame.grid_rowconfigure(0, weight=1)
        programming_window_frame.grid_rowconfigure(1, weight=0)
        programming_window_frame.grid_columnconfigure(0, weight=1)
        serial_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nw")
        self.mdi_box.grid(row=1, column=0, padx=5, pady=0, sticky="nsew")
        
        # Create Function Buttons
        funk_frame = tk.Frame(self.master, borderwidth=1, relief=tk.RIDGE)
        funk_frame.grid(row=1, column=1, padx=0, pady=0, sticky="ne")
        manual_frame = tk.Frame(funk_frame, relief=tk.SOLID)
        manual_frame.grid(row=1, column=0)
        self.manual_button_state = False  # initial state of the manual button
        self.manual_button_text = tk.StringVar(value="MANUAL")
        # Create toggle button for manual mode
        def toggle_manual_mode():
            self.manual_button_state = not self.manual_button_state
            data = self.display_serial_input()
            if data and ("j>" in data or "c>" in data):
                    self.manual_button_text.set("NOMANUAL")
                    command_string = f"NOMANUAL"
                    print("Current manual mode:", self.manual_mode.get())
            else:
                self.manual_button_text.set("MANUAL")
                command_string = f"MANUAL {self.manual_mode.get()}"
                print("Current manual mode:", self.manual_mode.get())
            self.send_command_serial(command_string)
        self.manual_mode = tk.StringVar(value="JOINT")
        def set_manual_mode_to_joint():
            self.manual_mode.set("JOINT")
        self.manual_mode_toggle_joint = tk.Radiobutton(manual_frame, text="J", variable=self.manual_mode, value="JOINT", command=set_manual_mode_to_joint)
        self.manual_mode_toggle_joint.grid(row=0, column=1)
        def set_manual_mode_to_cylindrical():
            self.manual_mode.set("CYLINDRICAL") 
        self.manual_mode_toggle_cylindrical = tk.Radiobutton(manual_frame, text="C", variable=self.manual_mode, value="CYLINDRICAL", command=set_manual_mode_to_cylindrical)
        self.manual_mode_toggle_cylindrical.grid(row=0, column=2)
        self.manual_button = tk.Button(manual_frame, textvariable=self.manual_button_text, command=toggle_manual_mode)
        self.manual_button.grid(row=0, column=0)
        # Create Speed and Axis Control Frames
        speed_axis_frame = tk.Frame(funk_frame)
        speed_axis_frame.grid(row=2, column=0)
        speed_frame = tk.Frame(speed_axis_frame, borderwidth=1)
        speed_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nw")
        self.speed_slider = Scale(speed_frame, from_=0, to=100, orient=HORIZONTAL, relief=tk.SOLID)
        self.speed_slider.grid(row=0, column=0, padx=0, pady=0, sticky="nw")
        self.speed_label = tk.Button(speed_frame, text="Speed", command=self.send_command)
        self.speed_label.grid(row=0, column=1, padx=0, pady=10, sticky="nw")
        axis_frame = tk.Frame(speed_axis_frame, borderwidth=1, relief=tk.RIDGE)
        axis_frame.grid(row=3, column=0, padx=0, pady=0, sticky="nw")
        axis_buttons_frame = tk.Frame(axis_frame)
        axis_buttons_frame.grid(row=0, column=0)
        self.axis_button = tk.Button(axis_buttons_frame, text="Axis Control", command=self.axis_control_window)
        self.axis_button.grid(row=0, column=1, padx=0, pady=0, sticky="nw")
        self.gripper_button = tk.Button(axis_buttons_frame, text="Open Gripper", command=self.toggle_gripper)
        self.gripper_button.grid(row=0, column=0, padx=0, pady=0, sticky="nw")

    # Create Menu Bar
        # Create menu bar
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)
    # File explorer menu
        # Create file menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As...", command=self.save_file_as)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
    # Add "Help" menu with "Error Codes" Search
        helpmenu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="Error Codes", command=self.error_window)
        helpmenu.add_command(label="Command List", command=self.command_list_list)
        manual_menu = tk.Menu(helpmenu, tearoff=0)
        helpmenu.add_cascade(label="Manuals", menu=manual_menu)
        manual_menu.add_command(label="Tutorial", command=lambda: self.open_manual(1))
        manual_menu.add_command(label="Programming", command=lambda: self.open_manual(2))
        manual_menu.add_command(label="Operation", command=lambda: self.open_manual(3))
    # Create Connection Drop Down menu
        self.connection_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Connection", menu=self.connection_menu)
        self.connection_menu.add_command(label="COM Settings", command=self.open_com_settings)
        self.connection_menu.add_command(label="Webcam", command=self.cam_settings_window)

    # Initialize serial port
        self.serial = None
        if self.serial:
            self.serial.close()
            self.serial = None
            self.serial_button.config(text="Connect")
            self.terminal.insert(tk.END, "Disconnected from serial port\r\n")
            
# Serial Connection
    # Search for available serial ports and report to terminal
    def get_available_ports(self):
        print("Getting Available Ports")
        serports = serial.tools.list_ports.comports()
        available_serports = []
        for serport in serports:
            if "in use" not in serport.description.lower():
                available_serports.append(serport.device)
                print("Port In Use")
        if len(available_serports) == 0:
            print("No Available Ports")
            return None
        elif len(available_serports) == 1:
            print("1 Available Port")
            return [serport.device for serport in serial.tools.list_ports.comports()]
        else:
            print("Multiple Available Ports")
            return [serport.device for serport in serial.tools.list_ports.comports()]
    # Toggle Baudrate between 9600 and 2400
    def toggle_baudrate(self):
        baudrate_options = [(9600, 'Serial: A'), (2400, 'Serial: B')]
        current_baudrate = self.baudrate.get()
        for baudrate, label in baudrate_options:
            if current_baudrate == baudrate:
                self.baudrate.set(baudrate_options[(baudrate_options.index((baudrate, label)) + 1) % 2][0])
                self.baud_label.config(text= f"{baudrate_options[(baudrate_options.index((baudrate, label)) + 1) % 2][0]}")
                self.baud_button.config(text=baudrate_options[(baudrate_options.index((baudrate, label)) + 1) % 2][1])
                break
    # Disconnect Serial Connection on Window Close
    def on_closing(self):
        if self.serial is not None:
            self.serial.close()
            print("Closing Serial Connection")
        self.master.destroy()                       
    # Toggle Serial Connection                                           
    def toggle_connection(self):
        if not self.serial_connected:
            serport = self.selected_port.get()
            baudrate = self.baudrate.get()
            print(baudrate)
            print("Attempting to connect to serial port")
            try:
                    self.serial = serial.Serial(serport=serport, baudrate=baudrate, timeout=0, xonxoff=True, rtscts=True)
                    self.serial.flush();
                    self.serial_button.configure(text="Disconnect", bg="green")
                    print("Connected to serial port.")
                    time.sleep(1.5)
                    self.send_command_serial("NOHELP")
                    self.master.after(1000,self.display_serial_input)
            except serial.serialutil.SerialException:
                messagebox.showerror("Connection Error", "Could not connect to " + self.selected_port.get())
                print("Connection to serial port failed.")     
        else:
            self.serial.close()
            if os.name == 'nt':
                self.serial.hEvent = None
            print("Closing Serial Connection")
            self.serial_connected = False
            self.serial = None
            self.serial_button.configure(text="Connect", bg="red")   
    # Drip Feed Serial Data from Text Box
    def send_program(self, select_all=False):
        if select_all:
            # Select all the code in the text box
            self.text_box.tag_add("sel", "1.0", "end")
        else:
            # Check if there is a selection already
            try:
                start = self.text_box.index("sel.first")
                end = self.text_box.index("sel.last")
            except TclError:
                # No selection, do something else (e.g., select all)
                self.text_box.tag_add("sel", "1.0", "end")
                start = self.text_box.index("sel.first")
                end = self.text_box.index("sel.last")
        # Check if "sel" tag is present
        if self.text_box.tag_ranges("sel"):
            # Get the start and end index of the current selection
            start = self.text_box.index("sel.first")
            end = self.text_box.index("sel.last")
            # Make sure the cursor is visible on the selected line
            self.text_box.see(start)
            # Do something with the selected text (e.g., send it to a server)
            selected_text = self.text_box.get(start, end)
            lines = selected_text.strip().split('\r\n')
            self.text_box.tag_configure("current_line", background="blue")
            self.text_box.tag_configure("sent_line", background="gray")
            for i, line in enumerate(lines):
                # Highlight the current line in blue
                current_line_start = f"{int(start.split('.')[0]) + i}.0"
                current_line_end = f"{int(start.split('.')[0]) + i}.end"
                self.text_box.tag_add("current_line", current_line_start, current_line_end)
                self.text_box.see(current_line_start)
                self.text_box.update()
                # Send the line to the serial port
                self.send_command_serial(line)
                # Highlight the sent line in gray
                self.text_box.tag_remove("current_line", current_line_start, current_line_end)
                sent_line_start = f"{int(start.split('.')[0]) + i + 1}.0"
                sent_line_end = f"{int(start.split('.')[0]) + i + 1}.end"
                self.text_box.tag_add("sent_line", sent_line_start, sent_line_end)
                self.text_box.see(sent_line_start)
                self.text_box.update()
        # Remove the selection
        self.text_box.tag_remove("sel", "1.0", "end")
        # Set the cursor to the end of the text box
        self.text_box.mark_set("insert", "end")
        self.text_box.tag_remove("current_line", "1.0", "end")
        self.text_box.tag_remove("sent_line", "1.0", "end")
        self.text_box.update()
        self.text_box.focus_set()
    # Function to handle commented code
    def handle_commented_code(self, text):
        # Define Commands sent to serial
        commands = []
        # Parse text_box contents
        for line in text.split("\n"):
            # Ignore comments enclosed in parentheses
            if "(" in line and ")" in line:
                comment_start = line.find("(")
                comment_end = line.find(")")
                comment_text = line[comment_start+1:comment_end]
                # Add tag to highlight comments in purple
                self.text_box.tag_add("comment", f"1.0+{comment_start}c", f"1.0+{comment_end}c")
                line = line[:comment_start] + f'\033[2m\033[35m{comment_text}\033[0m' + line[comment_end+1:]
                # Add commented line to the terminal window
                self.text_box.insert(END, f"\n{line}")
            else:
                # Send non-commented line to serial port
                line = line.strip()
                if line:
                    commands.append(line)
                    # Add non-commented line to the terminal window
                    self.text_box.insert(END, f"\n{line}")
        return commands
    # Write to Serial Port
    def send_command(self, event):
        # Define Variables
        text = self.text_box.get("1.0", "end").strip().upper()
        mdi_text = self.mdi_box.get("1.0", "end").strip().upper()
        speed_slider = self.speed_slider.get()
        # Define Commands sent to serial
        commands = []
        # Handle commented code separately
        commands += self.handle_commented_code(text)
        if speed_slider:
            self.send_command_serial(str(speed_slider).strip())
        if commands:
            self.send_command_serial(";".join(commands).strip())
            self.text_box.focus_set()
        if mdi_text:
            self.send_command_serial(mdi_text.strip())
            self.mdi_box.delete("1.0", END)
            self.mdi_box.focus_set()
        # Define tag to highlight comments in purple
        self.text_box.tag_configure("comment", foreground="purple")
        if speed_slider:
            self.send_command_serial(str(speed_slider).strip())
        if commands:
            self.send_command_serial(";".join(commands).strip())
            self.text_box.focus_set()
        if mdi_text:
            self.send_command_serial(mdi_text.strip())
            self.mdi_box.delete("1.0", END)
            self.mdi_box.focus_set()
            # Define tag to highlight comments in purple
            self.text_box.tag_configure("comment", foreground="purple")
    # Send Stuff to serial       
    def send_command_serial(self,command):
        command = command.strip().upper()+'\r\n'
        #print(command)
        self.serial.write(command.encode('ascii'))
        self.terminal.yview_moveto(1.0)
    # Display What is sent to serial from the controller
    def display_serial_input(self):
        data = self.serial.read(self.baudrate.get())
        if data:
            data = data.decode('ascii')
            self.terminal.tag_config(data, foreground="green")
            self.terminal.insert(tk.END, f"{data} \r\n", "data")
            print(data)
            self.robot_error(data)  # call robot_error function with received data
        self.master.after(104, self.display_serial_input)
        return data  # add this line to return the received data
    
# Toggle Functions
    # Gripper Button and Command
    def toggle_gripper(self):
        # Toggle the gripper status and change the label and button text accordingly
        if self.gripper_closed:
            self.send_command_serial("OPEN GRIPPER")
            self.gripper_closed = False
            self.gripper_button.config(text="Open Gripper")
        else:
            self.send_command_serial("CLOSE GRIPPER")
            self.gripper_closed = True
            self.gripper_button.config(text="Close Gripper")
            
# Create Axis Control Pop Up window
    def axis_control_window(self):
        window = Toplevel(self.master)
        window.title("Axis Control")
        axis_labels = ["Axis 1", "Axis 2", "Axis 3", "Axis 4", "Axis 5", "Axis 6"]
        for i, label in enumerate(axis_labels):
            axis_label = Label(window, text=label)
            axis_label.grid(row=i, column=0, padx=5, pady=5)
            plus_button = Button(window, text="+", width=5, command=lambda x=i: self.send_command(f"{axis_labels[x]} +"))
            plus_button.grid(row=i, column=1, padx=5, pady=5)
            minus_button = Button(window, text="-", width=5, command=lambda x=i: self.send_command(f"{axis_labels[x]} -"))
            minus_button.grid(row=i, column=2, padx=5, pady=5)
        interpolate_label = Label(window, text="Interpolated Motion")
        interpolate_label.grid(row=0, column=3, padx=5, pady=5, columnspan=2)
        move1_button = Button(window, text="Move 1", width=10, command=lambda: self.send_command("Move 1"))
        move1_button.grid(row=1, column=3, padx=5, pady=5)
        move2_button = Button(window, text="Move 2", width=10, command=lambda: self.send_command("Move 2"))
        move2_button.grid(row=2, column=3, padx=5, pady=5)
        move3_button = Button(window, text="Move 3", width=10, command=lambda: self.send_command("Move 3"))
        move3_button.grid(row=3, column=3, padx=5, pady=5)
        
    def robot_error(self, data):
        # Get first 3 characters of data
        first_3_chars = data[:3].strip()
        # Check if first 3 characters are digits
        if first_3_chars.isdigit():
            error_code = first_3_chars
            print("Found error code")
            print(error_code)
            # Check if error code exists in error_code database
            if error_code in error_codes.error_codes:
                print("error code matched in database")
                # Check if error window is already open
                if hasattr(self, 'error_codes_window') and self.error_codes_window.winfo_exists():
                    # If error window is open, update the search box and perform search
                    search_box = self.error_codes_window.children['!frame'].children['!entry']
                    search_box.focus_set()
                    search_box.delete(0, tk.END)
                    search_box.insert(0, error_code)
                    search_box.insert(tk.END, error_code)
                    print("Updating Error Window")
                    self.display_serial_input()
                else:
                    # If error window is closed, open it and perform search
                    print("Opening Error Window")
                    self.error_window()
                    search_box = self.error_codes_window.children['!frame'].children['!entry']
                    search_box.focus_set()
                    search_box.delete(0, tk.END)
                    search_box.insert(0, error_code)
                    search_box.insert(tk.END, error_code)
                    #self.error_codes_window = None  # Set error codes window attribute to None when closed
                    self.error_window()
                    self.display_serial_input()
            else:
                print("error code not found in database")
                self.display_serial_input()
                return
        else:
            self.display_serial_input()
            return
# File Menu Bar Functions                                       
    # Function to display error code pop-up window from error_codes.py
    def error_window(self):
        def search_error_code():
            error_code = search_box.get()
            if error_code in error_codes.error_codes:
                description_box.delete(1.0, END)
                description_box.insert(END, error_codes.error_codes[error_code])
            else:
                description_box.delete(1.0, END)
                description_box.insert(END, "Error code not found")
            show_error_description()
        def search_box_key_pressed(event):
            search_error_code()
        if not self.error_codes_window:
            # Create pop-up window
            error_codes_window = Toplevel()
            error_codes_window.title("Search Error Codes")
            error_codes_window.geometry("350x170")
            # Create frame for search box and button
            search_frame = Frame(error_codes_window)
            search_frame.grid(row=0, column=0, sticky=W, padx=5, pady=0)
            # Create search box and button
            search_label = Label(search_frame, text="Error Code:")
            search_label.grid(row=0, column=0, sticky=W)
            search_box = Entry(search_frame, width=30)
            search_box.grid(row=0, column=1)
            search_box.bind("<Return>", search_box_key_pressed)
            search_button = Button(search_frame, text="Search", command=search_error_code)
            search_button.grid(row=0, column=2)
            # Create description box
            description_label = Label(error_codes_window, text="Description:")
            description_label.grid(row=1, column=0, sticky=SW, padx=5, pady=5)
            description_box = Text(error_codes_window, height=6, width=42, wrap=WORD)
            description_box.grid(row=2, column=0, sticky=SW, padx=5, pady=5)
            # Set self.error_codes_window to the created Toplevel widget
            self.error_codes_window = error_codes_window
        else:
            # Bring existing window to the front
            self.error_codes_window.lift()
            def show_error_description():
                code = search_box.get()
                description = error_codes.error_codes.get(code)
                if description is None:
                    description_box.delete(1.0, END)
                    description_box.insert(END, "Error code not found")
                else:
                    description_box.delete(1.0, END)
                    description_box.insert(END, description)                         
    # Open manual pdfs from J:\Documents\CRS Robot Arm\Manuals
    def open_manual(self, manual_num):
        manual_names = {
            1: "CRSA250_Tutorial.pdf",
            2: "CRSA250_Programming_Manual.pdf",
            3: "CRSA250_Operators_Manual.pdf"
        }
        filename = manual_names.get(manual_num)
        if filename:
            os.startfile("J:\\Documents\\CRS Robot Arm Terminal Code\\CRS Robot Arm\\Manuals\\" + filename)
    # Save what is in the text box for next load        
    def load_text(self):
        try:
            with open("saved_text.txt", "r") as f:
                self.text_box.delete("1.0", tk.END)
                self.text_box.insert(tk.END, f.read())
        except FileNotFoundError:
            pass
    def save_text(self):
        with open("saved_text.txt", "w") as f:
            f.write(self.text_box.get("1.0", tk.END))
        self.master.destroy()      
 # File Save Menu
    def open_file(self):
        filename = filedialog.askopenfilename(defaultextension=".txt")
        if filename:
            self.filename = filename
            with open(self.filename, 'r') as f:
                self.text_box.delete("1.0", tk.END)
                self.text_box.insert(tk.END, f.read())        
    def save_file(self):
        if self.filename:
            with open(self.filename, 'w') as f:
                f.write(self.text_box.get("1.0", tk.END))
        else:
            self.save_file_as()
    def save_file_as(self):
        file_types = [('Text files', '.txt'), ('All files', '.*')]
        self.filename = tk.filedialog.asksaveasfilename(defaultextension='.txt', filetypes=file_types)
        if self.filename:
            if not self.filename.endswith('.txt'):
                self.filename += '.txt'
            self.save_file()
    # Call the Command List window to open        
    def command_list_list(self):
        self.master.grab_release()  # Release any existing grabs
        popup = CommandListPopup(self, self.text_box)
        popup.grab_set()
     # Open COM Settings Dialog and update selected port and baudrate       
    def open_com_settings(self):
        dialog = ComSettingsDialog(self.master, self.selected_port.get(), self.baudrate.get())
        self.master.wait_window(dialog.top)
        if dialog.result is not None:
            self.selected_port.set(dialog.result[0])
            self.baudrate.set(dialog.result[1])
            self.baud_label.config(text= f"{self.baudrate.get}")
# Wencam Settings            
    def show_webcam(self, camera_port, fps):
        if self.webcam_running:
            return
        self.live_view.config(text="Connecting to webcam...")
        self.parent.update()
        self.cap = cv2.VideoCapture(camera_port)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        if not self.cap.isOpened():
            self.live_view.config(text="Failed to connect to webcam. Please check your webcam settings.")
            return
        self.camthread = threading.Thread(target=self.update_webcam)
        self.camthread.start()
        self.webcam_button.config(bg='green')
        self.webcam_running = True
    def update_webcam(self):
        while self.camthread:
            ret, frame = self.cap.read()
            if ret:
                # Convert the frame to RGB format
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                new_width = 200
                new_height = 100
                frame = cv2.resize(frame, (new_width, new_height))
                image = Image.fromarray(frame)
                photo_image = ImageTk.PhotoImage(image)
                self.live_view.config(image=photo_image)
                self.live_view.image = photo_image
            else:
                # Display an error message if the webcam fails to connect
                self.live_view.config(text="Failed to connect to webcam.")
                break
            time.sleep(0.05)
        self.cap.release()
        cv2.destroyAllWindows()
    def cam_pop_up(self, event):
        # Create a new window
        pop_up_window = tk.Toplevel(self.parent)
        pop_up_window.title("Live Feed")
        pop_up_window.geometry("500x500")
        # Create a new frame for the live view in the pop-up window
        live_view_frame_pop_up = tk.Frame(pop_up_window, borderwidth=2, relief="groove", bg='black')
        live_view_frame_pop_up.pack(expand=True, fill="both")
        # Create a new label for the live view in the pop-up window
        live_view_pop_up = tk.Label(live_view_frame_pop_up, text="")
        live_view_pop_up.pack(expand=True, fill="both")
        # Start the thread to update the live view in the new window
        self.thread_pop_up = threading.Thread(target=self.update_webcam_pop_up, args=(live_view_pop_up,))
        self.thread_pop_up.start()    
    def update_webcam_pop_up(self, live_view_pop_up):
        while self.thread_pop_up:
            ret, frame = self.cap.read()
            if ret:
                # Convert the frame to RGB format
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Calculate the new dimensions of the frame to maintain aspect ratio and fit inside the live view frame
                height, width, _ = frame.shape
                max_size = min(live_view_pop_up.winfo_width(), live_view_pop_up.winfo_height())
                ratio = min(max_size / width, max_size / height)
                new_width = int(ratio * width)
                new_height = int(ratio * height)
                # Resize the frame to fit the live view frame while maintaining aspect ratio
                frame = cv2.resize(frame, (new_width, new_height))
                # Convert the frame to PhotoImage format and display it in the live view label
                image = Image.fromarray(frame)
                photo_image = ImageTk.PhotoImage(image)
                live_view_pop_up.config(image=photo_image)
                live_view_pop_up.image = photo_image
            else:
                # Display an error message if the webcam fails to connect
                live_view_pop_up.config(text="Failed to connect to webcam.")
                break
            time.sleep(0.05)
        self.cap.release()
        cv2.destroyAllWindows()
    def stop_webcam(self):
        if self.camthread:
            self.camthread.join()
            self.camthread = None
        if self.cap:
            self.cap.release()
        self.webcam_button.config(bg='red')
        self.webcam_running = False
        cv2.destroyAllWindows()
    # Capture Image to File
    def capture_image(self):
        if not self.webcam_running:
            return
        self.capture_button.config(bg='green')
        ret, frame = self.cap.read()
        img_folder = 'images'
        if not os.path.exists(img_folder):
            os.makedirs(img_folder)
        img_num = len(os.listdir(img_folder))
        img_name = f'img_{img_num+1}.jpg'
        img_path = os.path.join(img_folder, img_name)
        cv2.imwrite(img_path, frame)
        self.capture_button.config(bg='gray')
    def record_video(self):
        if not self.webcam_running:
            return
        self.record_thread = threading.Thread(target=self.write_video)
        self.record_thread.start()
    def write_video(self):
        out = cv2.VideoWriter('', cv2.VideoWriter_fourcc(*'MJPG'), 10.0, (640, 480))
        while self.webcam_running:
            ret, frame = self.cap.read()
            if ret:
                out.write(frame)
            else:
                break
        out.release()
    def convert_frame(self, frame):
        """Converts a OpenCV frame to a format that can be displayed in a tkinter label"""
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, _ = frame.shape
        img = tk.PhotoImage(master=self.live_view, width=w, height=h)
        img.blank = False  # keep a reference to the image to prevent garbage collection
    def image_path(self):
        return self.image_path_var.get()
    def video_path(self):
        return self.video_path_var.get()
    def camera_port(self):
        return self.port_var.get()
    def fps(self):
        return self.fps_entry.get()         
# Webcam Settings pop up Window        
    def cam_settings_window(self):
        # Create the settings window
        settings_window = tk.Toplevel(self)
        settings_window.title("Camera Settings")
        # Define default values

    # Read the configuration file to get the saved filenames
        try:
            with open("webcam_settings.txt", "r") as f:
                for line in f:
                    key, value = line.strip().split("=")
                    if key == "image_filename":
                        self.image_filename = value
                    elif key == "image_path":
                        self.image_path_var.set(value)
                    elif key == "video_filename":
                        self.video_filename = value
                    elif key == "video_path":
                        self.video_path_var.set(value)
        except FileNotFoundError:
            # If the configuration file doesn't exist, use default values
            self.image_filename = "output.jpg"
            self.image_path = ""
            self.video_filename = "output.avi"
            self.video_path = ""
        # Image filename label and entry
        tk.Label(settings_window, text="Image Filename:").grid(row=0, column=0, sticky="w")
        self.image_filename_entry = tk.Entry(settings_window, width=30)
        self.image_filename_entry.insert(0, "")
        self.image_filename_entry.grid(row=0, column=1, sticky="w")
        # Image path label, button, and entry
        tk.Label(settings_window, text="").grid(row=1, column=0, sticky="w")
        self.image_path_entry = tk.Entry(settings_window, width=30)
        self.image_path_entry.grid(row=1, column=1, sticky="w")
        self.image_path_button = tk.Button(settings_window, text="Image Path:", command=self.select_image_path)
        self.image_path_button.grid(row=1, column=0, sticky="w")
        self.image_path_label = tk.Label(settings_window, text="")
        self.image_path_label.grid(row=1, column=2, sticky="w")
        # Video filename label and entry
        tk.Label(settings_window, text="Video Filename:").grid(row=2, column=0, sticky="w")
        self.video_filename_entry = tk.Entry(settings_window, width=30)
        self.video_filename_entry.insert(0, "")
        self.video_filename_entry.grid(row=2, column=1, sticky="w")
        # Video path label, button, and entry
        tk.Label(settings_window, text="").grid(row=3, column=0, sticky="w")
        self.video_path_entry = tk.Entry(settings_window, width=30)
        self.video_path_entry.grid(row=3, column=1, sticky="w")
        self.video_path_button = tk.Button(settings_window, text="Video Path:", command=self.select_video_path)
        self.video_path_button.grid(row=3, column=0, sticky="w")
        self.video_path_label = tk.Label(settings_window, text="")
        self.video_path_label.grid(row=3, column=2, sticky="w")
        # Create variables for image path and video path
        self.update_image_path = tk.StringVar(value="")
        self.update_video_path = tk.StringVar(value="")
        # Camera port label and menu
        tk.Label(settings_window, text="Camera Port:").grid(row=0, column=3, sticky="e")
        self.port_var = tk.StringVar(settings_window)
        self.port_var.set("")
        self.camport_menu = tk.OptionMenu(settings_window, self.port_var, "")
        self.camport_menu.grid(row=0, column=4, sticky="w")
        # Search open ports button
        tk.Button(settings_window, text="Search Open Ports", command=self.search_ports).grid(row=2, column=3, sticky="e")
        # Connect button
        tk.Button(settings_window, text="Connect", command=self.show_webcam).grid(row=2, column=4, sticky="e")
        # FPS label and entry
        tk.Label(settings_window, text="FPS:").grid(row=1, column=3, sticky="e")
        self.fps_entry = tk.Entry(settings_window, width=10)
        self.fps_entry.insert(0, "30")
        self.fps_entry.grid(row=1, column=4, sticky="w")
        # Save button
        tk.Button(settings_window, text="Save Settings", command=self.save_settings).grid(row=3, column=4, sticky="w")
        # Set the settings window to modal
        settings_window.grab_set()        
    def select_video_path(self):
        video_path = filedialog.askdirectory()
        if video_path:
            self.video_path_var.set(video_path)
            self.video_path_entry.delete(0, tk.END)
            self.video_path_entry.insert(0, video_path)
            self.video_path_entry.bind("<FocusOut>", lambda event: self.update_video_path())  
            # Update the settings file with the new values
        with open('settings.txt', 'w') as f:
            f.write(self.video_filename_entry.get() + '\n')
            f.write(self.video_path_entry.get() + '\n')
    def select_image_path(self):
        image_path = filedialog.askdirectory()
            # Update the settings file with the new values
        with open('settings.txt', 'w') as f:
            f.write(self.image_filename_entry.get() + '\n')
            f.write(self.image_path_entry.get() + '\n')
            # Bind update functions to entry widgets
            self.image_path_entry.bind("<FocusOut>", lambda event: self.update_image_path())
        if image_path:
            self.image_path_var.set(image_path)
            self.image_path_entry.delete(0, tk.END)
            self.image_path_entry.insert(0, image_path)
  # Search for Connected Webcams                  
    def search_ports(self):
        # Get connected camera ports
        cam_ports = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cam_ports.append(i)
                cap.release()
        if cam_ports:
            # Update the camera port menu with the connected ports
            self.camport_menu['menu'].delete(0, 'end')
            for camport in cam_ports:
                # Add each connected port to the menu
                self.camport_menu['menu'].add_command(label=str(camport), command=lambda p=camport: self.port_var.set(p))
            # Set the default port to the first connected port
            self.port_var.set(str(cam_ports[0]))
        else:
            # If no cameras are connected, display an error message
            self.camport_menu['menu'].delete(0, 'end')
            self.port_var.set("")
            self.camport_menu['menu'].add_command(label="No cameras are currently connected")
    def save_settings(self):
        # Retrieve the values from the entry fields and drop-down menu
        camera_port = self.port_var.get().strip()
        fps = self.fps_entry.get().strip()
        video_filename = self.video_filename_entry.get().strip()
        video_path = self.video_path_label.cget("text").strip()
        image_filename = self.image_filename_entry.get().strip()
        image_path = self.image_path_label.cget("text").strip()
        current_settings = (camera_port, fps, video_filename, video_path, image_filename, image_path)
        # Check which settings have been changed and update the current settings
        if camera_port:
            current_settings = (int(camera_port),) + current_settings[1:]
        if fps:
            current_settings = current_settings[:1] + (int(fps),) + current_settings[2:]
        if video_filename:
            current_settings = current_settings[:2] + (video_filename,) + current_settings[3:]
        if video_path:
            current_settings = current_settings[:3] + (video_path,) + current_settings[4:]
        if image_filename:
            current_settings = current_settings[:4] + (image_filename,) + current_settings[5:]
        if image_path:
            current_settings = current_settings[:5] + (image_path,)
        # Write the settings to the configuration file
        with open("webcam_settings.txt", "w") as f:
            f.write(f"video_filename={current_settings[2]}\n")
            f.write(f"video_path={current_settings[3]}\n")
            f.write(f"image_filename={current_settings[4]}\n")
            f.write(f"image_path={current_settings[5]}\n")

        # Save the updated settings to the parent window
        self.parent.camera_settings = current_settings

# Command List Popup Window             
class CommandListPopup(tk.Toplevel):
    def __init__(self, parent, text_box):
        super().__init__(parent)
        self.title("Command List")
        self.geometry("600x600")
        self.resizable(True, True)
        self.text_box = text_box
        # Create a search box and label
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.search_command)
        self.search_label = ttk.Label(self, text="Search:")
        self.search_label.pack(side=tk.TOP, padx=5, pady=5)
        self.search_box = ttk.Entry(self, textvariable=self.search_var, width=30)
        self.search_box.pack(side=tk.TOP, padx=5, pady=5)
        # Create a treeview to display the command list
        self.treeview = ttk.Treeview(self)
        self.treeview.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # Define columns for the treeview
        self.treeview["columns"] = ("format", "description")
        self.treeview.column("#0", width=75, anchor="w")
        self.treeview.column("format", width=50)
        self.treeview.column("description", width=500, anchor="w")
        # Add headings for the columns
        self.treeview.heading("#0", text="Command")
        self.treeview.heading("format", text="Code")
        self.treeview.heading("description", text="Description")
        # Add a scrollbar to the treeview
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.treeview.yview)
        self.scrollbar.pack(side=tk.RIGHT)
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        # Add a right-click context menu to the treeview
        self.treeview.bind("<Button-3>", self.show_context_menu)
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Copy Command", command=self.copy_command)
        self.context_menu.add_command(label="Copy Description", command=self.copy_description)
        # Add the command list data to the treeview
        self.treeview.bind("<Double-Button-1>", self.paste_command)
        self.update_treeview()
        # Start the event loop
        self.parent = parent
        self.protocol("WM_DELETE_WINDOW")
        self.mainloop()
    def update_treeview(self):
        self.treeview.delete(*self.treeview.get_children())
    # Add the command list data to the treeview
        for command, data in command_list.command_list.items():
            comment = data.get("f", "N/A")
            description = data.get("description", "N/A")
            if self.search_var.get().lower() in command.lower() or self.search_var.get().lower() in comment.lower() or self.search_var.get().lower() in description.lower():
                self.treeview.insert("", "end", text=command, values=(comment, description))
    def search_command(self, *args):
        self.update_treeview()
    def show_context_menu(self, event):
        item = self.treeview.identify("item", event.x, event.y)
        if item:
            self.treeview.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
        # Double Click to send command to program box
    def paste_command(self, event):
        selected_item = self.treeview.selection()[0]
        command = self.treeview.item(selected_item, "text")
        text_box = self.parent.text_box
        # Replace selected text if there is any
        if text_box.tag_ranges("sel"):
            start, end = self.text_box.tag_ranges("sel")
            text_box.delete(start, end)
            text_box.insert(start, f"{command}")
        else:
            # Find the next empty line in the text box and paste the command there
            line_number = 1
            while True:
                if not self.text_box.get(f"{line_number}.0", f"{line_number}.end"):
                    self.text_box.insert(f"{line_number}.0", f"{command}\n")
                    break
                line_number += 1
        self.context_menu.add_command(label="Paste Command", command=self.paste_command)
    # Right Click to Copy Command or Description
    def copy_command(self):
        selected_item = self.treeview.selection()[0]
        command = self.treeview.item(selected_item, "text")
        self.clipboard_clear()
        self.clipboard_append(command)
    def copy_description(self):
        selection = self.treeview.selection()
        if selection:
            description = self.treeview.item(selection, "values")[1]
            self.clipboard_append(description)
            
# COM Port Settings Menu
class ComSettingsDialog(Dialog):
    def __init__(self, parent, serport, baudrate):
        self.serport = serport
        self.baudrate = baudrate
        super().__init__(parent, title="COM Settings")
    def body(self, master):
        port_label = tk.Label(master, text="Port:")
        port_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.port_entry = tk.Entry(master, width=10)
        self.port_entry.insert(END, self.serport)
        self.port_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        baudrate_label = tk.Label(master, text="Baudrate:")
        baudrate_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.baudrate_entry = tk.Entry(master, width=10)
        self.baudrate_entry.insert(END, self.baudrate)
        self.baudrate_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        return self.port_entry
    def apply(self):
        serport = self.port_entry.get()
        baudrate = self.baudrate_entry.get()
        try:
            baudrate = int(baudrate)
        except ValueError:
            messagebox.showerror("Error", "Baudrate must be an integer")
            return
        self.result = (serport, baudrate)        
        
if __name__ == "__main__":
    
    root = tk.Tk()
    app = Application(master=root, parent=root)
    app.mainloop()