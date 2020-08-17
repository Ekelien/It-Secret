import tkinter as tk
from ctypes import windll
from tkinter import filedialog, scrolledtext
import os

'''
-------------------------------
        Helper Function
-------------------------------
'''


def XOR(filename, new_filename, password):
    file = open(filename, "rb")
    new_file = open(new_filename, "wb")
    bytes = file.read(1)
    counter = 0
    while bytes:
        new_file.write(byte_xor(bytes, str.encode(password[counter])))
        counter += 1
        if counter == len(password):
            counter = 0
        bytes = file.read(1)
    file.close()
    new_file.close()


def center_window(main_window, w, h):
    # get screen width and height
    ws = main_window.winfo_screenwidth()
    hs = main_window.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    main_window.geometry('%dx%d+%d+%d' % (w, h, x, y))


def center_message(mother, main, ww, wh, w, h):
    ws = mother.winfo_x()
    hs = mother.winfo_y()
    x = (ww-w)/2+ws
    y = (wh-h)/2+hs
    main.geometry('%dx%d+%d+%d' % (w, h, x, y))


def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


'''
----------------------------
        Helper Class     
----------------------------
'''


class MessageWindows:
    def __init__(self, st):
        self.top = tk.Toplevel(app)
        center_message(app, self.top, 666, 407, 300, 50)
        self.top.overrideredirect(1)
        self.l = tk.Label(self.top, text=st, font=("Calibri", 14))
        self.l.place(x=0, y=0, relwidth=1, relheight=1)
        self.l.config(bg="#ffa3a3")
        self.top.after(1000, self.cleanup)

    def cleanup(self):
        self.top.destroy()


class ConfirmationWindow:
    def __init__(self, st):
        self.top = tk.Toplevel(app)
        center_window(self.top, 400, 200)
        self.top.configure(background="#ffffff")
        self.top.resizable(0, 0)

        self.message = tk.Label(self.top)
        self.message.place(relx=0.075, rely=0.15, height=86, width=335)
        self.message.configure(background="#ffffff", foreground="#000000", text=st, font=(
            "Calibri", 12))

        self.confirm = MyButton(self.top)
        self.confirm.place(relx=0.2, rely=0.75, height=26, width=80)
        self.confirm.config(background="#f6f6f6",
                            foreground="#000000", text='''Confirm''')
        self.confirm.hover_color = "#ffa3a3"
        self.confirm.command(self.yes)

        self.cancel = MyButton(self.top)
        self.cancel.place(relx=0.6, rely=0.75, height=26, width=80)
        self.cancel.config(background="#f6f6f6",
                           foreground="#000000", text='''Cancel''')
        self.cancel.command(self.no)

        self.return_value = False

    def yes(self, event):
        self.return_value = True
        self.top.destroy()

    def no(self, event):
        self.top.destroy()


class MyButton(tk.Label):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        super().bind("<Enter>", self.mouse_enter)
        super().bind("<Leave>", self.mouse_leave)
        self.colour = "#f6f6f6"
        self.hover_color = "#e9e9f6"

    def place(self, **kw):
        super().place(**kw)

    def config(self, **kw):
        super().config(**kw)

    def command(self, function):
        super().bind("<Button-1>", function)

    def mouse_enter(self, event):
        super().config(bg=self.hover_color)

    def mouse_leave(self, event):
        super().config(bg=self.colour)


class HomeButton(MyButton):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        super().config(font=("Calibri", 14, "bold"))

    def mouse_enter(self, event):
        super().config(bg="#b894b8", fg="white")

    def mouse_leave(self, event):

        super().config(bg="#f2f2f2", fg="#f2f2f2")


'''
-----------------------------
        Main Function
-----------------------------
'''


class Main:
    def __init__(self, top=None):

        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'

        top.resizable(0, 0)
        top.title("It\'Secret")
        top.configure(background="#ffffff")
        self.app = top
        center_window(self.app, 666, 407)
        self.app.protocol("WM_DELETE_WINDOW", self.delete_temp_file)

        self.loading_frame = None  # loading interface
        self.instruction_frame = None  # instruction interface
        self.main_frame = None  # main program interface
        self.current_frame = None

        # widget of loading_frame
        self.Label_title = None
        self.Label_encrypt = None
        self.Label_dncrypt = None

        # widget of instruction_frame
        self.Label_instruction = None
        self.Button_back_to_menu = None
        self.Label_enter_program = None

        # widget of main_frame
        self.Button_start_processing = None
        self.Label_help = None
        self.Frame_choose_file = None
        self.Label_file_directory = None
        self.Button_choose_file = None
        self.Label_password_instruction = None
        self.Entry_password_entry = None

        self.filename = ""
        self.new_filename = ""
        self.password = ""
        self.made_temp_file = False
        self.string_vars = tk.StringVar()
        self.string_vars.trace("w", lambda name, index,
                               mode, var=self.string_vars: self.entryupdate())

        self.has_opened = False
        self.id = ""

        self.load_loading_frame(1)

    def load_loading_frame(self, event):
        if self.current_frame:
            self.current_frame.destroy()

        if self.id == "d":
            if self.has_opened:
                nw = ConfirmationWindow(
                "This action will delete your tempting file,\n please remember to save it\n if needed.")
            nw.top.grab_set()
            nw.top.focus_set()
            self.app.wait_window(nw.top)
            nw.top.grab_release()
            if nw.return_value:
                os.remove(self.new_filename)
                self.has_opened = False

        self.loading_frame = tk.Frame(self.app)
        self.loading_frame.place(
            relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.loading_frame.configure(relief='flat', background="#ffffff")
        self.Label_title = tk.Label(self.loading_frame)
        self.Label_title.place(relx=0.06, rely=0.074, height=226, width=586)
        self.Label_title.configure(background="#ffffff", font="-family {Calibri} -size 64 -weight bold",
                                   foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", text='''It'Secret''')

        self.Label_encrypt = HomeButton(self.loading_frame)
        self.Label_encrypt.place(
            relx=0.151, rely=0.713, height=66, relwidth=0.33)
        self.Label_encrypt.config(
            background="#f2f2f2", foreground="#f2f2f2", relief="flat", text='''Encrypting''')
        self.Label_encrypt.command(self.interface_selection)

        self.Label_decrypt = HomeButton(self.loading_frame)
        self.Label_decrypt.place(
            relx=0.52, rely=0.713, height=66, relwidth=0.33)
        self.Label_decrypt.config(
            background="#f2f2f2", foreground="#f2f2f2", relief="flat", text='''Decrypting''')
        self.Label_decrypt.command(self.interface_selection)

        self.current_frame = self.loading_frame

    def interface_selection(self, event):
        if event.widget == self.Label_decrypt:
            self.id = "d"
        elif event.widget == self.Label_encrypt:
            self.id = "e"
        self.load_instruction_frame("")

    def load_instruction_frame(self, event):
        if self.current_frame:
            self.current_frame.destroy()
        self.instruction_frame = tk.Frame(self.app)
        self.instruction_frame.place(
            relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.instruction_frame.configure(relief='flat', background="#ffffff")

        self.Text_instruction = scrolledtext.ScrolledText(
            self.instruction_frame)
        self.Text_instruction.place(
            relx=0.071, rely=0.098, relheight=0.698, relwidth=0.86)
        self.Text_instruction.configure(
            background="#f6f6f6", font=("Calibri", 12))
        self.Text_instruction.configure(foreground="black", relief="flat")

        if self.id == "d":
            self.Text_instruction.insert(tk.INSERT, '''\
                                        -----------------------
                                             Decrypting
                                        -----------------------
1. Choose your encrypted file, and enter the password you used 
    to encrypt it.
2. Click \"open\", the program will decrypt your file to a temporary 
    file and open it.
3. You can then modify the temporary file.
4. After modifying, close your file, and click \"save\". The program
    will encrypt your modified temporary file and update your 
    original file.

*  Closing the program, reselecting file or going back to main 
    menu will delete your temporary file.''')

        elif self.id == "e":
            self.Text_instruction.insert(tk.INSERT, '''\
                                        -----------------------
                                             Encrypting
                                        -----------------------
1. Choose the file you want it to be encrypted.
2. Enter your preferred password.
3. The program will encrypt the file using your password and 
    save it to a file with the name of your original file followed by 
    "_encrypted" suffix.

*  Please always remember your password. The program cannot
    tell whether the password is correct or not. If you forgot your 
    password, you can never decrypt your file!''')

        self.Button_back_to_menu = MyButton(self.instruction_frame)
        self.Button_back_to_menu.place(
            relx=0.25, rely=0.86, height=33, relwidth=0.24)
        self.Button_back_to_menu.config(
            background="#f2f2f2", foreground="#000000", text='''Back''')
        self.Button_back_to_menu.command(self.load_loading_frame)

        self.Button_enter_program = MyButton(self.instruction_frame)
        self.Button_enter_program.place(
            relx=0.51, rely=0.86, height=33, relwidth=0.24)
        self.Button_enter_program.config(
            background="#f2f2f2", foreground="#000000", text='''Continue''')
        self.Button_enter_program.command(self.load_main_frame)

        self.current_frame = self.instruction_frame

    def load_main_frame(self, event):
        if self.current_frame:
            self.current_frame.destroy()

        self.main_frame = tk.Frame(self.app)
        self.main_frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.main_frame.configure(relief='flat', background="#ffffff")

        self.Label_help = MyButton(self.main_frame)
        self.Label_help.place(relx=0.03, rely=0.049, height=36, width=35)
        self.Label_help.config(background="#f2f2f2",
                               foreground="#000000", text='''?''')
        self.Label_help.hover_color = "#ffffce"
        self.Label_help.command(self.load_instruction_frame)

        self.Label_home = MyButton(self.main_frame)
        self.Label_home.place(relx=0.1, rely=0.049, height=36, width=65)
        self.Label_home.config(background="#f2f2f2",
                               foreground="#000000", text='''Home''')
        self.Label_home.hover_color = "#ffffce"
        self.Label_home.command(self.load_loading_frame)

        self.Frame_choose_file = tk.Frame(self.main_frame)
        self.Frame_choose_file.place(
            relx=0.101, rely=0.295, relheight=0.081, relwidth=0.8)
        self.Frame_choose_file.configure(relief='flat', background="#ffffff")

        self.Label_file_directory = tk.Label(self.Frame_choose_file)
        self.Label_file_directory.place(
            relx=0.0, rely=0.0, height=33, width=400)
        self.Label_file_directory.configure(
            background="#f9f9f9", foreground="#000000")

        self.Button_choose_file = MyButton(self.Frame_choose_file)
        self.Button_choose_file.place(
            relx=0.75, rely=0.0, height=33, width=133)
        self.Button_choose_file.config(
            background="#f2f2f2", foreground="#000000", text='''Choose File''')
        self.Button_choose_file.command(self.select_file)

        self.Label_password_instruction = tk.Label(self.main_frame)
        self.Label_password_instruction.place(
            relx=0.35, rely=0.467, height=33, width=200)
        self.Label_password_instruction.configure(
            background="#ffffff", foreground="#000000", text='''Please Enter Password''')

        self.Entry_password_entry = tk.Entry(self.main_frame)
        self.Entry_password_entry.place(
            relx=0.251, rely=0.663, height=29, relwidth=0.5)
        self.Entry_password_entry.configure(textvariable=self.string_vars, background="#f2f2f2",
                                            font="-family {Calibri}", foreground="#000000", justify='center', relief="flat")

        self.password = ""
        self.Entry_password_entry.delete(0, 'end')

        if self.id == "d":
            self.Button_start_processing = MyButton(self.main_frame)
            self.Button_start_processing.place(
                relx=0.25, rely=0.86, height=33, relwidth=0.24)
            self.Button_start_processing.config(
                background="#f2f2f2", foreground="#000000", text='''Open''')
            self.Button_start_processing.command(self.process)

            self.Button_save_modified = MyButton(self.main_frame)
            self.Button_save_modified.place(
                relx=0.51, rely=0.86, height=33, relwidth=0.24)
            self.Button_save_modified.config(
                background="#f2f2f2", foreground="#000000", text='''Save''')
            self.Button_save_modified.command(self.save_file)

        elif self.id == "e":
            self.Button_start_processing = MyButton(self.main_frame)
            self.Button_start_processing.place(
                relx=0.38, rely=0.86, height=33, relwidth=0.26)
            self.Button_start_processing.config(
                background="#f2f2f2", foreground="#000000", text='''Encrypt''')
            self.Button_start_processing.command(self.encrypt)

        self.current_frame = self.main_frame

    def select_file(self, event):
        if self.has_opened:
            nw = ConfirmationWindow(
                "This action will delete your tempting file,\n please remember to save it\n if needed.")
            nw.top.grab_set()
            nw.top.focus_set()
            self.app.wait_window(nw.top)
            nw.top.grab_release()
            if nw.return_value:
                os.remove(self.new_filename)
                self.has_opened = False
            else:
                return
        self.filename = filedialog.askopenfilename(title="Select A File")
        if self.filename:
            self.Label_file_directory.config(text=self.filename)

    def entryupdate(self):
        temp = self.string_vars.get()
        if len(temp) > len(self.password):
            self.password += temp[-1]
        else:
            self.password = self.password[:-1]
        self.Entry_password_entry.delete(0, 'end')
        self.Entry_password_entry.insert(0, "*"*len(self.password))

    def process(self, event):
        if self.filename == None or self.filename == "":
            nw = MessageWindows("Please choose a file!")
            return
        elif self.password == "":
            nw = MessageWindows("Please enter password!")
            return
        self.new_filename = self.filename[:self.filename.rfind(
            "/")+1]+"temp"+self.filename[self.filename.rfind("."):]
        XOR(self.filename, self.new_filename, self.password)
        os.system("start "+self.new_filename)
        self.has_opened = True
        return

    def save_file(self, event):
        if not self.has_opened:
            nw = MessageWindows("Not available!")
            return
        else:
            nw = ConfirmationWindow(
                "This action will permenently \ndelete and replace your original file,\n are you SURE?")
            nw.top.grab_set()
            nw.top.focus_set()
            self.app.wait_window(nw.top)
            nw.top.grab_release()
            if nw.return_value:
                XOR(self.new_filename, self.filename, self.password)
            nw = MessageWindows("Done!")
            return

    def delete_temp_file(self):
        if self.id=="d":
            try:
                os.remove(self.new_filename)
            except:
                pass
        app.destroy()

    def encrypt(self, event):
        if self.filename == None or self.filename == "":
            nw = MessageWindows("Please choose a file!")
            return
        elif self.password == "":
            nw = MessageWindows("Please enter password!")
            return
        self.new_filename = self.filename[:self.filename.rfind(
            ".")]+"_encrypted"+self.filename[self.filename.rfind("."):]
        XOR(self.filename, self.new_filename, self.password)
        path = self.filename[:self.filename.rfind("/")]
        os.startfile(path)
        return


windll.shcore.SetProcessDpiAwareness(1)     # Set DPI

app = tk.Tk()
main = Main(app)
app.mainloop()
