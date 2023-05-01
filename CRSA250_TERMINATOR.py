import serial
import serial.tools.list_ports
import time
import psutil
import os
import sys
import csv
import threading
import re
import error_codes #Library Containing CRS A250 Error Codes
import command_list #Library Containing CRS A250 Command List
import cv2
import PIL
import numpy as np
import tensorflow as tf
import pytesseract
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.ttk as ttk

from command_list import * #Library Containing CRS A250 Command List
from pathlib import Path
from threading import Thread, Event
from tkinter import PanedWindow
from ttkthemes import ThemedTk
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



root = ThemedTk()
root.set_theme("black")
root.wm_title("CRS A250 Terminal")
#tabs = Application(root)
#app = Application(master=root, parent=root)    

selected_port = tk.StringVar(value="COM5")
baudrate = tk.IntVar(value=9600)
command_list = command_list
gripper_closed = False  # add a variable to keep track of the gripper status
serial_connected = False
serial = None
error_codes_window = None
after_id = None
cap = None
thread = None
camera_port = 0
fps = 30
camthread = None
webcam_running = False
#parent = parent
image_path_entry = None
video_path_entry = None
camera_settings = None
run_ocr = False
CRS_Connected = False
notebook_visible = False
tab1 = None
tab2 = None
tab3 = None
tab4 = None
tab5 = None
ocr_data = []
image_path_var = tk.StringVar(value="")
video_path_var = tk.StringVar(value="")
image_filename_var = tk.StringVar(value="")
video_filename_var = tk.StringVar(value="")
fps_var = tk.StringVar()
port_var = tk.StringVar()
master.protocol("WM_DELETE_WINDOW", on_closing)
original_stdout_fd = os.dup(sys.stdout.fileno())
original_stdout = os.fdopen(original_stdout_fd, "w")
paned_window = tk.PanedWindow(master, orient=tk.VERTICAL)  


##############################################
# Serial Connection
##############################################
######################################################################## M
##############################################     MAIN #### WINDOW    # A
############################################## ### MAIN #### WINDOW #### I
##############################################     MAIN #### WINDOW    # N
######################################################################## !


##############################################
# MAIN WINDOW GUI
##############################################

# TERMINAL BOX
terminal_frame = tk.Frame(master)
terminal_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
terminal = tk.Text(terminal_frame, width=40, height=15, font=('Courier', 10))
terminal.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
terminal.configure(background="black", foreground="white")
terminal.config(yscrollcommand=send_command_serial)
scrollbar = tk.Scrollbar(terminal_frame, command=terminal.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
terminal.config(yscrollcommand=scrollbar.set)

# MDI ENTRY 
mdi_box = tk.Entry(terminal_frame, width=40, font=('Courier', 10))
mdi_box.grid(row=1, column=0, padx=5, pady=0, sticky="sw")
mdi_box.bind('<Return>', clear_mdi)

# APPLICATION LOG
appOut_frame = tk.Frame(terminal_frame, background=master["background"])
appOut_frame.grid(row=2, column=0, padx=5, pady=8, sticky="nsew")
appOut = tk.Text(appOut_frame, width=26, height=4, wrap="word", state="normal")
appOut.grid(row=0, column=0, sticky="nsew")
scrollbar = tk.Scrollbar(appOut_frame, command=appOut.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
appOut["yscrollcommand"] = scrollbar.set
appOut.configure(background=master["background"], foreground="black")

# PROGRAMMING BOX
programming_window_frame = tk.Frame(terminal_frame)
programming_window_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
program_box = tk.Text(programming_window_frame, width=40, height=15)
program_box.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# LOAD LAST PROGRAM
load_text()

# SET GRID SPACING
terminal_frame.grid_rowconfigure(0, weight=5)
terminal_frame.grid_rowconfigure(1, weight=1)
terminal_frame.grid_rowconfigure(2, weight=1)
terminal_frame.grid_columnconfigure(0, weight=5)
terminal_frame.grid_columnconfigure(1, weight=0)
terminal_frame.grid_columnconfigure(2, weight=5)
programming_window_frame.grid_rowconfigure(0, weight=1)
programming_window_frame.grid_rowconfigure(1, weight=0)
programming_window_frame.grid_columnconfigure(0, weight=1)
mdi_box.grid(row=1, column=0, padx=5, pady=0, sticky="nsew")


##############################################
# Create the frame for the programming buttons
##############################################

# FRAME FOR THE BUTTONS
programming_button_frame = tk.Frame(terminal_frame)
programming_button_frame.grid(row=1, column=2, padx=5, pady=0, sticky="nsew")

# SEND PROGRAM BUTTON
send_text_button = tk.Button(programming_button_frame, text="Send",  command=send_program)
send_text_button.grid(row=0, column=3, padx=5, pady=0, sticky="se")

# COMMAND LIST BUTTON
command_list_button = tk.Button(programming_button_frame, text="Commands", command=command_list_list)
command_list_button.grid(row=1, column=1, padx=5, pady=0, sticky="sw")

# SAVE BUTTON
save_button = tk.Button(programming_button_frame, text="Save", command=save_file)
save_button.grid(row=0, column=2, padx=5, pady=0)

# LOAD BUTTON
load_button = Button(programming_button_frame, text="Load", command = open_file)
load_button.grid(row=0, column=1, padx=5, pady=0)

# CONNECT BUTTON
serial_button = tk.Button(programming_button_frame, text="Connect", command = toggle_connection, bg='red')
serial_button.grid(row=0, column=0, padx=0, pady=0, sticky="w")

# EXPAND CONGIGURATION BUTTON
showbox_button = Button(programming_button_frame, text="Toggle Tabs", command=lambda: create_tabs(paned_window, showbox_button))
showbox_button.grid(row=1, column=2, padx=5, pady=0, sticky="sw")


##############################################
# MANUAL MODE BUTTON AND TOGGLE FUNCTION
##############################################

manual_frame = tk.Frame(programming_button_frame)
manual_frame.grid(row=1, column=0)
manual_button_state = False  # initial state of the manual button
manual_button_text = tk.StringVar(value="MANUAL")
# Create toggle button for manual mode
def toggle_manual_mode():
    manual_button_state = not manual_button_state
    data = display_serial_input()
    if data and ("j>" in data or "c>" in data):
            manual_button_text.set("NOMANUAL")
            command_string = f"NOMANUAL"
            print("Current manual mode:", manual_mode.get())
    else:
        manual_button_text.set("MANUAL")
        command_string = f"MANUAL {manual_mode.get()}"
        print("Current manual mode:", manual_mode.get())
    send_command_serial(command_string)
manual_mode = tk.StringVar(value="JOINT")
def set_manual_mode_to_joint():
    manual_mode.set("JOINT")
manual_mode_toggle_joint = tk.Radiobutton(manual_frame, text="J", variable=manual_mode, value="JOINT", command=set_manual_mode_to_joint)
manual_mode_toggle_joint.grid(row=0, column=1)
def set_manual_mode_to_cylindrical():
    manual_mode.set("CYLINDRICAL") 
manual_mode_toggle_cylindrical = tk.Radiobutton(manual_frame, text="C", variable=manual_mode, value="CYLINDRICAL", command=set_manual_mode_to_cylindrical)
manual_mode_toggle_cylindrical.grid(row=0, column=2)
manual_button = tk.Button(manual_frame, textvariable=manual_button_text, command=toggle_manual_mode)
manual_button.grid(row=0, column=0)

##############################################
# SET PANNED WINDOW
##############################################

paned_window = paned_window
if notebook_visible:
    showbox_button.config(text="Toggle Tabs")
    notebook_frame.grid_remove()
    paned_window.remove(notebook_frame)
    paned_window.grid_remove()
    paned_window.remove(paned_window)
    notebook_visible = False
    # Check if paned window is empty and reset window size if it is
    if len(paned_window.panes()) == 0:
        master.geometry("")
else:
    showbox_button.config(text="Hide Tabs")
    # Create the notebook and add it to the paned window
    paned_window.grid(row=0, column=5, padx=5, pady=5, sticky="nsew")
    notebook_frame = tk.Frame(paned_window)
    notebook_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
    notebook = ttk.Notebook(notebook_frame)
    notebook.grid(row=0, column=0, sticky="nsew")
    
######################################################################## T
##############################################     TAB 1     WEBCAM    # A
############################################## ### TAB 1 ### WEBCAM #### B
##############################################     TAB 1     WEBCAM    #
######################################################################## 1         
    
    # TAB 1 FRAME
    tab1 = tk.Frame(notebook)
    notebook.add(tab1, text="Webcam")
##############################################
# WEBCAM 
##############################################
    webcam_frame = tk.Frame(tab1, borderwidth=2, width=200, height=100)
    webcam_frame.grid(row=1, column=0, padx=5, pady=0, sticky="se")
    
    # LIVE VIEW WINDOW
    live_view_frame = tk.Frame(webcam_frame, borderwidth=2, bg='black')
    live_view_frame.grid(row=0, column=0,)
    live_view_width = 200
    live_view_height = 100
    live_view = tk.Label(live_view_frame, text="'Webcam' Button to Connect \n\n Config Settings in Connection Menu", font=("Helvetica", 8), pady=20, fg="white", bg="black") #width=live_view_width, height=live_view_height,
    live_view.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
    live_view_frame.grid_propagate(False)
    live_view_frame.config(width=live_view_width, height=live_view_height)
    live_view.bind("<Double-Button-1>", cam_pop_up)
    
    # CAMERA BUTTONS
    cam_buttons_frame = tk.Frame(webcam_frame, borderwidth=0)
    cam_buttons_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nwse")
    webcam_button = tk.Button(cam_buttons_frame, text="Webcam", command=show_webcam, bg='red')
    webcam_button.grid(row=0, column=0, padx=5, pady=5)
    capture_button = tk.Button(cam_buttons_frame, text="Capture", command=capture_image, bg='gray')
    capture_button.grid(row=0, column=1, padx=5, pady=5)
    record_button = tk.Button(cam_buttons_frame, text="Record", command=record_video, bg='gray')
    record_button.grid(row=0, column=2, padx=5, pady=5)
    after_id = None
    cap = None

    
######################################################################## T
##############################################     TAB 2    CONTROL    # A
############################################## ### TAB 2 ### DATA ###### B
##############################################     TAB 2    CONTROL    # 
######################################################################## 2

    # TAB 2
    tab2 = tk.Frame(notebook)
    notebook.add(tab2, text="Control")
   
    # FRAMES
    axis_frame = tk.Frame(tab2)
    axis_frame.grid(row=1, column=0)   
    speed_frame = tk.Frame(axis_frame, borderwidth=1)
    speed_frame.grid(row=4, column=3, padx=0, pady=0, sticky="nw")
    
    # SPEED SLIDER
    speed_slider = Scale(speed_frame, from_=0, to=100, orient=HORIZONTAL, relief=tk.SOLID)
    speed_slider.grid(row=0, column=0, padx=0, pady=0, sticky="nw")
    speed_label = tk.Button(speed_frame, text="Speed", command=process_code)
    speed_label.grid(row=0, column=1, padx=0, pady=10, sticky="nw")
    
    # GRIPPER TOGGLE BUTTON
    gripper_button = tk.Button(speed_frame, text="Open Gripper", command=toggle_gripper)
    gripper_button.grid(row=1, column=0, padx=0, pady=0, sticky="nw")
    
    # AXIS BUTTONS
    axis_labels = ["Axis 1", "Axis 2", "Axis 3", "Axis 4", "Axis 5", "Axis 6"]
    for i, label in enumerate(axis_labels):
        axis_label = Label(axis_frame, text=label)
        axis_label.grid(row=i, column=0, padx=5, pady=5)
        plus_button = Button(axis_frame, text="+", width=5, command=lambda x=i: process_code(f"{axis_labels[x]} +"))
        plus_button.grid(row=i, column=1, padx=5, pady=5)
        minus_button = Button(axis_frame, text="-", width=5, command=lambda x=i: process_code(f"{axis_labels[x]} -"))
        minus_button.grid(row=i, column=2, padx=5, pady=5)
    interpolate_label = Label(axis_frame, text="Interpolated Motion")
    interpolate_label.grid(row=0, column=3, padx=5, pady=5, columnspan=2)
    move1_button = Button(axis_frame, text="Move 1", width=10, command=lambda: process_code("Move 1"))
    move1_button.grid(row=1, column=3, padx=5, pady=5)
    move2_button = Button(axis_frame, text="Move 2", width=10, command=lambda: process_code("Move 2"))
    move2_button.grid(row=2, column=3, padx=5, pady=5)
    move3_button = Button(axis_frame, text="Move 3", width=10, command=lambda: process_code("Move 3"))
    move3_button.grid(row=3, column=3, padx=5, pady=5)
    
    
######################################################################## T
##############################################     TAB 3    DATA OUT   # A
############################################## ### TAB 3 ### DATA ###### B
##############################################     TAB 3    DATA OUT   #
######################################################################## 3

    # Create a frame for the second tab
    tab3 = tk.Frame(notebook)
    notebook.add(tab3, text="I/O")
    
    
######################################################################## T
##############################################     TAB 4    DATA OUT   # A
############################################## ### TAB 4 ### DATA ###### B
##############################################     TAB 4    DATA OUT   #
######################################################################## 4

    # Create a frame for the second tab
    tab4 = tk.Frame(notebook)
    notebook.add(tab4, text="Command")
    
    
######################################################################## T
##############################################     TAB 5    DATA OUT   # A
############################################## ### TAB 5 ### DATA ###### B
##############################################     TAB 5    DATA OUT   # 
######################################################################## 5

# Create a frame for the second tab
    tab5 = tk.Frame(notebook)
    notebook.add(tab5, text="Config")
#create main frames
    serial_frame = tk.Frame(tab5)
    serial_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
    
    camConfig_frame = tk.Frame(tab5, relief="ridge", borderwidth=1)
    camConfig_frame.grid(row=3, column=0, padx=5, pady=5, sticky="nw")
    
    camFile_frame = tk.Frame(tab5)
    camFile_frame.grid(row=0, column=0, padx=(175, 0), pady=5, sticky="nw")     
    
    
##############################################     
# COM Settings
############################################## 

    available_serports = get_available_ports()
    selected_port.set(available_serports[0] if available_serports else '')
    port_menu = ttk.Combobox(serial_frame, textvariable=selected_port, values=available_serports)
    port_menu.config(width=10)
    port_menu.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    serial_button = tk.Button(serial_frame, text="Connect", command=toggle_connection, bg='red')
    serial_button.grid(row=0, column=1, padx=0, pady=4, sticky="w")      
    port_entry = tk.Entry(serial_frame, width=15)
    port_entry = PlaceholderEntry(serial_frame, width=15, placeholder='COM Port')
    #port_entry.insert(selected_port)
    port_entry.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    roBaud_label = tk.Label(serial_frame, text="9600")
    roBaud_label.grid(row=1, column=0, padx=(60,0), pady=5, sticky="w")
    baud_button = tk.Button(serial_frame, text="Serial: A", command=toggle_baudrate)
    baud_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    baudrate_entry = tk.Entry(serial_frame, width=6)
    baudrate_entry = PlaceholderEntry(serial_frame, width=6, placeholder='Baud')
    #  baudrate_entry.insert(Entry, baudrate)
    baudrate_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")


############################################## 
# Webcam Settings
############################################## 

    camFile_label = tk.Label(camConfig_frame, text="Image Filename:").grid(row=0, column=0, sticky="w")
    image_filename_entry = tk.Entry(width=30, textvariable=image_filename_var)
    image_filename_entry.grid(row=0, column=1, sticky="w")
    # Image path label, button, and entry
    camPath_label = tk.Label(camConfig_frame, text="").grid(row=1, column=0, sticky="w")
    image_path_entry = tk.Entry(camConfig_frame, width=30, textvariable=image_path_var)
    image_path_entry.grid(row=1, column=1, sticky="w")
    image_path_button = tk.Button(camConfig_frame, text="Image Path:", command=select_image_path)
    image_path_button.grid(row=1, column=0, sticky="w")
    image_path_label = tk.Label(text="")
    image_path_label.grid(row=1, column=2, sticky="w")
    # Video filename label and entry
    camFile_label = tk.Label(camConfig_frame, text="Video Filename:").grid(row=2, column=0, sticky="w")
    video_filename_entry = tk.Entry(camConfig_frame, width=30, textvariable=video_filename_var)
    video_filename_entry.grid(row=2, column=1, sticky="w")
    # Video path label, button, and entry
    camPath_label = tk.Label(camConfig_frame, text="").grid(row=3, column=0, sticky="w")
    video_path_entry = tk.Entry(camConfig_frame, width=30, textvariable=video_path_var)
    video_path_entry.grid(row=3, column=1, sticky="w")
    video_path_button = tk.Button(camConfig_frame, text="Video Path:", command=select_video_path)
    video_path_button.grid(row=3, column=0, sticky="w")
    video_path_label = tk.Label(camConfig_frame, text="")
    video_path_label.grid(row=3, column=2, sticky="w")
    # Create variables for image path and video path
    update_image_path = tk.StringVar(value="")
    update_video_path = tk.StringVar(value="")
    
    
##############################################     
# Camera port    
############################################## 

    # Camera port label and menu
    port_var = tk.StringVar()
    port_var.set("")
    camport_menu = tk.OptionMenu(camFile_frame, port_var, "")
    camport_menu.grid(row=0, column=0, sticky="w")
    # Search open ports button
    camPorts_button = tk.Button(camFile_frame, text="SearchPorts", command=search_ports).grid(row=0, column=1, sticky="e")
    # Connect button
    camFps_label = tk.Label(camFile_frame, text="FPS:").grid(row=2, column=0, sticky="e")
    fps_entry = tk.Entry(camFile_frame, width=10)
    fps_entry.insert(0, "30")
    fps_entry.grid(row=2, column=1, sticky="w")
    
    
############################################## 
# Save button
############################################## 

    camSave_button = tk.Button(tab5, text="Save Settings", command=save_settings).grid(row=5, column=0, sticky="w")                                    
        
    
############################################## 
############################################## 
####### TABS OVER ######### TABS OVER ########
############################################## 
##############################################    
 
    notebook.grid(row=1, column=0, sticky="nsew")
    master.grid_rowconfigure(1, weight=1)
    master.grid_columnconfigure(0, weight=1)
    notebook_visible = True
    paned_window.add(paned_window)
    paned_window.add(notebook_frame)
    orig_geometry = master.geometry()


############################################## 
# ctrl + Options
############################################## 

#master.bind("<Control-o>", lambda event: toggle_ocr())


############################################## 
# Create Menu Bar
############################################## 

menu_bar = tk.Menu(master)
master.config(menu=menu_bar)
 
# CREATE FILE MENU
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Save", command = save_file)
file_menu.add_command(label="Save As...", command=save_file_as)
file_menu.add_command(label="Open", command=open_file)
menu_bar.add_cascade(label="File", menu=file_menu)

# HELP MENU
helpmenu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=helpmenu)

# ERRORS
helpmenu.add_command(label="Error Codes", command=error_window)

# COMMAND LIST
helpmenu.add_command(label="Command List", command=command_list_list)
manual_menu = tk.Menu(helpmenu, tearoff=0)

# MANUALS
helpmenu.add_cascade(label="Manuals", menu=manual_menu)
manual_menu.add_command(label="Tutorial", command=lambda: open_manual(1))
manual_menu.add_command(label="Programming", command=lambda: open_manual(2))
manual_menu.add_command(label="Operation", command=lambda: open_manual(3))

# CONNECTION MENU
connection_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Connection", menu=connection_menu)
connection_menu.add_command(label="Webcam", command=webcam_settings_window)

# TOOLS MENU
tools_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Tools", menu=tools_menu)
ocr_config_menu = Menu(tools_menu, tearoff=0)
ocr_config_menu.add_command(label="OCR Data", command=show_ocr_data_popup)
tools_menu.add_cascade(label="OCR Config", menu=ocr_config_menu)
little_tools = Menu(tools_menu, tearoff=0)
little_tools.add_command(label="Mark")
tools_menu.add_cascade(label="Little Tools", menu=little_tools)


############################################################################################
############################################################################################
######## GUI OVER ######### GUI OVER ################# GUI OVER ######### GUI OVER #########
############################################################################################
############################################################################################

    # Search for available serial ports and report to terminal
def get_available_ports():
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
def toggle_baudrate():
    baudrate_options = [(9600, 'Serial: A'), (2400, 'Serial: B')]
    current_baudrate = baudrate.get()
    for baudrate, label in baudrate_options:
        if current_baudrate == baudrate:
            baudrate.set(baudrate_options[(baudrate_options.index((baudrate, label)) + 1) % 2][0])
            baud_label.config(text= f"{baudrate_options[(baudrate_options.index((baudrate, label)) + 1) % 2][0]}")
            baud_button.config(text=baudrate_options[(baudrate_options.index((baudrate, label)) + 1) % 2][1])
            break
###############################################        
# Disconnect Serial Connection on Window Close
###############################################
def on_closing():
    if serial is not None:
        serial.close()
        print("Closing Serial Connection")
        CRS_Connected = False
    master.destroy()              
             
# Toggle Serial Connection                                           
def toggle_connection():
    if not serial_connected:
        serport = selected_port.get()
        baudrate = baudrate.get()
        print(baudrate)
        print("Attempting to connect to serial port")
        try:
                serial = serial.Serial(serport=serport, baudrate=baudrate, timeout=0, xonxoff=True, rtscts=True)
                serial.flush();
                serial_button.configure(text="Disconnect", bg="green")
                print("Connected to serial port.")
                CRS_Connected = True
                time.sleep(1.5)
                send_command_serial("NOHELP")
                master.after(1000,display_serial_input)
        except serial.serialutil.SerialException:
            messagebox.showerror("Connection Error", "Could not connect to " + selected_port.get())
            print("Connection to serial port failed.")     
    else:
        serial.close()
        if os.name == 'nt':
            serial.hEvent = None
        print("Closing Serial Connection")
        serial_connected = False
        CRS_Connected = False
        serial = None
        serial_button.configure(text="Connect", bg="red")   
##############################################
# Send code from MDI and Program boxes to be processed, But it looks cool when a program is running
##############################################

def send_program():
    try:
        start = program_box.index("sel.first")
        end = program_box.index("sel.last")
        selected_text = program_box.get(start, end)
    except TclError:
        selected_text = program_box.get("1.0", "end").strip()
    process_code(selected_text)
    # Remove the selection
    program_box.tag_remove("sel", "1.0", "end")
    # Set the cursor to the end of the text box
    program_box.mark_set("insert", "end")
    program_box.tag_remove("current_line", "1.0", "end")
    program_box.tag_remove("sent_line", "1.0", "end")
    program_box.update()
    program_box.focus_set() 
    
    
##############################################
    # Extract the command and time value from a command string
##############################################  

def extract_command_data(command_str):
    print(f"Extracting command data from string: {command_str}")
    command = ""
    value = ""
    if command_str.startswith("("):
        command, _, value = command_str.strip("()").partition(")")
    else:
        print(f"Invalid command string: {command_str}")
        return None
    print(f"Extracted command: {command} - Value: {value}")
    return command, value

# Check if code is for robot or software
def process_code(text):
    commands = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        for command_str in line.split():
            command_data = extract_command_data(command_str)
            if command_data is None:
                print(f"Invalid command: {command_str}")
                continue

            # Send command to app code if it exists
            command_key = f"({command_data[0]})"
            if command_key in command_list:
                command_info = command_list[command_key]
                print(f"Sending command to app code: {command_info} - Command data: {command_data}")
                app_code(command_info, {'value': command_data[1]})
            else:
                # Don't send commands in parentheses to serial
                if '(' not in command_str:
                    serial_command = f"{command_data[0]}:"
                    if command_data[1]:
                        serial_command += command_data[1]
                    serial_command += "\n"
                    print(f"Sending command directly to serial: {serial_command}")
                    send_to_serial(serial_command)
    return commands

# Process the command using the app code
def app_code(command_info, command_data):
    if 'T' in command_info.get('modes', ''):
        if command_data.get('value'):
            duration = int(command_data['value'])
            print(command_data['value'])
            print(command_info['app'])
        else:
            duration = 60  # Default to 60 seconds

        function_str = command_info['app'].replace('$', '')
        print(f"Executing function: {function_str} with duration {duration}")
        try:
            function_to_call = getattr(function_str)
            function_to_call(duration)
        except AttributeError as e:
            print(f"Function not found: {function_str} - Exception: {e}")
        except Exception as e:
            print(f"Failed to execute command: {command_info['command']} - Exception: {e}")

    else:
        function_str = command_info['app'].replace('$', '')
        print(f"Executing function: {function_str}")
        try:
            function_to_call = getattr(function_str)
            function_to_call()
        except AttributeError as e:
            print(f"Function not found: {function_str} - Exception: {e}")
        except Exception as e:
            print(f"Failed to execute command: {command_info['command']} - Exception: {e}")   
    # Function for the (WAIT) command  
def wait_function(duration=30):
    print(f"waiting for {duration} seconds")
    duration_ms = duration * 1000  # Convert duration to milliseconds
    send_text_button.config(state=tk.DISABLED)  # Disable the button
    after(duration_ms, lambda: send_text_button.config(state=tk.NORMAL))
    after(duration_ms + 100, print("done waiting"))


# Clear MDI Box once sent           
def clear_mdi( event=None):
    # Define Variables
    mdi_text= mdi_box.get().strip().upper()
    process_code(mdi_text)
    # Clear the mdi_box
    mdi_box.delete(0, tk.END)
    mdi_box.focus_set()
    
# Send Stuff to serial       
def send_command_serial(command):
    if CRS_Connected:
        command = command.strip().upper() + '\r\n'
        serial.write(command.encode('ascii'))
        terminal.yview_moveto(1.0)
    else:
        print(f"CRS not Connected or Detected. {command} blocked")  
    
# Display What is sent to serial from the controller
def display_serial_input():
    data = serial.read(baudrate.get())
    if data:
        data = data.decode('ascii')
        terminal.tag_config(data, foreground="green")
        terminal.insert(tk.END, f"{data} \r\n", "data")
        print(data)
        robot_error(data)  # call robot_error function with received data
    master.after(104, display_serial_input)
    return data  # add this line to return the received data



# Read serial input for errors       
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
            if hasattr('error_codes_window') and error_codes_window.winfo_exists():
                # If error window is open, update the search box and perform search
                search_box = error_codes_window.children['!frame'].children['!entry']
                search_box.focus_set()
                search_box.delete(0, tk.END)
                search_box.insert(0, error_code)
                search_box.insert(tk.END, error_code)
                print("Updating Error Window")
                display_serial_input()
            else:
                # If error window is closed, open it and perform search
                print("Opening Error Window")
                self.error_window()
                search_box = error_codes_window.children['!frame'].children['!entry']
                search_box.focus_set()
                search_box.delete(0, tk.END)
                search_box.insert(0, error_code)
                search_box.insert(tk.END, error_code)
                #error_codes_window = None  # Set error codes window attribute to None when closed
                self.error_window()
                display_serial_input()
        else:
            print("error code not found in database")
            display_serial_input()
            return
    else:
        display_serial_input()
        return


    # Gripper Button and Command
def toggle_gripper():
    # Toggle the gripper status and change the label and button text accordingly
    if gripper_closed:
        send_command_serial("OPEN GRIPPER")
        gripper_closed = False
        gripper_button.config(text="Open Gripper")
    else:
        send_command_serial("CLOSE GRIPPER")
        gripper_closed = True
        gripper_button.config(text="Close Gripper")


    # Save what is in the text box for next load        
def load_text():
    try:
        with open("saved_text.txt", "r") as f:
            program_box.delete("1.0", tk.END)
            program_box.insert(tk.END, f.read())
    except FileNotFoundError:
        pass
def save_text():
    with open("saved_text.txt", "w") as f:
        f.write(program_box.get("1.0", tk.END))
    master.destroy()    

##############################################
# Webcam Settings
##############################################

def save_last_port(port):
# Save the last used port to the webcam_settings.txt file
    try:
        with open('webcam_settings.txt', 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    for i in range(len(lines)):
        if lines[i].startswith('camera_port='):
            lines[i] = 'camera_port={}\n'.format(port)
            break
    else:
        lines.append('camera_port={}\n'.format(port))
    with open('webcam_settings.txt', 'w') as f:
        f.writelines(lines)
def start_webcam_thread():
    show_webcam_thread = threading.Thread(target=show_webcam)
    show_webcam_thread.start()
def show_webcam(fps=30):
    if webcam_running:
        return
    live_view.config(text="Connecting to webcam...")
    parent.update()
    try:
        fps = int(fps_var.get())  # Get the value of fps_var
    except ValueError:
        fps = 30  # Set default value if the input is not a valid integer
    try:
        with open('webcam_settings.txt', 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = []
    for line in lines:
        if line.startswith('camera_port='):
            try:
                last_port = int(line.split('=')[1].strip())
            except ValueError:
                last_port = 0  # Set default value if the last used port is not a valid integer
            break
    else:
        last_port = 0  # Set default value if the camera_port line is not found
    # Only search for the last port
    cap = cv2.VideoCapture(last_port)
    if cap.isOpened():
        save_last_port(last_port)  # Save the new port to the webcam_settings.txt file
    else:
        live_view.config(text="Failed to connect to webcam. Please check your webcam settings.")
        return
    cap.set(cv2.CAP_PROP_FPS, fps)
    webcam_button.config(bg='green')
    webcam_running = True
    camthread = True
    update_webcam_thread = threading.Thread(target=update_webcam)
    update_webcam_thread.start()
    
def toggle_ocr():
    run_ocr = not run_ocr
    print(f"OCR is now {'ON' if run_ocr else 'OFF'}")
            
def update_webcam():
    script_directory = os.path.dirname(os.path.abspath(__file__))
    tesseract_path = os.path.join(script_directory, "Tesseract-OCR", "tesseract.exe")
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    while camthread:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if run_ocr:
                gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                camText = pytesseract.image_to_string(gray)
                print(camText)
                run_ocr = False
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            camText = pytesseract.image_to_string(gray)
            print(camText)
            new_width = 200
            new_height = 100
            frame = cv2.resize(frame, (new_width, new_height))
            image = Image.fromarray(frame)
            photo_image = ImageTk.PhotoImage(image)
            live_view.config(image=photo_image)
            live_view.image = photo_image
            save_last_port(cap.get(cv2.CAP_PROP_POS_FRAMES))  # Save the last frame position to the webcam_settings.txt file
        else:
            live_view.config(text="Failed to connect to webcam.")
        time.sleep(0.05)
    cap.release()
    cv2.destroyAllWindows()

def cam_pop_up(event):
    # Create a new window
    pop_up_window = tk.Toplevel(parent)
    pop_up_window.title("Live Feed")
    pop_up_window.geometry("500x500")
    # Create a new frame for the live view in the pop-up window
    live_view_frame_pop_up = tk.Frame(pop_up_window, borderwidth=2, relief="groove", bg='black')
    live_view_frame_pop_up.pack(expand=True, fill="both")
    # Create a new label for the live view in the pop-up window
    live_view_pop_up = tk.Label(live_view_frame_pop_up, text="")
    live_view_pop_up.pack(expand=True, fill="both")
    
    if camthread == True:# Start the thread to update the live view in the new window
        thread_pop_up = threading.Thread(target=update_webcam_pop_up, args=(live_view_pop_up,))
        thread_pop_up.start()    
        

def update_webcam_pop_up(live_view_pop_up):
    while thread_pop_up:
        ret, frame = cap.read()
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
    cap.release()
    cv2.destroyAllWindows()
def stop_webcam():
    if camthread:
        camthread.join()
        camthread = None
    if cap:
        cap.release()
    webcam_button.config(bg='red')
    webcam_running = False
    cv2.destroyAllWindows()
# Capture Image to File
def capture_image():
    if not webcam_running:
        print("Webcam not connected!")
        return
    capture_button.config(bg='green')
    ret, frame = cap.read()
    img_folder = 'images'
    print("Image Captured")
    if not os.path.exists(img_folder):
        os.makedirs(img_folder)
    img_num = len(os.listdir(img_folder))
    img_name = f'img_{img_num+1}.jpg'
    img_path = os.path.join(img_folder, img_name)
    print(f"CAPIMG saved: {img_path}")  
    cv2.imwrite(img_path, frame)
    #print("Image saved to file")
    capture_button.config(bg='gray')
    
#  Record video for maximum of 60 seconds. (RECVID)"time" commands and sets recording time       
def record_video(duration):
    if not webcam_running:
        print("Webcam not running")
        return

    # Generate unique filename for video
    video_folder = 'videos'
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
    video_num = len(os.listdir(video_folder))
    video_name = f'video_{video_num+1}.avi'
    video_path = os.path.join(video_folder, video_name)

    # Write video frames to file
    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'MJPG'), 10.0, (640, 480))
    start_time = time.time()
    print(f"Recording video for {duration} seconds")

    while webcam_running and time.time() - start_time < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            break

    print(f"Recording Saved to {video_path}")
    out.release()
# Save the video to a file        
def write_video():
    if not webcam_running:
        print("Webcam not running")
        return
# Generate unique filename for video by counting the number of files with the same name in the videos folder
    video_folder = 'videos'
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
    video_num = len(os.listdir(video_folder))
    video_name = f'video_{video_num+1}.avi'
    video_path = os.path.join(video_folder, video_name)
# Write video frames to file
    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'MJPG'), 10.0, (640, 480))
    start_time = time.time()
    print(f"Starting recording for {recording_duration} seconds")
    while webcam_running and time.time() - start_time < recording_duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            break
    out.release()
    print(f"Recording Saved to {video_path}")
# Converts a OpenCV frame to a format that can be displayed in a tkinter label
def convert_frame(frame):
    """Converts a OpenCV frame to a format that can be displayed in a tkinter label"""
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, _ = frame.shape
    img = tk.PhotoImage(master=live_view, width=w, height=h)
    img.blank = False  # keep a reference to the image to prevent garbage collection
    
# Set Image and video paths 
def image_path():
    return image_path_var.get()
def video_path():
    return video_path_var.get()
def camera_port():
    return port_var.get()
def fps():
    return fps_entry.get() 




############################################## 
 # File Save Menu
############################################## 

def open_file():
    defaultextension = "newProgram"
    filename = filedialog.askopenfilename(defaultextension=".txt")
    if filename:
        filename = filename
        with open(filename, 'r') as f:
            program_box.delete("1.0", tk.END)
            program_box.insert(tk.END, f.read())        
def save_file():
    newFilename =  "newProgram"
    if newFilename:
        with open(newFilename, 'w') as f:
            f.write(program_box.get("1.0", tk.END))
    else:
        save_file_as()
def save_file_as():
    file_types = [('Text files', '.txt'), ('All files', '.*')]
    filename = tk.filedialog.asksaveasfilename(defaultextension='.txt', filetypes=file_types)
    if filename:
        if not filename.endswith('.txt'):
            filename += '.txt'
        save_file()





# Create a class for the application
class Application(tk.Frame):
    # Initialize the application
    def __init__(parent, master = None):
        super().__init__(master)
        # master = master   
                            
# Function to display error code pop-up window from error_codes.py
    def error_window():
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
        if not error_codes_window:
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
            # Set error_codes_window to the created Toplevel widget
            error_codes_window = error_codes_window
        else:
            # Bring existing window to the front
            error_codes_window.lift()
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
    def open_manual(manual_num):
        manual_names = {
            1: "CRSA250_Tutorial.pdf",
            2: "CRSA250_Programming_Manual.pdf",
            3: "CRSA250_Operators_Manual.pdf"
        }
        filename = manual_names.get(manual_num)
        if filename:
            os.startfile("J:\\Documents\\CRS Robot Arm Terminal Code\\CRS Robot Arm\\Manuals\\" + filename)
  

    # Call the Command List window to open        
    def command_list_list():
        master.grab_release()  # Release any existing grabs
        popup = CommandListPopup(program_box)
        popup.grab_set()
     # Open COM Settings Dialog and update selected port and baudrate       

##############################################         
#Open Webcam Settings Window   
##############################################  
  
    def webcam_settings_window():
        # Create the settings window
        window = Toplevel(master)
        window.title("Camera Settings")
        value = "" # assign a default value or set to an empty string
        image_filename_var = tk.StringVar(value=value)
        image_path_var = tk.StringVar(value=value)
        video_filename_var = tk.StringVar(value=value)
        video_path_var = tk.StringVar(value=value)
        fps_var = tk.StringVar(value="30")
        port_var = tk.StringVar(value="")
        settings_window()
        
        try:
            with open("webcam_settings.txt", "r") as f:
                for line in f:
                    key, value = line.strip().split("=")
                    if key == "image_filename":
                        image_filename_var.set(value)
                    elif key == "image_path":
                        image_path_var.set(value)
                    elif key == "video_filename":
                        video_filename_var.set(value)
                    elif key == "video_path":
                        video_path_var.set(value)
        except FileNotFoundError:
            # If the configuration file doesn't exist, use default values
            image_filename_var.set("output.jpg")
            video_filename_var.set("output.avi")
        # Image filename label and entry
        tk.Label(text="Image Filename:").grid(row=0, column=0, sticky="w")
        image_filename_entry = tk.Entry(width=30, textvariable=image_filename_var)
        image_filename_entry.grid(row=0, column=1, sticky="w")
        # Image path label, button, and entry
        tk.Label(text="").grid(row=1, column=0, sticky="w")
        image_path_entry = tk.Entry(width=30, textvariable=image_path_var)
        image_path_entry.grid(row=1, column=1, sticky="w")
        image_path_button = tk.Button(text="Image Path:", command=select_image_path)
        image_path_button.grid(row=1, column=0, sticky="w")
        image_path_label = tk.Label(text="")
        image_path_label.grid(row=1, column=2, sticky="w")
        # Video filename label and entry
        tk.Label(text="Video Filename:").grid(row=2, column=0, sticky="w")
        video_filename_entry = tk.Entry(width=30, textvariable=video_filename_var)
        video_filename_entry.grid(row=2, column=1, sticky="w")
        # Video path label, button, and entry
        tk.Label(text="").grid(row=3, column=0, sticky="w")
        video_path_entry = tk.Entry(width=30, textvariable=video_path_var)
        video_path_entry.grid(row=3, column=1, sticky="w")
        video_path_button = tk.Button(text="Video Path:", command=select_video_path)
        video_path_button.grid(row=3, column=0, sticky="w")
        video_path_label = tk.Label(text="")
        video_path_label.grid(row=3, column=2, sticky="w")
        # Create variables for image path and video path
        update_image_path = tk.StringVar(value="")
        update_video_path = tk.StringVar(value="")
        # Camera port label and menu
        tk.Label(text="Camera Port:").grid(row=0, column=3, sticky="e")
        port_var = tk.StringVar()
        port_var.set("")
        camport_menu = tk.OptionMenu(port_var, "")
        camport_menu.grid(row=0, column=4, sticky="w")
        # Search open ports button
        tk.Button(text="Search Open Ports", command=search_ports).grid(row=2, column=3, sticky="e")
        # Connect button
        tk.Label(text="FPS:").grid(row=1, column=3, sticky="e")
        fps_entry = tk.Entry(width=10)
        fps_entry.insert(0, "30")
        fps_entry.grid(row=1, column=4, sticky="w")
        # Save button
        tk.Button(text="Save Settings", command=save_settings).grid(row=3, column=3, sticky="w")
    def select_video_path():
        video_path = filedialog.askdirectory()
        if video_path:
            video_path_var.set(video_path)
            video_path_entry.bind("<FocusOut>", lambda event: update_video_path())  
            # Update the settings file with the new values
        with open('webcam_settings.txt', 'w') as f:
            f.write(video_filename_entry.get() + '\n')
            f.write(video_path_entry.get() + '\n')
    def select_image_path():
        image_path = filedialog.askdirectory()
            # Update the settings file with the new values
        if image_path:
            image_path_var.set(image_path)
            image_path_entry.bind("<FocusOut>", lambda event: update_image_path())
        # Update the settings file with the new values
        with open("webcam_settings.txt", "a") as f:
            f.write(f"image_path={image_path}\n")
        with open('webcam_settings.txt', 'w') as f:
            f.write(image_filename_entry.get() + '\n')
            f.write(image_path_entry.get() + '\n')
            # Bind update functions to entry widgets
            image_path_entry.bind("<FocusOut>", lambda event: update_image_path())
        if image_path:
            image_path_var.set(image_path)
            image_path_entry.delete(0, tk.END)
            image_path_entry.insert(0, image_path)
# Search for Connected Webcams                  
    def search_ports():
        # Get connected camera ports
        cam_ports = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cam_ports.append(i)
                cap.release()
        if cam_ports:
            # Update the camera port menu with the connected ports
            camport_menu['menu'].delete(0, 'end')
            for camport in cam_ports:
                # Add each connected port to the menu
                camport_menu['menu'].add_command(label=str(camport), command=lambda p=camport: port_var.set(p))
            # Set the default port to the first connected port
            port_var.set(str(cam_ports[0]))
        else:
            # If no cameras are connected, display an error message
            camport_menu['menu'].delete(0, 'end')
            port_var.set("")
            camport_menu['menu'].add_command(label="No cameras are currently connected")
    def save_settings():
        # Retrieve the values from the entry fields and drop-down menu
        camera_port = port_var.get().strip()
        fps = fps_entry.get().strip()
        video_filename = video_filename_entry.get().strip()
        video_path = video_path_entry.get().strip()
        image_filename = image_filename_entry.get().strip()
        image_path = image_path_entry.get().strip()
        current_settings = (camera_port, fps, video_filename, video_path, image_filename, image_path)
        # Check which settings have been changed and update the current settings
        if camera_port:
            current_settings = (int(camera_port),) + current_settings[1:]
        if fps:
            current_settings = current_settings[:1] + (int(fps),) + current_settings[2:]
        if video_filename:
            video_filename_var.set(video_filename)
        if video_path:
            video_path_var.set(video_path)
        if image_filename:
            image_filename_var.set(image_filename)
        if image_path:
            image_path_var.set(image_path)
        # Write the settings to the configuration file
        with open("webcam_settings.txt", "w") as f:
            f.write(f"video_filename={video_filename_entry.get().strip()}\n")
            f.write(f"video_path={video_path_entry.get().strip()}\n")
            f.write(f"image_filename={image_filename_entry.get().strip()}\n")
            f.write(f"image_path={image_path_entry.get().strip()}\n")
        
    def show_ocr_data_popup(): 
        # Create an instance of OCRDataPopup
        popup = OCRDataPopup(ocr_data = "0")
        # Call the show method of the instance
        popup.show()
       
       
       
# COM Port Settings Menu
    def ComSet(master, serport, baudrate):
        serport = serport
        baudrate = baudrate
        port_label = tk.Label(master, text="Port:")
        port_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        port_entry = tk.Entry(master, width=10)
        port_entry.insert(END, serport)
        port_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        baudrate_label = tk.Label(master, text="Baudrate:")
        baudrate_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        baudrate_entry = tk.Entry(master, width=10)
        baudrate_entry.insert(END, baudrate)
        baudrate_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        return port_entry
    def applyComSet():
        serport = port_entry.get()
        baudrate = baudrate_entry.get()
        try:
            baudrate = int(baudrate)
        except ValueError:
            messagebox.showerror("Error", "Baudrate must be an integer")
            return
        result = (serport, baudrate)        
               



############################################## 
# START SERIAL CONNECTION
############################################## 

serial = None
if serial:
    serial.close()
    serial = None
    serial_button.config(text="Connect")
    terminal.insert(tk.END, "Disconnected from serial port\r\n")
       
############################################## 
# OCR COFIG POP UP WINDOW
############################################## 
class OCRDataPopup(tk.Toplevel):
    def __init__(self, parent, ocr_data):
        super().__init__(parent)
        self.title("OCR Data")
        ocr_data = ocr_data
        # Define the name of the file
        self.filename = 'ocr_data.txt'
        self.file_path = os.path.join(os.getcwd(), self.filename)
        self.value_entry = '0'
            
        # Load the data from the previous save file
        self.file_path = "last_data_settings.txt"
        self.last_data_settings = self.load_data(self.file_path)
        if self.last_data_settings is None:
            self.last_data_settings = "0,0,0,0,0,0"
        self.last_data_settings = self.last_data_settings.strip()
        self.last_data_settings = self.last_data_settings.split(",")
        if len(self.last_data_settings) < 6:
            self.last_data_settings = ["0"] * 6    
            
    def show(self):
        print("Showing OCR Data Popup...")
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", on_closing)
              
        # Create a new frame to hold ocr data widgets
        self.ocrData_frame = tk.Frame(self)
        self.ocrData_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nwe")

        # Create a frame to hold the label and entry frames
        self.set_point_frame = tk.Frame(self.ocrData_frame, borderwidth=1, relief="solid")
        self.set_point_frame.grid(row=0, column=1, padx=(10, 50), pady=5, sticky="nwe")
        # Create a frame for the labels and another for the entries
        self.label_frame = tk.Frame(self.set_point_frame)
        self.entry_frame = tk.Frame(self.set_point_frame)
        # Add the label and entry frames to the main frame
        self.label_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nwe")
        self.entry_frame.grid(row=1, column=0, padx=0, pady=0, sticky="we")
        # Value box
        self.value_label = tk.Label(self.label_frame, text="Set Value:")
        self.value_label.grid(row=0, column=0, padx=(5, 0), pady=0, sticky="w")
        self.value_entry = tk.Entry(self.entry_frame, width=8)
        self.value_entry.grid(row=0, column=0, padx=(5, 0), pady=2, sticky="we")
        # Row Count box & Row Count Repeat Box
        self.row_label = tk.Label(self.label_frame, text="rC")
        self.row_label.grid(row=0, column=1, padx=(5, 0), pady=0, sticky="w")
        self.row_entry.grid(row=0, column=1, padx=(0, 0), pady=2, sticky="we")
        self.rp_label = tk.Label(self.label_frame, text="rP")
        self.rp_label.grid(row=0, column=2, padx=(5, 0), pady=0, sticky="w")
        self.rp_entry = tk.Entry(self.entry_frame, width=4)
        self.rp_entry.grid(row=0, column=2, padx=(0, 0), pady=2, sticky="we")
        # Tolerance box
        self.tolerance_label = tk.Label(self.label_frame, text="Tolerance:")
        self.tolerance_label.grid(row=0, column=3, padx=(0, 0), pady=0, sticky="w")
        self.tolerance_entry = tk.Entry(self.entry_frame, width=8)
        self.tolerance_entry.grid(row=0, column=3, padx=(0, 0), pady=2, sticky="we")
        # Range box
        self.plus_range_label = tk.Label(self.label_frame, text="+")
        self.plus_range_label.grid(row=0, column=4, padx=(0, 15), pady=0, sticky="e")
        self.plus_range_value = tk.IntVar()
        self.plus_range_button = tk.Checkbutton(self.entry_frame, variable=self.plus_range_value)
        self.plus_range_button.grid(row=0, column=4, padx=(0, 15), pady=(0, 5), sticky="e")
        self.minus_range_label = tk.Label(self.label_frame, text="-")
        self.minus_range_label.grid(row=0, column=4, padx=(15, 0), pady=0, sticky="w")
        self.minus_range_value = tk.IntVar()
        self.minus_range_button = tk.Checkbutton(self.entry_frame, variable=self.minus_range_value)
        self.minus_range_button.grid(row=0, column=4, padx=(15, 0), pady=(0, 5), sticky="w")
        
        # Create a new frame to hold export function
        self.export_frame = tk.Frame(self.ocrData_frame)
        self.export_frame.grid(row=0, column=2, padx=(50, 0), pady=(0, 5), sticky="we")
        # Create a new frame for the Save to and Export buttons
        self.buttons_frame = tk.Frame(self.export_frame)
        self.buttons_frame.grid(row=0, column=0, padx=5, pady=0, sticky="w")
        # Export button
        self.export_button = tk.Button(self.buttons_frame, text="Export", command=self.export_callback)
        self.export_button.grid(row=0, column=1, padx=(15, 0), pady=2, sticky="we")
        # Save file path button
        self.save_path_button = tk.Button(self.buttons_frame, text="Save to:", command=self.set_ocrData_path)
        self.save_path_button.grid(row=0, column=0, padx=(0, 15), pady=2, sticky="w")
        # Save file path entry
        self.save_path_entry = tk.Entry(self.export_frame, width=20)
        self.save_path_entry.grid(row=1, column=0, padx=5, pady=0, sticky="we")
        self.protocol("WM_DELETE_WINDOW", on_closing) 
        
        # Create a new frame called csv_frame
        self.csv_frame = tk.Frame(self)
        self.csv_frame.grid(row=3, column=0, padx=5, pady=5, sticky="we")
        # Create a new frame called tree_frame inside csv_frame
        self.tree_frame = tk.Frame(self.csv_frame)
        self.tree_frame.grid(row=0, column=0, padx=5, pady=5, sticky="we")
        # Data entries
        self.tree = ttk.Treeview(self.tree_frame, columns=("Recorded Value", "Tolerance", "Deviation", "Pass/Fail"), show="headings")
        self.tree.grid(row=1, column=0, padx=5, pady=5, sticky="wse")
        self.tree_scrollbar = tk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree_scrollbar.grid(row=1, column=1, padx=(0, 5), pady=5, sticky="ns")
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)
        # Set the headers
        self.tree.heading("#1", text="Recorded Value")
        self.tree.heading("#2", text="Tolerance")
        self.tree.heading("#3", text="Deviation")
        self.tree.heading("#4", text="Pass/Fail")
        # Data Points
        self.tree.column("#1", width=100, anchor="center")
        self.tree.column("#2", width=100, anchor="center")
        self.tree.column("#3", width=100, anchor="center")
        self.tree.column("#4", width=100, anchor="center")
        # Define alternating row colors
        odd_row_color = "#f6f6f6"
        even_row_color = "#ffffff"
        for i in range(10):
            row_color = odd_row_color if i % 2 == 0 else even_row_color
            self.tree.insert('', 'end', values=(" ", " ", " ", " "), tags=("empty",))
            self.tree.tag_configure("empty", background=row_color, foreground=row_color)
        self.tree.grid(row=1, column=0, padx=5, pady=5, sticky="wse")
                    # Load the last data settings if the file exists
        self.last_data_settings_path = "last_data_settings.txt"
        self.last_data_settings = self.load_data(self.last_data_settings_path)
        # Fill in the entry boxes with the last settings
        if self.last_data_settings:
            self.last_data_settings = self.last_data_settings.split(",")
            self.value_entry.insert(0, self.last_data_settings[0])
            self.row_entry.insert(0, self.last_data_settings[1])
            self.rp_entry.insert(0, self.last_data_settings[2])
            self.tolerance_entry.insert(0, self.last_data_settings[3])
            self.plus_range_value.set(int(self.last_data_settings[4]))
            self.minus_range_value.set(int(self.last_data_settings[5]))
            
    def set_ocrData_path(self):
        self.file_path = filedialog.askdirectory()
        self.save_path_entry.delete(0, tk.END)
        self.save_path_entry.insert(0,self.file_path)
        
    def save_data(self, file_path, data):
        with open(file_path, "w") as f:
            for entry in self.entry_frame.winfo_children():
                if isinstance(entry, tk.Entry):
                    value = entry.get()
                    if value.strip() != "":
                        f.write(value + "\n")
                        
    def on_closing(self):
        # Define a list of labels for each field
        labels = ["Value:", "Row Count:", "Repeat Count:", "Tolerance:", "Plus Range:", "Minus Range:"]
        # Define an empty list for changed_lines
        changed_lines = []
        data = ""
        # Get the data from the entry fields
        value = self.value_entry.get()
        row_count = self.row_entry.get()
        repeat_count = self.rp_entry.get()
        tolerance = self.tolerance_entry.get()
        plus_range = self.plus_range_value.get()
        minus_range = self.minus_range_value.get()
        # Loop through each field and add the label and value to the data string
        for i, field in enumerate([value, row_count, repeat_count, tolerance, plus_range, minus_range]):
            # Add the label and value to the data string
            data += labels[i] + " " + str(field) + "\n"

        # Load the data from the previous save file
        file_path = "last_data_settings.txt"
        previous_data = self.load_data(file_path)
        # Check if the data has been changed
        if previous_data:
            previous_lines = previous_data.split("\n")
            if len(previous_lines) >= 1 and value != previous_lines[0]:
                changed_lines.append(value)
            else:
                changed_lines.append(previous_lines[0])
            if len(previous_lines) >= 2 and row_count != previous_lines[1]:
                changed_lines.append(row_count)
            else:
                changed_lines.append(previous_lines[1])
            if len(previous_lines) >= 3 and repeat_count != previous_lines[2]:
                changed_lines.append(repeat_count)
            else:
                changed_lines.append(previous_lines[2])
            if len(previous_lines) >= 4 and tolerance != previous_lines[3]:
                changed_lines.append(tolerance)
            else:
                changed_lines.append(previous_lines[3])
            if len(previous_lines) >= 5 and plus_range != previous_lines[4]:
                changed_lines.append(plus_range)
            else:
                changed_lines.append(previous_lines[4])
            if len(previous_lines) >= 6 and minus_range != previous_lines[5]:
                changed_lines.append(minus_range)
            else:
                changed_lines.append(previous_lines[5])
            # Join the changed_lines list into a string
            data = " ".join(changed_lines)
        else:
            data = f"{value}\n{row_count}\n{repeat_count}\n{tolerance}\n{plus_range}\n{minus_range}"
            
        # Save the changed data to the text file
        self.save_data(self.file_path, data)

        # Destroy the window
        self.destroy()

    def load_data(self, file_path):
        try:
            with open(file_path, "r") as f:
                data = f.read()
                if data:
                    return data.strip()
                else:
                    return ""
        except FileNotFoundError:
            return ""
        
        # Save the contents of the entry boxes, excluding the csv_frame, to a file
    def save_last_data_settings(self):
        last_data_settings = "{},{},{},{},{},{}".format(
            self.value_entry.get(),
            self.row_entry.get(),
            self.rp_entry.get(),
            self.tolerance_entry.get(),
            self.plus_range_value.get(),
            self.minus_range_value.get()
        )
        self.save_data("last_data_settings.txt", last_data_settings)
        
    def export_callback(self):
        # Get the value and tolerance data from the Entry widgets
        value = self.value_entry.get()
        tolerance = self.tolerance_entry.get()
        # Prepare the data for export
        export_data = []
        for entry in self.entry_frame:
            value = entry["data_entry"].get()
            tolerance = entry["tolerance_entry"].get()
            try:
                tolerance = float(tolerance)
            except ValueError:
                tolerance = None
            export_data.append({
                "Pass/Fail": "",
                "Recorded Value": value,
                "Tolerance Deviation": tolerance
            })
        # Create a file dialog to get the file path and name
        self.file_path = filedialog.askdirectory(defaultextension=".csv")
        if not self.file_path:
            return

        # Export the data
        export_data(export_data, self.file_path)
        messagebox.showinfo('Export Complete', 'Data has been exported successfully.')

    def export_data(self, export_data, filepath):
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Pass/Fail', 'Recorded Value', 'Tolerance Deviation'])
            for row in export_data:
                writer.writerow([row['Pass/Fail'], row['Recorded Value'], row['Tolerance Deviation']])
        messagebox.showinfo('Export Complete', 'Data has been exported successfully.')
         
      
                            
# Webcam Settings pop up Window        

# Command List Popup Window             
class CommandListPopup(tk.Toplevel):
    def __init__(self, parent, program_box):
        super().__init__(parent)
        self.title("Command List")
        self.geometry("600x600")
        self.resizable(True, True)
        self.program_box = program_box
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
        self.context_menu.add_command(label="Copy format", command=self.copy_format)
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
        for command, data in command_list.items():
            format = data.get("format", "N/A")
            description = data.get("description", "N/A")
            if self.search_var.get().lower() in command.lower() or self.search_var.get().lower() in format.lower() or self.search_var.get().lower() in description.lower():
                self.treeview.insert("", "end", text=command, values=(format, description))
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
        program_box = self.parent.program_box
        # Replace selected text if there is any
        if program_box.tag_ranges("sel"):
            start, end = self.program_box.tag_ranges("sel")
            program_box.delete(start, end)
            program_box.insert(start, f"{command}")
        else:
            # Find the next empty line in the text box and paste the command there
            line_number = 1
            while True:
                if not self.program_box.get(f"{line_number}.0", f"{line_number}.end"):
                    self.program_box.insert(f"{line_number}.0", f"{command}\n")
                    break
                line_number += 1
        self.context_menu.add_command(label="Paste Command", command=self.paste_command)
    # Right Click to Copy Command or Description
    def copy_command(self):
        selected_item = self.treeview.selection()[0]
        command = self.treeview.item(selected_item, "text")
        self.clipboard_clear()
        self.clipboard_append(command)
    def copy_format(self):
        selection = self.treeview.selection()
        if selection:
            format = self.treeview.item(selection, "values")[2]
            self.clipboard_append(format)
            

class TextRedirector:
    def __init__(self, appOut, original_stdout):
        self.text_widget = appOut
        self.original_stdout = original_stdout
    def write(self, string):
        # Print the output to the IDE terminal
        self.original_stdout.write(string)
        if not string.strip():
            return
        self.text_widget.config(state="normal")
        # Move to the new line if the last character is not a newline
        if self.text_widget.get("end-2c") != "\n":
            self.text_widget.insert(tk.END, "\n")
        # Add a red "msg:" to the message
        self.text_widget.insert(tk.END, "msg: ", "red")
        self.text_widget.tag_config("red", foreground="red")
        # Split the string into lines
        lines = string.splitlines()
        for i, line in enumerate(lines):
            if i != 0:
                self.text_widget.insert(tk.END, "\n")
            self.text_widget.insert(tk.END, line)
            # Get the current line and column
            _, current_col = map(int, self.text_widget.index(tk.END).split('.'))
            # Calculate the remaining space in the line
            remaining_space = 20 - (current_col - 1) - len("msg: ")
            # Add the separator if there is remaining space, limit to remaining_space characters
            if remaining_space > 0:
                separator = "-" * remaining_space
                self.text_widget.insert(tk.END, f"{separator}")
        # Update idletasks to make sure the text widget is updated
        self.text_widget.update_idletasks()
        # Calculate the total number of lines in the text widget
        total_lines = int(self.text_widget.index(tk.END).split('.')[0]) - 2
        # Scroll to the bottom of the text widget
        self.text_widget.yview_moveto(float(total_lines) / float(total_lines + 1))
        self.text_widget.config(state="disabled")
    def flush(self):
        pass


class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder='', color='grey', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.clear_placeholder)
        self.bind("<FocusOut>", self.set_placeholder)
        self.set_placeholder()

    def clear_placeholder(self, event):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def set_placeholder(self, event=None):
        if not self.get():
            self.insert('0', self.placeholder)
            self['fg'] = self.placeholder_color



sys.stdout = TextRedirector(app.appOut, app.original_stdout)  # Redirect the standard output
app.mainloop()
    
