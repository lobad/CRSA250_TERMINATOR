import tkinter as tk
import serial

class SerialMonitor:
    def __init__(self, port, baudrate):
        self.serial = serial.Serial(port=port, baudrate=baudrate)

    def read_serial(self):
        while True:
            line = self.serial.readline()
            if line:
                print(line.decode('utf-8').strip())
                
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()
        

    def create_widgets(self):
        # Create the terminal window
        self.terminal = tk.Text(self, height=10, width=50)
        self.terminal.grid(row=0, column=1, columnspan=6, padx=10, pady=10)
        
        # Create serial port settings widgets
        serial_settings_frame = tk.Frame(self.master)
        serial_settings_frame.pack(side=tk.TOP, padx=5, pady=5)

        tk.Label(serial_settings_frame, text='Serial Port').grid(row=0, column=0)
        tk.Entry(serial_settings_frame, textvariable=self.port_var).grid(row=0, column=1)

        tk.Label(serial_settings_frame, text='Baudrate').grid(row=1, column=0)
        tk.Entry(serial_settings_frame, textvariable=self.baudrate_var).grid(row=1, column=1)

        tk.Button(serial_settings_frame, text='Connect', command=self.connect_serial).grid(row=0, column=2, rowspan=2, padx=5)
        
        # Create the options menu
        self.options_menu = tk.Menu(self.master)
        self.master.config(menu=self.options_menu)

        # Create the "Save" and "Load" options in the menu
        self.file_menu = tk.Menu(self.options_menu)
        self.options_menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save")
        self.file_menu.add_command(label="Load")

        # Create the buttons for HOME, MANUAL, and AUTO
        self.home_button = tk.Button(self, text="HOME")
        self.home_button.grid(row=1, column=0)
        self.manual_button = tk.Button(self, text="MANUAL")
        self.manual_button.grid(row=1, column=1)
        self.auto_button = tk.Button(self, text="AUTO")
        self.auto_button.grid(row=1, column=2)

        # Create the buttons for WAIST, SHOULDER, ELBOW, WRIST, TWIST, and HAND
        labels = ["WAIST", "SHOULDER", "ELBOW", "WRIST", "TWIST", "HAND"]
        self.plus_buttons = []
        self.minus_buttons = []
        for i, label in enumerate(labels):
            plus_button = tk.Button(self, text="+", width=2)
            plus_button.grid(row=i+2, column=7)
            self.plus_buttons.append(plus_button)
            minus_button = tk.Button(self, text="-", width=2)
            minus_button.grid(row=i+2, column=8)
            self.minus_buttons.append(minus_button)
            label = tk.Label(self, text=label)
            label.grid(row=i+2, column=0)

        # Create the preset programs dropdown menu
        self.preset_menu = tk.Menu(self.options_menu)
        self.options_menu.add_cascade(label="Presets", menu=self.preset_menu)
        self.preset_menu.add_command(label="Preset 1")
        self.preset_menu.add_command(label="Preset 2")

root = tk.Tk()
app = Application(master=root)
app.mainloop()

