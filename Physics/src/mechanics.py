import tkinter as tk
from tkinter import ttk, messagebox
from mecha import Mechanics

class MechanicsCalculator:
    def __init__(self, root):
        self.mechanics = Mechanics()
        self.root = root
        self.root.title("Mechanics Calculator")
        self.root.iconbitmap("C:/Users/ced/Physics Project/Physics/src/Icon.ico")
        
        # Define the style for ttk widgets
        style = ttk.Style()
        style.configure("TFrame", background="#1d2b36")
        style.configure("TCombobox", font=("Arial", 16), padding=5)
        style.configure("TButton", font=("Arial", 16), padding=10, width=15)
        style.configure("TLabel", background="#1d2b36", foreground="#ffffff")

        self.root.config(bg="#1d2b36")  # Background color for the root window
        self.root.state('zoomed')
        self.root.resizable(False, False)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Main frame with the applied style
        self.main_frame = ttk.Frame(root, style="TFrame")
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.main_frame.grid_rowconfigure(0, weight=0)  
        self.main_frame.grid_rowconfigure(1, weight=0)  
        self.main_frame.grid_rowconfigure(2, weight=0)  
        self.main_frame.grid_rowconfigure(3, weight=1) 
        self.main_frame.grid_rowconfigure(4, weight=0)  
        self.main_frame.grid_columnconfigure(0, weight=1)  

        self.title_label = ttk.Label(
            self.main_frame,
            text="Solving Mechanics",
            font=("Impact", 60, "bold"),
            anchor="center",
            style="TLabel"
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(50, 20), sticky="n")

        self.description_label = ttk.Label(
            self.main_frame,
            text="Focuses on the motion of objects and the forces that affect them. It includes concepts such as \nNewton's laws, kinematics, dynamics, and statics, applicable in understanding the physical behavior of systems.",
            font=("Arial", 20),
            anchor="center",
            justify="center",
            style="TLabel"
        )
        self.description_label.grid(row=1, column=0, columnspan=2, pady=(100, 10), sticky="n")

        self.operation_label = ttk.Label(self.main_frame, text="Select Operation:", font=("Arial", 15, "bold"), style="TLabel")
        self.operation_label.grid(row=2, column=0, padx=20, pady=20, sticky="w")
        
        self.operations = {
            "Velocity": (self.calculate_velocity, ["initial_velocity", "acceleration", "time"], "v = u + at", "m/s"),
            "Displacement": (self.calculate_displacement, ["initial_velocity", "acceleration", "time"], "s = ut + 1/2 * a * t^2", "m"),
            "Acceleration": (self.calculate_acceleration, ["final_velocity", "initial_velocity", "time"], "a = (v - u) / t", "m/s²"),
            "Force": (self.calculate_force, ["mass", "acceleration"], "F = m * a", "N"),
            "Work": (self.calculate_work, ["force", "displacement", "angle"], "W = F * d * cos(θ)", "J"),
            "Kinetic Energy": (self.calculate_kinetic_energy, ["mass", "velocity"], "KE = 1/2 * m * v^2", "J"),
            "Power": (self.calculate_power, ["work", "time"], "P = W / t", "W"),
            "Momentum": (self.calculate_momentum, ["mass", "velocity"], "p = m * v", "kg·m/s"),
            "Impulse": (self.calculate_impulse, ["force", "time"], "I = F * t", "N·s"),
            "Circular Velocity": (self.calculate_circular_velocity, ["radius", "period"], "v = 2 * π * r / T", "m/s")
        }

        self.operation_var = tk.StringVar()
        self.operation_menu = ttk.Combobox(
            self.main_frame,
            textvariable=self.operation_var,
            values=list(self.operations.keys()),
            state="readonly",
            height=9,
            width=30,
            font=("Arial", 18),
            style="TCombobox", 
        )
        self.operation_menu.grid(row=2, column=0,padx=200, pady=20, sticky="w")  # Keep dropdown on the right side
        self.operation_menu.bind("<<ComboboxSelected>>", self.update_input_fields)

        self.input_frame = tk.Frame(self.main_frame, bg="#1d2b36")  # Changed to tk.Frame
        self.input_frame.grid(row=3, column=0, padx=200, pady=10, sticky="nsew")
        self.input_frame.grid_propagate(False) 
        self.inputs = {}
        self.create_input_fields()
        
        self.formula_label = ttk.Label(self.input_frame, text="", font=("Arial", 14), justify="center", style="TLabel")
        self.formula_label.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="nsew")

        self.output_label = ttk.Label(self.input_frame, text="Result: ", font=("Arial", 18), anchor="center", style="TLabel")
        self.output_label.grid(row=len(self.inputs) + 3, column=1, padx=10, pady=10, sticky="nsew")
        self.output_label.grid_remove() 

        self.calculate_button = ttk.Button(self.input_frame, text="Calculate", command=self.calculate, style="TButton")
        self.calculate_button.grid(row=len(self.inputs) + 4, column=1, pady=10, sticky="nsew")
        self.calculate_button.grid_remove() 

        self.back_button = ttk.Button(self.main_frame, text="Back", command=self.back, style="TButton")
        self.back_button.grid(row=4, column=0, columnspan=2, pady=20, sticky="nsew")

    def create_input_fields(self):
        fields = [
            ("initial_velocity", "m/s"), ("acceleration", "m/s²"), ("time", "s"), ("final_velocity", "m/s"),
            ("mass", "kg"), ("velocity", "m/s"), ("force", "N"), ("displacement", "m"), ("angle", "°"), 
            ("work", "J"), ("radius", "m"), ("period", "s")
        ]

        for idx, (field, unit) in enumerate(fields):
            label = ttk.Label(self.input_frame, font=("Arial", 15), text=f"{field.replace('_', ' ').capitalize()}:", style="TLabel")
            entry = ttk.Entry(self.input_frame, font=("Arial", 15))
            unit_label = ttk.Label(self.input_frame, font=("Arial", 15), text=unit, style="TLabel")

            # Adding unit label in the second column to align with input fields
            label.grid(row=idx + 1, column=0, sticky="ew", padx=10, pady=5)
            entry.grid(row=idx + 1, column=1, sticky="ew", padx=10, pady=5)
            unit_label.grid(row=idx + 1, column=2, sticky="w", padx=10, pady=5)

            self.input_frame.grid_columnconfigure(0, weight=1)
            self.input_frame.grid_columnconfigure(1, weight=3)

            self.inputs[field] = (label, entry, unit_label)
            label.grid_remove()
            entry.grid_remove()
            unit_label.grid_remove()

    def update_input_fields(self, event=None):
        """Update input fields based on selected operation."""
        # Hide all inputs initially
        for label, entry, unit_label in self.inputs.values():
            label.grid_remove()
            entry.grid_remove()
            unit_label.grid_remove()

        operation = self.operation_var.get()  # Get selected operation
        if operation in self.operations:
            # Retrieve operation details
            func, required_fields, formula, unit = self.operations[operation]

            # Display formula
            self.formula_label.config(text=f"Formula: {formula}")
            self.formula_label.grid()

            # Show required input fields
            for idx, field in enumerate(required_fields):
                if field in self.inputs:
                    label, entry, unit_label = self.inputs[field]
                    label.grid(row=idx + 1, column=0, sticky="w", padx=5, pady=5)
                    entry.grid(row=idx + 1, column=1, padx=5, pady=5, sticky="ew")
                    unit_label.grid(row=idx + 1, column=2, sticky="w", padx=10, pady=5)

            # Show calculate button
            self.calculate_button.grid(row=len(required_fields) + 2, column=1, pady=10, sticky="nsew")
            self.output_label.grid_remove()
        else:
            # Hide formula and calculate button if no operation is selected
            self.formula_label.config(text="")
            self.formula_label.grid_remove()
            self.calculate_button.grid_remove()  

    def calculate(self):
        """Perform the selected operation and display the result."""
        try:
            # Retrieve selected operation
            operation = self.operation_var.get()
            if not operation:
                raise ValueError("No operation selected.")

            func, required_fields, formula, unit = self.operations[operation]

            # Set input values into Mechanics instance
            for field in required_fields:
                label, entry, _ = self.inputs[field]
                value = entry.get()
                if value.strip() == "":
                    raise ValueError(f"Please enter a value for {field.replace('_', ' ').capitalize()}")
                setattr(self.mechanics, field, float(value))

            # Perform calculation
            result = func()

            # Display result
            self.output_label.config(text=f"Result: {result:.4f} {unit}")
            self.output_label.grid()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
            
    def back(self):
        self.root.destroy()

    def calculate_velocity(self):
        return self.mechanics.calculate_velocity()

    def calculate_displacement(self):
        return self.mechanics.calculate_displacement()

    def calculate_acceleration(self):
        return self.mechanics.calculate_acceleration()

    def calculate_force(self):
        return self.mechanics.calculate_force()

    def calculate_work(self):
        return self.mechanics.calculate_work()

    def calculate_kinetic_energy(self):
        return self.mechanics.calculate_kinetic_energy()

    def calculate_power(self):
        return self.mechanics.calculate_power()

    def calculate_momentum(self):
        return self.mechanics.calculate_momentum()

    def calculate_impulse(self):
        return self.mechanics.calculate_impulse()

    def calculate_circular_velocity(self):
        return self.mechanics.calculate_circular_velocity()

if __name__ == "__main__":
    root = tk.Tk()
    app = MechanicsCalculator(root)
    root.mainloop()
