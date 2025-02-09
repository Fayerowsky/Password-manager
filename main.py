import customtkinter as ctk
from tkinter import messagebox as mb
from PIL import Image


class Application:
    def __init__(self, root):
        self.root = root
        self.root.geometry("250x150")
        self.root.resizable(False, False)
        self.root.title("Password Manager")
        self.root.attributes("-topmost", True)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_login_ui()

        ctk.set_appearance_mode("dark")

    def create_login_ui(self):
        self.label1 = ctk.CTkLabel(self.root, text="Username")
        self.label2 = ctk.CTkLabel(self.root, text="Password")
        self.entry1 = ctk.CTkEntry(self.root)
        self.entry2 = ctk.CTkEntry(self.root, show="*")
        self.btn = ctk.CTkButton(self.root, text="Login", command=self.verify)
        self.label_res = ctk.CTkLabel(self.root, text="")

        self.label1.pack()
        self.entry1.pack()
        self.label2.pack()
        self.entry2.pack()
        self.btn.pack(pady=5)
        self.label_res.pack()

    def verify(self):
        var1 = self.entry1.get()
        var2 = self.entry2.get()

        if var1 == "log" and var2 == "in":
            self.clear_login_ui()
            self.create_main_ui()
        else:
            self.label_res.configure(text="Invalid username or password")

    def clear_login_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_rows(self):

        try:
            with open("data", "r") as self.passwd_file:
                self.lines = self.passwd_file.readlines()

                contents = open("data", "r").read()
                if not contents:
                    ctk.CTkLabel(self.main_frame, text="No saved passwords.").pack()

            for line in self.lines:
                entry_frame = ctk.CTkFrame(self.main_frame, fg_color="#171717", corner_radius=5)
                entry_frame.pack(pady=7, padx=10, fill="x")

                label = ctk.CTkLabel(entry_frame, text=line.strip(), text_color="white", width=500, height=50)
                label.pack(side="left", padx=10, pady=5, expand=True)

                delete_icon = ctk.CTkImage(light_image=Image.open("delete.png"), size=(25, 25))
                delete_btn = ctk.CTkButton(entry_frame, text="", image=delete_icon, width=40, height=40, fg_color="transparent",
                                           command=lambda l=line: self.delete_entry(l))
                delete_btn.pack(side="right", padx=10, pady=5)

        except FileNotFoundError:
            ctk.CTkLabel(self.main_frame, text="No saved passwords.").pack()

    def create_main_ui(self):
        self.root.geometry("700x400")

        self.ui_frame = ctk.CTkFrame(self.root)
        self.ui_frame.pack(side="top", fill="both", expand=True)

        self.side_frame = ctk.CTkFrame(self.ui_frame, width=50)
        self.side_frame.pack(side="left", fill="y", padx=5)
        self.side_frame.pack_propagate(False)

        self.main_frame = ctk.CTkScrollableFrame(self.ui_frame, width=600)
        self.main_frame.pack(side="right", fill="both", expand=True)

        icon_image = ctk.CTkImage(light_image=Image.open("plus.png"), size=(35, 35))
        self.add_btn = ctk.CTkButton(self.side_frame, text="", image=icon_image, width=50, height=50,
                                     command=self.create_add_ui, fg_color="transparent")
        self.add_btn.pack(side="top", pady=10)

        self.create_main_rows()

    def delete_entry(self, line):
        self.lines.remove(line)
        with open("data", "w") as file:
            file.writelines(self.lines)

        self.ui_frame.destroy()
        self.create_main_ui()

    def submit_func(self, v1, v2, v3):
        if v1 == "" or v2 == "" or v3 == "":
            mb.showerror("Error", "Please enter all values")
            return

        with open("data", "a") as passwd_file:
            passwd_file.write(f"{v1} {v2} {v3}\n")

        self.add_frame.destroy()
        self.add_btn.configure(state="normal")

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.create_main_rows()
        self.main_frame.configure(width=600)

    def cancel_func(self):
        self.add_frame.destroy()
        self.add_btn.configure(state="normal")

    def create_add_ui(self):
        self.add_frame = ctk.CTkFrame(self.root)
        self.add_frame.pack(side="bottom", fill="both", pady=5, padx=5)

        self.add_frame.grid_columnconfigure(0, weight=1)
        self.add_frame.grid_columnconfigure(1, weight=1)

        add_var1 = ctk.StringVar()
        add_var2 = ctk.StringVar()
        add_var3 = ctk.StringVar()

        ctk.CTkLabel(self.add_frame, text="Name").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        ctk.CTkLabel(self.add_frame, text="Username").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        ctk.CTkLabel(self.add_frame, text="Password").grid(row=2, column=0, sticky="e", padx=10, pady=5)

        entry_width = 300

        ctk.CTkEntry(self.add_frame, textvariable=add_var1, width=entry_width).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        ctk.CTkEntry(self.add_frame, textvariable=add_var2, width=entry_width).grid(row=1, column=1, padx=5, pady=5, sticky="w")
        ctk.CTkEntry(self.add_frame, textvariable=add_var3, width=entry_width).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        submit_btn = ctk.CTkButton(self.add_frame, text="Submit",
                                   command=lambda: self.submit_func(add_var1.get(), add_var2.get(), add_var3.get()))
        submit_btn.grid(row=3, column=1, pady=10, sticky="w")

        cancel_btn = ctk.CTkButton(self.add_frame, text="cancel",
                                   command=self.cancel_func)
        cancel_btn.grid(row=3, column=1, pady=10)

        self.add_btn.configure(state="disabled")


if __name__ == "__main__":
    root = ctk.CTk()
    app = Application(root)
    root.mainloop()
