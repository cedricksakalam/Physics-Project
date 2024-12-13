import tkinter as tk
from tkinter import ttk

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Physics Solver")
        self.geometry("1920x1080")
        self.config(bg="#F0F0F0")  # Light gray background
        self.state('zoomed')  # Start window maximized
        self.create_widgets()

    def create_widgets(self):
        """This function is responsible for setting up all UI components."""
        # Header label for "Solve Physics Problems"
        self.label = tk.Label(self, text="Solve Physics Problems", font=("Helvetica", 48, "bold"), fg="#3E6D99")
        self.label.place(relx=0.5, rely=0.1, anchor="center")  # Center the header label

        # Frame for boxes, centered in the window
        self.box_frame = ttk.Frame(self, padding=20, relief="flat", style="TFrame")
        self.box_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Grid configuration for 3 boxes (equal width)
        for i in range(3):
            self.box_frame.grid_columnconfigure(i, weight=1, uniform="equal")
        
        self.create_boxes()

    def setup_button_style(self):
        """Define the style of the buttons."""
        style = ttk.Style(self)
        style.configure("TButton",
                        background="#4A90E2",  # Soft blue button background
                        foreground="white",     # White text color
                        relief="flat",          # Flat buttons (no 3D effect)
                        padding=(10, 10),       # Adjust padding for a nicer button size
                        font=("Helvetica", 12), # Modern font
                        width=20)               # Fixed width for buttons
        # Add hover effect for buttons
        style.map("TButton",
                  background=[("active", "#357ABD"), ("pressed", "#357ABD")],
                  foreground=[("active", "white"), ("pressed", "white")]
        )

    def create_boxes(self):
        """Create boxes with descriptions and buttons."""
        box_data = [
            ("Solve for Mechanics", self.solve_mechanics),
            ("Solve for Sound Waves", self.solve_Waves),
            ("Solving Electricity", self.solve_electricity)
        ]

        # Create boxes and their buttons
        for index, (description_text, button_command) in enumerate(box_data):
            self.create_box(index, description_text, button_command)

    def create_box(self, index, description_text, button_command):
        """Create a box with description and button inside."""
        box = ttk.Frame(self.box_frame, padding=10, relief="solid", style="TFrame")
        box.grid(row=0, column=index, padx=20, pady=20, sticky="nsew")  # Grid positioning

        description = tk.Label(box, text=description_text, font=("Helvetica", 14, "bold"), wraplength=250, anchor="center", justify="center")
        description.pack(pady=20)

        button = ttk.Button(box, text="Go", command=button_command, style="TButton")
        button.pack(pady=10)

    def solve_mechanics(self):
        from mechanics import MechanicsCalculator
        self.withdraw()  # Hide the main window
        self.mechanics = MechanicsCalculator(self)  # Pass the main window as parent
        self.mechanics.grab_set()  # Block interaction with the main window until this window is closed

    def solve_Waves(self):
        from Waves import SoundWaveCalculator
        self.withdraw()  # Hide the main window
        self.waves = SoundWaveCalculator(self)  # Pass the main window as parent
        self.waves.grab_set()  # Block interaction with the main window until this window is closed

    def solve_electricity(self):
        from Electricity import ElectricityCalculator
        self.withdraw()  # Hide the main window
        self.electricity = ElectricityCalculator(self)  # Pass the main window as parent
        self.electricity.grab_set()  # Block interaction with the main window until this window is closed

if __name__ == "__main__":
    app = Main()
    app.mainloop()