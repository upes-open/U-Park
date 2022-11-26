from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter as tk
import pygsheets
import cv2


# color data ------------------------
dark = '#222222'
light = '#EAF4F4'
accent = '#A0CC3A'
buttoncol = '#555555'
#------------------------------------

#-------------------------------------------- Root widget -------------------------------------------------#
root=Tk()
root.title("Authenticator")
root.geometry("825x400+300+200")
root.resizable(False, False)
root.config(bg=dark)

#------------------------------------------- Second widget ------------------------------------------------#

def enter_second():
    namecheck=user.get()
    passcheck=passw.get()

    if namecheck=="Admin":
        if passcheck=="12345":
            second=Tk()
            second.title("Authenticator")
            second.resizable(False, False)
            second.config(bg=dark, padx=10, pady=10)
            root.destroy()
    
            Label(second, text="Automated Parking System", bg=dark, fg=light, border=0, font=("Microsoft YaHei UI", 25), pady=10, padx=30).grid(row=0, column=0, columnspan=3, sticky=E+W)
            Label(second, text="Powered by OPEN", bg=dark, fg=accent, border=0, font=("Microsoft YaHei UI", 15), pady=10).grid(row=1, column=0, columnspan=3, sticky=E+W)
            
            Label(second, text="Raghav Agarwal", bg=dark, fg=light, border=0, font=("Microsoft YaHei UI", 12), pady=5).grid(row=3, column=0, sticky=E+W)
            Label(second, text="Saarini Ritesh", bg=dark, fg=light, border=0, font=("Microsoft YaHei UI", 12), pady=5).grid(row=3, column=1, sticky=E+W)
            Label(second, text="Akanksha Gupta", bg=dark, fg=light, border=0, font=("Microsoft YaHei UI", 12), pady=5).grid(row=3, column=2, sticky=E+W)
            
            Label(second, text="Navinya Sawarkar", bg=dark, fg=light, border=0, font=("Microsoft YaHei UI", 12), pady=5).grid(row=4, column=0, sticky=E+W)
            Label(second, text="Khushi Chadha", bg=dark, fg=light, border=0, font=("Microsoft YaHei UI", 12), pady=5).grid(row=4, column=1, sticky=E+W)
            Label(second, text="Rohin Mehrotra", bg=dark, fg=light, border=0, font=("Microsoft YaHei UI", 12), pady=5).grid(row=4, column=2, sticky=E+W)
            

            def exit_sec():
                second.destroy()

            def third():
                second.destroy()
                enter_third()

            Button(second, text="Start", padx=20, border=0, bg=buttoncol, fg=light, command=third).grid(row=5, column=0, pady=10)
            Button(second, text="Exit ", padx=20, border=0, bg=buttoncol, fg=light, command=exit_sec).grid(row=5, column=2, pady=10)

            second.mainloop()
        else:
            response = messagebox.showwarning("Error", "Incorrect Username or Password")
            Label(root, text=response).pack()
    else:
        response = messagebox.showwarning("Error", "Incorrect Username or Password")
        Label(root, text=response).pack()

#-------------------------------------------- Third widget ------------------------------------------------#

def enter_third():
    third = Tk()
    third.title("Automated Parking System")
    third.resizable(False, False)
    third.config(bg=dark)

    bigframe = LabelFrame(third, padx=10, pady=10)
    bigframe.pack(padx=10, pady=10)
    frame = LabelFrame(bigframe, text="Camera Views", padx=5, pady=5)
    frame.grid(row=0, column=0, padx=10, pady=10)
    frame2 = LabelFrame(bigframe, text="Log", padx=5, pady=5)
    frame2.grid(row=0, column=1, padx=10, pady=10)

    #images
    
    # car = Image.open("Authenticator\car.png")
    # resize_car = car.resize((400, 220))
    # car = ImageTk.PhotoImage(resize_car)
    Label(frame, text="Vehicle Entry View", bg=light).grid(row=1, column=0, sticky=E+W, columnspan=2)
    # Label(frame, image=car, bg=light).grid(row=2, column=0)

    app = Frame(frame, bg="white")
    app.grid(row=2, column=0, columnspan=2)
    # Create a label in the frame
    lmain = Label(app)
    lmain.grid(row=2, column=0, columnspan=2)

    # video
    cap = cv2.VideoCapture(0) #<-------------------------------------video source
    def video_stream():
        
        _, frame = cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        resize = cv2.resize(cv2image, (600,350))
        img = Image.fromarray(resize)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(1, video_stream) 


    #-----------------------------buttons
    def exit_third():
        third.destroy()

    def enter_roi():
        root = Toplevel()
        root.title("ROI")
        root.geometry("300x100")
        root.resizable(False, False)
        root.config(bg=dark)
        # Create a frame
        app = Frame(root, bg="white")
        app.grid()
        # Create a label in the frame
        lmain = Label(app)
        lmain.grid()

        # Capture from camera
        cap = cv2.VideoCapture(0)

        # function for video streaming
        def video_stream():
            _, frame = cap.read()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            resize = cv2.resize(cv2image, (300,100))
            img = Image.fromarray(resize)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            lmain.after(1, video_stream) 


        video_stream()
        root.mainloop()

    
    Button(frame, text="Number Plate View", bg=buttoncol, border=0, fg=light, pady=5, command=enter_roi).grid(row=3, column=0, pady=10)
    Button(frame, text="Exit", bg=buttoncol, border=0, fg=light, pady=5, padx=40, command=exit_third).grid(row=3, column=1, pady=10)
    video_stream()
    #table ----------------------------

    path = 'Authenticator\key.json'
    gc=pygsheets.authorize(service_account_file=path)
    sheetname = 'ParkingData'
    sh = gc.open(sheetname)
    wk1 = sh[0]

    l1 = wk1.get_all_values(include_tailing_empty=False, include_tailing_empty_rows=False)
    print(l1)

    # Using treeview widget
    trv = ttk.Treeview(frame2, selectmode ='browse')
    trv.grid(row=1,column=1,padx=20,pady=20)
    # number of columns
    trv["columns"] = ("1", "2", "3", "4")
    
    # Defining heading
    trv['show'] = 'headings'
    trv['height']=15 # Number of rows to display by default. 
    # width of columns and alignment 
    trv.column("1", width = 50, anchor ='c')
    trv.column("2", width = 130, anchor ='c')
    trv.column("3", width = 80, anchor ='c')
    trv.column("4", width = 80, anchor ='c')
    
    # Headings  
    # respective column heading are taken from google sheets
    # if only data is taken from google sheet then below lines can be added
    trv.heading("1", text ="Sr. No")
    trv.heading("2", text ="Number Plate")
    trv.heading("3", text ="Entry Time")
    trv.heading("4", text ="Token")

    for dt in l1:  # l1 is the list having google sheets data
        trv.insert("", 'end',iid=dt[0], text=dt[0],
                values =(dt[0],dt[1],dt[2],dt[3]))

    third.mainloop()

#---------------------------------------- Authentication window -------------------------------------------#

#Logo-------------
img = Image.open("Authenticator\login.png")
resize_image = img.resize((400, 400))
img = ImageTk.PhotoImage(resize_image)
Label(root, image=img, bg=light,padx=100).grid(row=0, column=0, rowspan=3)

#Form--------------
Frame(root, width=15, bg=dark).grid(row=0, column=1) #gap between left and right panel

frame = Frame(root, width=350, height=350, bg=dark, padx=50)
frame.grid(row=0, column=2)

heading = Label(frame, text="Automated\nParking", fg=accent, bg=dark, font=('Microsoft YaHei UI Light',23, 'bold'), justify=CENTER)
heading.grid(row=0, column=0, pady=20, padx=70)

#FormFunctions------
def user_enter(e):
    name=user.get()
    if name=="Username":
        user.delete(0, 'end')

def user_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,"Username")

def passw_enter(e):
    name=passw.get()
    if name=="Password":
        passw.delete(0, 'end')

def passw_leave(e):
    name=passw.get()
    if name=='':
        passw.insert(0,"Password")


#Form Fields-------
user = Entry(frame, width=30, fg=light, border=0, bg=dark, font=('Microsoft YaHei UI Light',11), justify=LEFT)
user.grid(row=1, column=0, pady=10)
user.insert(0,"Username")
user.configure(insertbackground=light)

user.bind('<FocusIn>', user_enter)
user.bind('<FocusOut>', user_leave)

Frame(frame,width=275, height=2, bg=accent).place(x=20, y=165) #underline below Username

Frame(frame, height=15, bg=dark, pady=20).grid(row=2, column=0) #gap between user and passw

passw = Entry(frame, width=30, fg=light, border=0, bg=dark, font=('Microsoft YaHei UI Light',11), justify=LEFT)
passw.grid(row=3, column=0, pady=10)
passw.insert(0,"Password")
passw.configure(insertbackground=light)

passw.bind('<FocusIn>', passw_enter)
passw.bind('<FocusOut>', passw_leave)

Frame(frame,width=275, height=2, bg=accent).place(x=20, y=220) #underline below password

Frame(frame, height=40, bg=dark, pady=20).grid(row=4, column=0) #gap between passw and button

#button--------
Button(frame,width=20, fg=light, bg=buttoncol, text="Sign in", font=('Microsoft YaHei UI',10), pady=5, border=0, relief=SUNKEN, command=enter_second).grid(row=5, column=0)





root.mainloop()