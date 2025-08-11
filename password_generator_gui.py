import tkinter as tk
from tkinter import messagebox
import string
import secrets
import math


try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False



def shuffled_join(chars):
    chars = list(chars)
    secrets.SystemRandom().shuffle(chars)
    return ''.join(chars)

def choose_random(pool, n=1):
    return [secrets.choice(pool) for _ in range(n)]

def estimate_entropy(length, pool_size):
    if pool_size <= 0 or length <= 0:
        return 0.0
    return length * math.log2(pool_size)

def strength_label(entropy_bits):
    if entropy_bits < 28:
        return "Very Weak"
    if entropy_bits < 36:
        return "Weak"
    if entropy_bits < 60:
        return "Moderate"
    if entropy_bits < 128:
        return "Strong"
    return "Very Strong"

def generate_password(length, use_upper, use_lower, use_digits, use_symbols,
                      min_upper=0, min_lower=0, min_digits=0, min_symbols=0):
    categories = {}
    if use_upper:
        categories['upper'] = string.ascii_uppercase
    if use_lower:
        categories['lower'] = string.ascii_lowercase
    if use_digits:
        categories['digits'] = string.digits
    if use_symbols:
        categories['symbols'] = "!@#$%^&*()-_=+[]{};:,.<>?/|"

    all_pool = ''.join(categories.values())
    if not all_pool:
        raise ValueError("No character sets selected.")

    min_map = {
        'upper': min_upper,
        'lower': min_lower,
        'digits': min_digits,
        'symbols': min_symbols
    }
    for cat in list(min_map.keys()):
        if cat not in categories:
            if min_map[cat] > 0:
                raise ValueError(f"Min for '{cat}' set but that set is disabled.")
            min_map.pop(cat, None)

    total_min = sum(min_map.values())
    if total_min > length:
        raise ValueError("Minimum requirements exceed password length.")

    chosen = []
    for cat, mn in min_map.items():
        if mn > 0:
            chosen += choose_random(categories[cat], mn)

    remaining = length - len(chosen)
    if remaining > 0:
        chosen += choose_random(all_pool, remaining)

    return shuffled_join(chosen), len(all_pool)


# -------- GUI Application --------
class PasswordGeneratorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Secure Password Generator")
        master.geometry("450x500")
        master.resizable(False, False)
        master.configure(bg="#1e1e2f")

        # Title
        title = tk.Label(master, text="🔐 Password Generator", font=("Arial", 18, "bold"), bg="#1e1e2f", fg="white")
        title.pack(pady=10)

        # Length slider
        tk.Label(master, text="Password Length:", bg="#1e1e2f", fg="white").pack()
        self.length_var = tk.IntVar(value=16)
        length_slider = tk.Scale(master, from_=6, to=64, orient="horizontal", variable=self.length_var,
                                 bg="#1e1e2f", fg="white", troughcolor="#333", highlightthickness=0)
        length_slider.pack(pady=5)

        # Checkboxes for char sets
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        for text, var in [("Uppercase", self.use_upper), ("Lowercase", self.use_lower),
                          ("Digits", self.use_digits), ("Symbols", self.use_symbols)]:
            tk.Checkbutton(master, text=text, variable=var, bg="#1e1e2f", fg="white", selectcolor="#333").pack(anchor="w", padx=50)

        # Generate Button
        gen_btn = tk.Button(master, text="Generate Password", command=self.generate, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        gen_btn.pack(pady=15)

        # Output
        self.password_entry = tk.Entry(master, font=("Consolas", 14), justify="center", width=35)
        self.password_entry.pack(pady=5)

        # Strength label
        self.strength_label = tk.Label(master, text="", bg="#1e1e2f", fg="white", font=("Arial", 12))
        self.strength_label.pack(pady=5)

        # Copy button
        copy_btn = tk.Button(master, text="Copy to Clipboard", command=self.copy_password, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
        copy_btn.pack(pady=10)

    def generate(self):
        try:
            password, pool_size = generate_password(
                length=self.length_var.get(),
                use_upper=self.use_upper.get(),
                use_lower=self.use_lower.get(),
                use_digits=self.use_digits.get(),
                use_symbols=self.use_symbols.get()
            )
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)

            ent = estimate_entropy(len(password), pool_size)
            self.strength_label.config(text=f"Entropy: {ent:.1f} bits → {strength_label(ent)}")

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def copy_password(self):
        pw = self.password_entry.get()
        if not pw:
            messagebox.showwarning("Warning", "No password to copy!")
            return
        if HAS_PYPERCLIP:
            pyperclip.copy(pw)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        else:
            self.master.clipboard_clear()
            self.master.clipboard_append(pw)
            messagebox.showinfo("Copied", "Password copied to clipboard!")



if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()
