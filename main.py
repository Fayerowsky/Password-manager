import customtkinter as ctk
from tkinter import messagebox as mb
from PIL import Image
from tkinter import filedialog
import os
import atexit

#add register on first run
#add simple pass_coding  /ɖ/
#add expand desc with title

class Application:
    def __init__(self, root):
        self.root = root
        self.root.geometry("250x150")
        self.root.resizable(False, False)
        self.root.title("Password Manager")
        self.root.attributes("-topmost", True)
        self.root.iconbitmap("image_files/app_ico.ico")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_login_ui()

        ctk.set_appearance_mode("dark")
#session information
    def session_open(self):
        self.pass_file = open("data/session.txt", "r").read()

    def session_close(self):
        open("data/session.txt", "w").write(self.pass_file)
        print("Session saved")
#login UI & service
    def create_login_ui(self):
        self.label1 = ctk.CTkLabel(self.root, text="Username")
        self.label2 = ctk.CTkLabel(self.root, text="Password")
        self.entry1 = ctk.CTkEntry(self.root)
        self.entry2 = ctk.CTkEntry(self.root, show="*")
        self.btn = ctk.CTkButton(self.root, text="Login", command=self.login_verify)
        self.label_res = ctk.CTkLabel(self.root, text="")

        self.label1.pack()
        self.entry1.pack()
        self.label2.pack()
        self.entry2.pack()
        self.btn.pack(pady=5)
        self.label_res.pack()
        self.pass_file = "data/data.txt"
        self.session_open()

    def login_verify(self):
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
#main_app UI
    def create_main_ui(self):
        self.root.geometry("700x400")

        self.ui_frame = ctk.CTkFrame(self.root)
        self.ui_frame.pack(side="top", fill="both", expand=True)

        self.side_frame = ctk.CTkFrame(self.ui_frame, width=50)
        self.side_frame.pack(side="left", fill="y", padx=5)
        self.side_frame.pack_propagate(False)

        self.main_frame = ctk.CTkScrollableFrame(self.ui_frame, width=600)
        self.main_frame.pack(side="right", fill="both", expand=True)

        icon_image = ctk.CTkImage(light_image=Image.open("image_files/add.png"), size=(35, 35))
        self.add_btn = ctk.CTkButton(self.side_frame, text="", image=icon_image, width=50, height=50,
                                     command=self.create_add_ui, fg_color="transparent")
        self.add_btn.pack(side="top", pady=10)
        icon_image2 = ctk.CTkImage(light_image=Image.open("image_files/path.png"), size=(35, 35))
        self.path_btn = ctk.CTkButton(self.side_frame, text="", image=icon_image2, width=50, height=50,
                                     command=self.path_select, fg_color="transparent")
        self.path_btn.pack(side="top", pady=10)

        if os.path.isfile(self.pass_file):
            self.create_main_ui_rows()
        else:
            ctk.CTkLabel(self.main_frame, text="No saved passwords, pick a file containing password data.").pack()

    def create_main_ui_rows(self):
        try:
            with open(self.pass_file, "r") as self.passwd_file:
                self.lines = self.passwd_file.readlines()

            contents = open(self.pass_file, "r").read()
            if not contents:
                ctk.CTkLabel(self.main_frame, text="No saved passwords.").pack()

            for line in self.lines:
                entry_frame = ctk.CTkFrame(self.main_frame, fg_color="#171717", corner_radius=5)
                entry_frame.pack(pady=7, padx=10, fill="x")

                slash_count = line.count(" / ")

                height = 88 if slash_count == 3 else 53

                entry = ctk.CTkTextbox(entry_frame, font=("Arial", 16), text_color="white", width=400,
                                       height=height, border_width=0, fg_color="transparent")
                entry.insert("0.0", line.strip().replace(" / ", "\n"))
                entry.configure(state="normal")
                entry.tag_add("readonly", "0.0", "end")
                entry.tag_config("readonly", foreground="white")
                entry.configure(state="disabled")
                entry.pack(side="left", padx=10, pady=5, fill="x", expand=True)

                delete_icon = ctk.CTkImage(light_image=Image.open("image_files/delete.png"), size=(25, 25))
                self.delete_btn = ctk.CTkButton(entry_frame, text="", image=delete_icon, width=40, height=40,
                                           fg_color="transparent",
                                           command=lambda l=line: self.delete_main_ui_rows(l))
                self.delete_btn.pack(side="right", padx=5, pady=5)

                modify_icon = ctk.CTkImage(light_image=Image.open("image_files/modify.png"), size=(25, 25))
                self.modify_btn = ctk.CTkButton(entry_frame, text="", image=modify_icon, width=40, height=40,
                                           fg_color="transparent",
                                           command=lambda l=line, sc=slash_count: self.create_modify_ui(l.strip(), sc))
                self.modify_btn.pack(side="right", padx=5, pady=5)

                add_more_icon = ctk.CTkImage(light_image=Image.open("image_files/add_more.png"), size=(25, 25))
                self.add_more_btn = ctk.CTkButton(entry_frame, text="", image=add_more_icon, width=40, height=40,
                                           fg_color="transparent",
                                           command=lambda l=line: self.create_add_more_ui(l.strip()))
                self.add_more_btn.pack(side="right", padx=5, pady=5)

                self.add_more_btn.configure(state="disabled") if slash_count == 3 else self.add_more_btn.configure(state="normal")

        except FileNotFoundError:
            ctk.CTkLabel(self.main_frame, text="No saved passwords.").pack()

    def delete_main_ui_rows(self, line):
        self.lines.remove(line)
        with open(self.pass_file, "w") as file:
            file.writelines(self.lines)

        self.ui_frame.destroy()
        self.create_main_ui()
#add_UI & service
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
                                   command=lambda: self.submit_add_ui(add_var1.get(), add_var2.get(),
                                                                         add_var3.get()))
        submit_btn.grid(row=3, column=1, pady=10, sticky="w")

        cancel_btn = ctk.CTkButton(self.add_frame, text="cancel",
                                   command=self.cancel_modify_ui)
        cancel_btn.grid(row=3, column=1, pady=10)

        self.add_btn.configure(state="disabled")

    def submit_add_ui(self, v1, v2, v3):
        if v1 == "" or v2 == "" or v3 == "":
            mb.showerror("Error", "Please enter all values")
            return

        with open(self.pass_file, "a") as passwd_file:
            passwd_file.write(f"{v1} / {v2} {v3}\n")

        self.add_frame.destroy()
        self.add_btn.configure(state="normal")

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.create_main_ui_rows()
        self.main_frame.configure(width=600)

    def cancel_add_ui(self):
        self.add_frame.destroy()
        self.add_btn.configure(state="normal")
#modify_ui & service
    def create_modify_ui(self, old_line, l):
        print(l)
        if l == 1:
            self.old_line = old_line
            self.add_frame = ctk.CTkFrame(self.root)
            self.add_frame.pack(side="bottom", fill="both", pady=5, padx=5)

            self.add_frame.grid_columnconfigure(0, weight=1)
            self.add_frame.grid_columnconfigure(1, weight=1)

            add_svar1 = ctk.StringVar(value=old_line.split()[0] if old_line else "")
            add_svar2 = ctk.StringVar(value=old_line.split()[2] if len(old_line.split()) > 1 else "")
            add_svar3 = ctk.StringVar(value=old_line.split()[3] if len(old_line.split()) > 2 else "")
            add_svar4 = ""
            add_svar5 = ""
            add_svar6 = ""

            ctk.CTkLabel(self.add_frame, text="New name").grid(row=0, column=0, sticky="e", padx=10, pady=5)
            ctk.CTkLabel(self.add_frame, text="New username").grid(row=1, column=0, sticky="e", padx=10, pady=5)
            ctk.CTkLabel(self.add_frame, text="New password").grid(row=2, column=0, sticky="e", padx=10, pady=5)

            entry_width = 300

            ctk.CTkEntry(self.add_frame, textvariable=add_svar1, width=entry_width).grid(row=0, column=1, padx=5, pady=5, sticky="w")
            ctk.CTkEntry(self.add_frame, textvariable=add_svar2, width=entry_width).grid(row=1, column=1, padx=5, pady=5, sticky="w")
            ctk.CTkEntry(self.add_frame, textvariable=add_svar3, width=entry_width).grid(row=2, column=1, padx=5, pady=5, sticky="w")

            submit_btn = ctk.CTkButton(self.add_frame, text="Submit",
                                   command=lambda: self.submit_modify_ui(add_svar1.get(), add_svar2.get(), add_svar3.get(), add_svar4, add_svar5, add_svar6))
            submit_btn.grid(row=3, column=1, pady=10, sticky="w")

            cancel_btn = ctk.CTkButton(self.add_frame, text="Cancel",
                                   command=self.cancel_modify_ui)
            cancel_btn.grid(row=3, column=1, pady=10)

        elif l == 3:
            self.old_line = old_line
            self.add_frame = ctk.CTkFrame(self.root)
            self.add_frame.pack(side="bottom", fill="both", pady=5, padx=5)

            self.add_frame.grid_columnconfigure(0, weight=1)
            self.add_frame.grid_columnconfigure(1, weight=1)
            self.add_frame.grid_columnconfigure(2, weight=1)

            split_line = old_line.split() if old_line else []
            add_svar1 = ctk.StringVar(value=split_line[0] if len(split_line) > 0 else "")
            add_svar2 = ctk.StringVar(value=split_line[2] if len(split_line) > 1 else "")
            add_svar3 = ctk.StringVar(value=split_line[3] if len(split_line) > 2 else "")
            add_svar4 = ctk.StringVar(value=split_line[5] if len(split_line) > 3 else "")
            add_svar5 = ctk.StringVar(value=split_line[7] if len(split_line) > 4 else "")
            add_svar6 = ctk.StringVar(value=split_line[8] if len(split_line) > 5 else "")

            entry_width = 250

            left_labels = ["Name", "Username", "Password"]
            left_vars = [add_svar1, add_svar2, add_svar3]

            for i in range(3):
                ctk.CTkLabel(self.add_frame, text=left_labels[i]).grid(row=i, column=0, sticky="e", padx=10, pady=5)
                ctk.CTkEntry(self.add_frame, textvariable=left_vars[i], width=entry_width).grid(row=i, column=1, padx=5,
                                                                                                pady=5, sticky="w")

            right_labels = ["Name", "Username", "Password"]
            right_vars = [add_svar4, add_svar5, add_svar6]

            for i in range(3):
                ctk.CTkLabel(self.add_frame, text=right_labels[i]).grid(row=i, column=2, sticky="e", padx=10, pady=5)
                ctk.CTkEntry(self.add_frame, textvariable=right_vars[i], width=entry_width).grid(row=i, column=3,
                                                                                                 padx=5, pady=5,
                                                                                                 sticky="w")

            submit_btn = ctk.CTkButton(
                self.add_frame, text="Submit",
                command=lambda: self.submit_modify_ui(
                    add_svar1.get(), add_svar2.get(), add_svar3.get(),
                    add_svar4.get(), add_svar5.get(), add_svar6.get()
                )
            )
            submit_btn.grid(row=3, column=1, columnspan=2, pady=10, padx=100, sticky="e")

            cancel_btn = ctk.CTkButton(self.add_frame, text="Cancel", command=self.cancel_modify_ui)
            cancel_btn.grid(row=3, column=2, columnspan=2, pady=10, sticky="w")

    def submit_modify_ui(self, sv1, sv2, sv3, sv4, sv5, sv6):
        if sv1 == "" or sv2 == "" or sv3 == "":
            mb.showerror("Error", "Please enter all values")
            return

        with open(self.pass_file, "r") as file:
            lines = file.readlines()

        with open(self.pass_file, "w") as file:
            for line in lines:
                if line.strip() == self.old_line:
                    if sv4 == "" or sv5 == "" or sv6 == "":
                        file.write(f"{sv1} / {sv2} {sv3}{sv4}{sv5}{sv6}\n")
                    else:
                        file.write(f"{sv1} / {sv2} {sv3} / {sv4} / {sv5} {sv6}\n")
                else:
                    file.write(line)

        self.add_frame.destroy()
        self.add_btn.configure(state="normal")

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.create_main_ui_rows()
        self.main_frame.configure(width=600)

    def cancel_modify_ui(self):
        self.add_frame.destroy()
        self.add_btn.configure(state="normal")
#add_more_ui & service
    def create_add_more_ui(self, old_line):
        self.old_line = old_line
        self.add_frame = ctk.CTkFrame(self.root)
        self.add_frame.pack(side="bottom", fill="both", pady=5, padx=5)

        self.add_frame.grid_columnconfigure(0, weight=1)
        self.add_frame.grid_columnconfigure(1, weight=1)

        add_amvar1 = ctk.StringVar()
        add_amvar2 = ctk.StringVar()
        add_amvar3 = ctk.StringVar()

        ctk.CTkLabel(self.add_frame, text="Add name").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        ctk.CTkLabel(self.add_frame, text="Add username").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        ctk.CTkLabel(self.add_frame, text="Add password").grid(row=2, column=0, sticky="e", padx=10, pady=5)

        entry_width = 300

        ctk.CTkEntry(self.add_frame, textvariable=add_amvar1, width=entry_width).grid(row=0, column=1, padx=5, pady=5,
                                                                                      sticky="w")
        ctk.CTkEntry(self.add_frame, textvariable=add_amvar2, width=entry_width).grid(row=1, column=1, padx=5, pady=5,
                                                                                      sticky="w")
        ctk.CTkEntry(self.add_frame, textvariable=add_amvar3, width=entry_width).grid(row=2, column=1, padx=5, pady=5,
                                                                                      sticky="w")

        submit_btn = ctk.CTkButton(self.add_frame, text="Submit",
                                   command=lambda: self.submit_add_more_ui(add_amvar1.get(), add_amvar2.get(),
                                                                           add_amvar3.get()))
        submit_btn.grid(row=3, column=1, pady=10, sticky="w")

        cancel_btn = ctk.CTkButton(self.add_frame, text="Cancel",
                                   command=self.cancel_add_more_ui)
        cancel_btn.grid(row=3, column=1, pady=10)

    def submit_add_more_ui(self, amv1, amv2, amv3):
        if amv1 == "" or amv2 == "" or amv3 == "":
            mb.showerror("Error", "Please enter all values")
            return

        with open(self.pass_file, "r") as file:
            lines = file.readlines()

        with open(self.pass_file, "w") as file:
            for line in lines:
                if line.strip() == self.old_line.strip():
                    file.write(line.strip() + " / " + f"{amv1} / {amv2} {amv3}\n")
                else:
                    file.write(line)

        self.add_frame.destroy()
        self.add_btn.configure(state="normal")

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.create_main_ui_rows()
        self.main_frame.configure(width=600)

    def cancel_add_more_ui(self):
        self.add_frame.destroy()
        self.add_btn.configure(state="normal")
#path_selection
    def path_select(self):
        self.pass_file = filedialog.askopenfilename(initialdir = "/", title = "Select a File",
                                          filetypes = (("Text files","*.txt*"), ("all files", "*.*")))

        self.path = self.pass_file
        self.ui_frame.destroy()
        self.create_main_ui()

if __name__ == "__main__":
    root = ctk.CTk()
    app = Application(root)
    atexit.register(app.session_close)
    root.mainloop()
