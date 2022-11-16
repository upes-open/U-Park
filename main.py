import cv2
from numpy import ndarray
from imutils import grab_contours
from easyocr import Reader
from statistics import mode 
from tkinter import *
from tkinter import ttk
from tkinter import font
from turtle import color
from PIL import Image, ImageTk

#function to detect and read license plate numbers
def plate_read(a):
    img = a
    img2 = a
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plateCascade = cv2.CascadeClassifier('licenseplate.xml')
    faces = plateCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors = 5, minSize=(25,25))
    plat = []
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,0),5)
        plat = img[y: y+h, x:x+w]
    if (type(plat) is ndarray):
        gray = cv2.cvtColor(plat, cv2.COLOR_BGR2GRAY)
        blured_image = cv2.GaussianBlur(gray,(11,11),0)
        edge_image_blur = cv2.Canny(blured_image,30,100)
        edge_image_normal = cv2.Canny(gray,30,100)
        #Finding points of contours
        key_points=cv2.findContours(edge_image_blur,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        #defining contours from keypoints
        contours = grab_contours(key_points)
        #drawing contours
        reader = Reader(['en'])
        all_reads = reader.readtext(plat)
        license_plate = ("".join(map(lambda read: read[-2], all_reads))).upper()
        return str(license_plate)
    else:
        return

#function to read video or webcam feed and detecting license plate numbers from those frames
def ReadFromVideo(p):
    l = []
    #cap = cv2.VideoCapture(p)
    flag = True
    #GUI window
    root = Tk()
    label = Label(root)
    label.grid(row=1, column=0)
    a = Frame(root)
    a.grid(row=1, column=1)
    while flag:
        #reading video or webcam feed
        cap = cv2.VideoCapture(p)
        ret, frame = cap.read()
        if (type(frame) is ndarray):

            # Extract Region of interest
            #roi = frame[350: 730,510: 810]
            roi = frame[350: 600,350:1000]
            pl = (plate_read(roi))
            #cv2.imshow("roi", roi)
            #cv2.imshow("Frame", frame)

            #GUI
            new = ttk.Treeview(a)
            new['columns'] = ('srno','plate_no','park_no')
            new.column("#0", width=0,  stretch=NO)

            new.column("srno",anchor=CENTER,width=50)
            new.column("plate_no",anchor=CENTER,width=90)
            new.column("park_no",anchor=CENTER,width=50)

            new.heading("srno",text="Sr no",anchor=CENTER)
            new.heading("plate_no",text="Plate no",anchor=CENTER)
            new.heading("park_no",text="Park no",anchor=CENTER)
            def clear_all():
                for item in new.get_children():
                    new.delete(item)
            
            new.grid()
            start = Button(root, text="Clear Table", command=clear_all, background="yellow", foreground="black", width=20)
            start.grid(row=2, column=0)
            stop = Button(root, text="Stop", command=root.destroy, background="red", foreground="white", width=20)
            stop.grid(row=3, column=0)

            #function to show frames
            def show_frames():
                cv2image= cv2.cvtColor(cap.read()[1][350: 600,350:1000],cv2.COLOR_BGR2RGB)
                pl = (plate_read(cv2image))
                #insertion of license plate number in gui
                if not pl:
                    if (l != []):
                        ml = (mode(l))
                        new.insert(parent='',index='end',text='',values=(len(new.get_children()) + 1,ml,len(new.get_children()) + 1))
                        print(ml) 
                        l.clear()
                    else:
                        pass
                else:
                    l.append(pl)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image = img)
                label.imgtk = imgtk
                label.configure(image=imgtk)
                label.after(20, show_frames)

            show_frames()

            key = cv2.waitKey(30)
            if key == 27:
                break

            
            root.mainloop()
            
        else:
            flag = False
        #show_frames()
    root.mainloop()
    cap.release()
    cv2.destroyAllWindows()

#Reading from video
ReadFromVideo('VN20221021_095309.mp4')

#Reading from webcam
#ReadFromVideo(0)