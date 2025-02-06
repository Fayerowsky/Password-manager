import tkinter as tk
from tkinter import ttk

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

        self.ui_frame = tk.Frame(self.root)
        self.side_frame = tk.Frame(self.ui_frame, width=100, bg="red")
        self.main_frame = tk.Frame(self.ui_frame, width=600, bg="pink")

        self.ui_frame.pack(side="top", fill="both", expand=True)
        self.side_frame.pack(side="left", fill="both", expand=True)
        self.main_frame.pack(side="right", fill="both", expand=True)

        self.add_btn = tk.Button(self.side_frame, text="Add", command=self.create_add_ui)
        self.add_btn.pack(side="bottom", pady=10)

    def submit_func(self, v1, v2, v3):
        label = tk.Label(self.main_frame, text=v1 + v2 + v3)
        label.pack()

    def create_add_ui(self):
        self.add_frame = tk.Frame(self.root, bg="green")
        self.add_frame.pack(side="bottom", fill="both", pady=5, padx=5)

        add_var1 = tk.StringVar()
        add_var2 = tk.StringVar()
        add_var3 = tk.StringVar()

        self.name_label = tk.Label(self.add_frame, text="name").grid(row=0, column=0)
        self.username_label = tk.Label(self.add_frame, text="username").grid(row=1, column=0)
        self.password_label = tk.Label(self.add_frame, text="password").grid(row=2, column=0)

        self.add_name = tk.Entry(self.add_frame, textvariable=add_var1, width=65).grid(row=0, column=1)
        self.add_username = tk.Entry(self.add_frame, textvariable=add_var2, width=65).grid(row=1, column=1)
        self.add_password = tk.Entry(self.add_frame, textvariable=add_var3, width=65).grid(row=2, column=1)

        submit_btn = tk.Button(self.add_frame, text="Submit", command=lambda: self.submit_func(add_var1.get(), add_var2.get(), add_var3.get()))
        submit_btn.grid(row=3, column=1, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()