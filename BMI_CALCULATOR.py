import tkinter as tk
from tkinter import ttk, messagebox

def calculate_bmi():
    try:
        weight = float(weight_entry.get())
        if weight <= 0:
            raise ValueError("Weight must be positive!")

        height_unit = height_combobox.get()
        if height_unit == "Centimeters (cm)":
            height_cm = float(height_entry.get())
            if height_cm <= 0:
                raise ValueError("Height must be positive!")
            height_m = height_cm / 100
        elif height_unit == "Meters (m)":
            height_m = float(height_entry.get())
            if height_m <= 0:
                raise ValueError("Height must be positive!")
        elif height_unit == "Feet/Inches":
            feet = float(feet_entry.get())
            inches = float(inches_entry.get())
            if feet <= 0 or inches < 0:
                raise ValueError("Height must be positive!")
            height_m = (feet * 12 + inches) * 0.0254
        else:
            raise ValueError("Invalid height unit!")

        bmi = weight / (height_m ** 2)
        category = classify_bmi(bmi)
        
        result_label.config(text=f"BMI: {bmi:.1f}", fg="#4CAF50")
        category_label.config(text=f"Category: {category}", fg="#FFD700")

    except ValueError as e:
        messagebox.showerror("Error", str(e))

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def update_height_entries(event):
    unit = height_combobox.get()
    if unit == "Feet/Inches":
        height_entry.grid_remove()
        feet_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        inches_entry.grid(row=3, column=2, padx=5, pady=5, sticky="ew")
        height_label.config(text="Height:")
    else:
        feet_entry.grid_remove()
        inches_entry.grid_remove()
        height_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew", columnspan=2)
        height_label.config(text=f"Height ({'m' if unit == 'Meters (m)' else 'cm'}):")

root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("800x600")
root.state('zoomed')  

bg_color = "#1e1e1e"
box_bg = "#252525"
fg_color = "#ffffff"
entry_bg = "#2d2d2d"
button_bg = "#3e3e3e"
button_active = "#4e4e4e"
accent_green = "#4CAF50"
accent_gold = "#FFD700"

style = ttk.Style()
style.theme_use("clam")
style.configure("TCombobox", fieldbackground=entry_bg, background=entry_bg, foreground=fg_color)
style.configure("TFrame", background=bg_color)

main_container = tk.Frame(root, bg=bg_color)
main_container.pack(expand=True, fill=tk.BOTH)

calc_frame = tk.Frame(main_container, bg=box_bg, bd=2, relief=tk.RIDGE, padx=20, pady=20)
calc_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

title_label = tk.Label(
    calc_frame,
    text="BMI Calculator",
    font=("Arial", 24, "bold"),
    bg=box_bg,
    fg=accent_green
)
title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

weight_label = tk.Label(
    calc_frame,
    text="Weight (kg):",
    font=("Arial", 12),
    bg=box_bg,
    fg=fg_color
)
weight_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)

weight_entry = tk.Entry(
    calc_frame,
    font=("Arial", 12),
    bg=entry_bg,
    fg=fg_color,
    insertbackground=fg_color,
    relief=tk.FLAT
)
weight_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

height_unit_label = tk.Label(
    calc_frame,
    text="Height Unit:",
    font=("Arial", 12),
    bg=box_bg,
    fg=fg_color
)
height_unit_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)

height_combobox = ttk.Combobox(
    calc_frame,
    values=["Centimeters (cm)", "Meters (m)", "Feet/Inches"],
    font=("Arial", 12),
    state="readonly"
)
height_combobox.set("Centimeters (cm)")
height_combobox.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
height_combobox.bind("<<ComboboxSelected>>", update_height_entries)

height_label = tk.Label(
    calc_frame,
    text="Height (cm):",
    font=("Arial", 12),
    bg=box_bg,
    fg=fg_color
)
height_label.grid(row=3, column=0, sticky="w", padx=5, pady=5)

height_entry = tk.Entry(
    calc_frame,
    font=("Arial", 12),
    bg=entry_bg,
    fg=fg_color,
    insertbackground=fg_color,
    relief=tk.FLAT
)
height_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

feet_entry = tk.Entry(
    calc_frame,
    font=("Arial", 12),
    bg=entry_bg,
    fg=fg_color,
    insertbackground=fg_color,
    relief=tk.FLAT
)
feet_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
feet_entry.grid_remove()

inches_entry = tk.Entry(
    calc_frame,
    font=("Arial", 12),
    bg=entry_bg,
    fg=fg_color,
    insertbackground=fg_color,
    relief=tk.FLAT
)
inches_entry.grid(row=3, column=2, padx=5, pady=5, sticky="ew")
inches_entry.grid_remove()

calculate_button = tk.Button(
    calc_frame,
    text="Calculate BMI",
    font=("Arial", 12, "bold"),
    bg=button_bg,
    fg=fg_color,
    activebackground=button_active,
    activeforeground=fg_color,
    relief=tk.FLAT,
    command=calculate_bmi
)
calculate_button.grid(row=4, column=0, columnspan=3, pady=20, sticky="ew")


result_frame = tk.Frame(calc_frame, bg=box_bg)
result_frame.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")

result_label = tk.Label(
    result_frame,
    text="BMI: -",
    font=("Arial", 14, "bold"),
    bg=box_bg,
    fg=accent_green
)
result_label.pack()

category_label = tk.Label(
    result_frame,
    text="Category: -",
    font=("Arial", 14),
    bg=box_bg,
    fg=accent_gold
)
category_label.pack()



root.mainloop()