import tkinter as tk
from os import write
from tkinter import ttk, messagebox
from tkinter import messagebox as mb

class Application:
    def __init__(self, root):
        self.root = root
        self.root.geometry("250x150")
        self.root.resizable(False, False)
        self.root.title("Password manager")
        self.root.attributes("-topmost", True)

        self.create_login_ui()

    def create_login_ui(self):
        self.label1 = tk.Label(self.root, text="Username")
        self.label2 = tk.Label(self.root, text="Password")
        self.entry1_var = tk.StringVar()
        self.entry2_var = tk.StringVar()
        self.entry1 = ttk.Entry(self.root, textvariable=self.entry1_var)
        self.entry2 = ttk.Entry(self.root, textvariable=self.entry2_var, show="*")
        self.btn = ttk.Button(self.root, text="Login", command=self.verify)
        self.label_res = tk.Label(self.root, text="")

        self.label1.pack()
        self.entry1.pack()
        self.label2.pack()
        self.entry2.pack()
        self.btn.pack()
        self.label_res.pack()

    def verify(self):
        var1 = self.entry1_var.get()
        var2 = self.entry2_var.get()

        if var1 == "log" and var2 == "in":
            self.clear_login_ui()
            self.create_main_ui()
        else:
            self.label_res.config(text="Invalid username or password")

    def clear_login_ui(self):
        self.label1.destroy()
        self.entry1.destroy()
        self.label2.destroy()
        self.entry2.destroy()
        self.btn.destroy()
        self.label_res.destroy()

    def create_main_ui(self):
        self.root.geometry("700x400")

        self.ui_frame = tk.Frame(self.root, bg="gray")
        self.ui_frame.pack(side="top", fill="both", expand=True)

        self.side_frame = tk.Frame(self.ui_frame, width=100, bg="gray")
        self.side_frame.pack(side="left", fill="y")
        self.side_frame.pack_propagate(False)

        self.main_frame = tk.Frame(self.ui_frame, width=600)
        self.main_frame.pack(side="right", fill="both", expand=True)
        self.main_frame.pack_propagate(False)

        self.add_btn = ttk.Button(self.side_frame, text="Add", command=self.create_add_ui, state="active")
        self.add_btn.pack(side="bottom", pady=10)

        try:
            with open("data", "r") as self.passwd_file:
                self.lines = self.passwd_file.readlines()

            for line in self.lines:
                tk.Label(self.main_frame, text=line.strip()).pack(pady=10, padx=10)
        except FileNotFoundError:
            tk.Label(self.main_frame, text="No saved passwords.").pack()

    def submit_func(self, v1, v2, v3):

        if v1 == "" or v2 == "" or v3 == "":
            mb.showerror("Error", "Please enter both values")
        else:
            with open("data", "a") as passwd_file:
                passwd_file.write(f"{v1} {v2} {v3}\n")

        self.add_frame.destroy()

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        with open("data", "r") as passwd_file:
            self.lines = passwd_file.readlines()

        for line in self.lines:
            tk.Label(self.main_frame, text=line.strip()).pack(padx=10, pady=5)

        self.side_frame.config(width=100)
        self.main_frame.config(width=600)

        self.add_btn.config(state="active")

    def create_add_ui(self):
        self.add_frame = tk.Frame(self.root)
        self.add_frame.pack(side="bottom", fill="both", pady=5, padx=5)

        add_var1 = tk.StringVar()
        add_var2 = tk.StringVar()
        add_var3 = tk.StringVar()

        self.name_label = tk.Label(self.add_frame, text="name").grid(row=0, column=0)
        self.username_label = tk.Label(self.add_frame, text="username").grid(row=1, column=0)
        self.password_label = tk.Label(self.add_frame, text="password").grid(row=2, column=0)

        self.add_name = ttk.Entry(self.add_frame, textvariable=add_var1, width=65).grid(row=0, column=1)
        self.add_username = ttk.Entry(self.add_frame, textvariable=add_var2, width=65).grid(row=1, column=1)
        self.add_password = ttk.Entry(self.add_frame, textvariable=add_var3, width=65).grid(row=2, column=1)

        submit_btn = ttk.Button(self.add_frame, text="Submit", command=lambda: self.submit_func(add_var1.get(), add_var2.get(), add_var3.get()))
        submit_btn.grid(row=3, column=1, pady=10)

        self.add_btn.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
