import tkinter as tk
from tkinter import ttk
from generator.core import generate_password, generate_multiple
from generator.strength import calculate_strength

class PasswordGeneratorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Generator")
        self.root.geometry("520x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#0F172A")

        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.password_var = tk.StringVar()
        self.length_var = tk.IntVar(value=16)
        self.exclude_var = tk.StringVar()
        self.strength_var = tk.StringVar(value="Strength: -")

        self._build_ui()

    def _build_ui(self):
        # Title Section
        title_label = tk.Label(self.root, text="Password Generator", font=("Segoe UI", 18, "bold"), fg="#F8FAFC", bg="#0F172A")
        title_label.pack(pady=(10, 2))

        subtitle_label = tk.Label(self.root, text="Cryptographically Secure", font=("Segoe UI", 10), fg="#64748B", bg="#0F172A")
        subtitle_label.pack(pady=(0, 10))

        # Password Output Section
        output_frame = tk.Frame(self.root, bg="#1E293B")
        output_frame.pack(fill="x", padx=20, pady=(0, 10))

        password_entry = tk.Entry(output_frame, textvariable=self.password_var, state="readonly", font=("Segoe UI", 16, "bold"), fg="#38BDF8", bg="#1E293B", readonlybackground="#1E293B", justify="center")
        password_entry.pack(fill="x", pady=10, ipady=5)
        
        copy_btn = tk.Button(output_frame, text="Copy", command=self.copy_to_clipboard, bg="#334155", fg="white", relief="flat", cursor="hand2")
        copy_btn.pack(pady=(0, 10))
        
        strength_lbl = tk.Label(output_frame, textvariable=self.strength_var, font=("Segoe UI", 10), bg="#1E293B", fg="#94A3B8")
        strength_lbl.pack(pady=(0, 10))

        # Settings
        settings_frame = tk.Frame(self.root, bg="#0F172A")
        settings_frame.pack(fill="x", padx=20, pady=10)
        
        # Length
        len_frame = tk.Frame(settings_frame, bg="#0F172A")
        len_frame.pack(fill="x", pady=5)
        tk.Label(len_frame, text="Length:", font=("Segoe UI", 10), bg="#0F172A", fg="white").pack(side="left")
        tk.Label(len_frame, textvariable=self.length_var, font=("Segoe UI", 10), bg="#0F172A", fg="white").pack(side="right")
        length_scale = tk.Scale(settings_frame, from_=4, to=128, orient="horizontal", variable=self.length_var, bg="#0F172A", fg="white", highlightthickness=0)
        length_scale.pack(fill="x")
        
        # Checkboxes
        chk_frame = tk.Frame(settings_frame, bg="#0F172A")
        chk_frame.pack(fill="x", pady=10)
        
        tk.Checkbutton(chk_frame, text="Uppercase", variable=self.uppercase_var, bg="#0F172A", fg="white", selectcolor="#1E293B").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Checkbutton(chk_frame, text="Lowercase", variable=self.lowercase_var, bg="#0F172A", fg="white", selectcolor="#1E293B").grid(row=0, column=1, sticky="w", padx=10, pady=5)
        tk.Checkbutton(chk_frame, text="Numbers", variable=self.digits_var, bg="#0F172A", fg="white", selectcolor="#1E293B").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        tk.Checkbutton(chk_frame, text="Symbols", variable=self.symbols_var, bg="#0F172A", fg="white", selectcolor="#1E293B").grid(row=1, column=1, sticky="w", padx=10, pady=5)

        # Exclude
        exc_frame = tk.Frame(settings_frame, bg="#0F172A")
        exc_frame.pack(fill="x", pady=5)
        tk.Label(exc_frame, text="Exclude Characters:", font=("Segoe UI", 10), bg="#0F172A", fg="white").pack(side="left")
        exc_entry = tk.Entry(exc_frame, textvariable=self.exclude_var, font=("Segoe UI", 10))
        exc_entry.pack(side="right", fill="x", expand=True, padx=(10, 0))

        # Generate Button
        generate_button = tk.Button(self.root, text="Generate Password", command=self.generate, bg="#2563EB", fg="#FFFFFF", font=("Segoe UI", 12, "bold"), pady=10, cursor="hand2", relief="flat")
        generate_button.pack(fill="x", padx=20, pady=20)

    def generate(self):
        try:
            pwd = generate_password(
                self.length_var.get(),
                self.uppercase_var.get(),
                self.lowercase_var.get(),
                self.digits_var.get(),
                self.symbols_var.get(),
                self.exclude_var.get()
            )
            self.password_var.set(pwd)
            
            # calculate strength
            strength_info = calculate_strength(pwd)
            self.strength_var.set(f"Strength: {strength_info['label']} ({strength_info['score']} pts, entropy: {strength_info['entropy']} bits)")
        except ValueError as e:
            from tkinter import messagebox
            messagebox.showerror("Validation Error", str(e))
            self.password_var.set("")
            self.strength_var.set("")
        except Exception as e:
            self.password_var.set("Error: " + str(e))
            self.strength_var.set("")

    def copy_to_clipboard(self):
        import pyperclip
        if self.password_var.get() and not self.password_var.get().startswith("Error"):
            pyperclip.copy(self.password_var.get())

    def run(self):
        self.root.mainloop()
