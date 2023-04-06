import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("Themed App")
        
        # Your GUI components and methods here

def main():
    # Create a ThemedTk instance outside of the class
    root = ThemedTk()
    
    # Get the list of available themes
    available_themes = root.get_themes()
    
    # Print the list of available themes
    print("Available themes:", available_themes)
    
    # Set a theme from the available themes, replace "selected_theme" with the desired theme name
    selected_theme = "arc"  # For example, you can use the "arc" theme
    root.set_theme(selected_theme)
    
    # Pass the root object to the class constructor
    app = Application(master=root)
    root.mainloop()

if __name__ == "__main__":
    main()