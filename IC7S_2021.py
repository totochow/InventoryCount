from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3
import tkinter.ttk as ttk
from datetime import datetime
import sys
import pyautogui
import time
import threading

#Setting up Variables
CycleCountDate = '7Seas Inventory Count \n Jan 31, 2021'

#Color Scheme
Color1 = '#9DE0AD'
Color2 = '#45ADA8'
Color3 = '#547980'

#Text Color
Dark_Text = '#594F4F'
Light_Text = '#E5FCC2'

#setting up the beginning page
root = Tk()
root.attributes('-fullscreen', True)
root.title(CycleCountDate)


#first homepage for log in
width = 230
height = 260
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, 0, 0))
root.resizable(0, 0)
root.config(bg=Color3)

style = ttk.Style()
style.configure("Treeview.Heading", font=(None, 8))
style.configure("Treeview", font=(None, 7))
            
#========================================VARIABLES========================================
USERNAME = StringVar()
PASSWORD = StringVar()
BIN_LOCATION = StringVar()
ITEM_NUM = StringVar()
LOT_NUM = StringVar()
PRODUCT_QTY = IntVar()
UM = StringVar()
SEARCH = StringVar()


#========================================METHODS==========================================

def Database():
    global conn, cursor
    conn = sqlite3.connect('pythontut.db')
    cursor = conn.cursor()
    #cursor.execute("CREATE TABLE IF NOT EXISTS `admin` (admin_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT)")
    #cursor.execute("CREATE TABLE IF NOT EXISTS `product` (product_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, bin_location TEXT, item_num TEXT, lot_num TEXT, product_qty TEXT)")
    cursor.execute("SELECT * FROM `admin` WHERE `username` = 'admin' AND `password` = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `admin` (username, password) VALUES('admin', 'admin')")
        conn.commit()

def Exit():

    result = tkMessageBox.askquestion(CycleCountDate, 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        global afk
        print('Exit')
        afk = False
        print(afk)
        root.destroy()
        sys.exit()




def Exit2():
    result = tkMessageBox.askquestion(CycleCountDate, 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        print('Exit2')
        global afk
        afk = False
        Home.destroy()
        sys.exit()


        
def ShowLoginForm():
    global loginform
    loginform = Toplevel()
    loginform.attributes('-fullscreen', True)
    loginform.title("Account Login")
    width = 230
    height = 260 
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    #loginform.resizable(0, 0)
    loginform.geometry("%dx%d+%d+%d" % (width, height, 0, 0))
    LoginForm()

def LoginForm():
    global lbl_result
    TopLoginForm = Frame(loginform, width=220, height=50, bd=1, relief=SOLID)
    TopLoginForm.pack(side=TOP, pady=10)
    lbl_text = Label(TopLoginForm, text="Login", font=('arial', 9), width=220, bg=Color2, fg=Light_Text)
    lbl_text.pack(fill=X)
    MidLoginForm = Frame(loginform, width=220)
    MidLoginForm.pack(side=TOP, pady=25)
    lbl_username = Label(MidLoginForm, text="Count Name:", font=('arial', 12), bd=9)
    lbl_username.grid(row=0)
    lbl_password = Label(MidLoginForm, text="Password:", font=('arial', 12), bd=9)
    lbl_password.grid(row=1)
    lbl_result = Label(MidLoginForm, text="", font=('arial', 9))
    lbl_result.grid(row=3, columnspan=2)
    username = Entry(MidLoginForm, textvariable=USERNAME, font=('arial', 12), width=9)
    username.grid(row=0, column=1)
    password = Entry(MidLoginForm, textvariable=PASSWORD, font=('arial', 12), width=9, show="*")
    password.grid(row=1, column=1)
    btn_login = Button(MidLoginForm, text="Login", font=('arial', 9), width=15, command=Login, bg=Color2, fg=Light_Text)
    btn_login.grid(row=2, columnspan=2, pady=10)
    btn_login.bind('<Return>', Login)
    username.focus_set()
     

    
def Home():
    global Home
    Home = Tk()
    Home.attributes('-fullscreen', True)
    Home.title("Home")
    width = 230
    height = 260
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    Home.geometry("%dx%d+%d+%d" % (width, height, 0, 0))
    Home.resizable(0, 0)
    Title = Frame(Home, bd=1, relief=SOLID)
    Title.pack(pady=10)
    lbl_display = Label(Title, text=CycleCountDate, font=('arial', 15))
    lbl_display.pack()
    menubar = Menu(Home)
    filemenu = Menu(menubar, tearoff=0)
    filemenu2 = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Logout", command=Logout)
    filemenu.add_command(label="Exit", command=Exit2)
    filemenu2.add_command(label="Add new", command=ShowAddNew)
    filemenu2.add_command(label="View", command=ShowView)
    menubar.add_cascade(label="Account", menu=filemenu)
    menubar.add_cascade(label="Inventory", menu=filemenu2)
    Home.config(menu=menubar)
    Home.config(bg=Color3)


def ShowAddNew():
    global addnewform
    addnewform = Toplevel()
    addnewform.attributes('-fullscreen', True)
    addnewform.title("Add new")
    width = 230
    height = 260
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    addnewform.geometry("%dx%d+%d+%d" % (width, height, 0, 0))
    addnewform.resizable(0, 0)
    AddNewForm()

def AddNewForm():
    TopAddNew = Frame(addnewform, width=220, height=10, bd=1, relief=SOLID)
    TopAddNew.pack(side=TOP, pady=5)
    rack = str(USERNAME.get())
    lbl_text = Label(TopAddNew, text=("Adding Count Result \n" + rack[3:-1] + " Count # " + rack[-1]), font=('arial', 9), width=220, bg=Color2, fg=Light_Text)
    lbl_text.pack(fill=X)
    MidAddNew = Frame(addnewform, width=220)
    MidAddNew.pack(side=TOP, pady=5)
    lbl_itemnum = Label(MidAddNew, text="Item Number:", font=('arial', 11), bd=6)
    lbl_itemnum.grid(row=0, sticky=W)
    lbl_lotnum = Label(MidAddNew, text="Lot:", font=('arial', 11), bd=6)
    lbl_lotnum.grid(row=2, sticky=W)
    lbl_qty = Label(MidAddNew, text="Lot Quantity:", font=('arial', 11), bd=6)
    lbl_qty.grid(row=3, sticky=W)
    lbl_UoM = Label(MidAddNew, text="Count UM in:", font=('arial', 11), bd=6)
    lbl_UoM.grid(row=1, sticky=W)
    itemnum = Entry(MidAddNew, textvariable=ITEM_NUM, font=('arial', 10), width=18)
    itemnum.grid(row=0, column=1)
    lotnum = Entry(MidAddNew, textvariable=LOT_NUM, font=('arial', 10), width=18)
    lotnum.grid(row=2, column=1)
    qty = Entry(MidAddNew, textvariable=PRODUCT_QTY, font=('arial', 10), width=18)
    qty.grid(row=3, column=1)
    UoM = OptionMenu(MidAddNew,UM," ")
    #UoM = Entry(MidAddNew, textvariable=UM, font=('arial', 10), width=20)
    UoM.grid(row=1, column=1)
    btn_add = Button(MidAddNew, text="Save", font=('arial', 12), width=14, command=AddNew, bg=Color2, fg=Light_Text)
    btn_add.grid(row=4, columnspan=1, pady=5, column=1)
    btn_add.bind('<Button-1>', lambda Event: FocusSet(itemnum))
    #btn_close
    btn_close = Button(MidAddNew, text="Close", font=('arial', 12), width=5, command=addnewform.destroy, bg=Color3, fg=Light_Text)
    btn_close.grid(row=5, rowspan=1, pady=50, column=1, sticky = 'SE')
    PRODUCT_QTY.set("")
    ITEM_NUM.trace('w', my_tracer)

    TopAddNew.focus_set()
    itemnum.focus_set()

    
    #UM.set("(Please Select)")
    mainloop()  


def my_tracer(a,b,c):
    Database()
    #UM.set(ITEM_NUM.get())
    cursor.execute("SELECT * FROM `item_um` WHERE `itemnum` = ? ", ((ITEM_NUM.get().upper(),)))
    if cursor.fetchone() is None:
        UM.set("Error, Check Item#")
    else:
        cursor.execute("SELECT * FROM `item_um` WHERE `itemnum` = ? ", ((ITEM_NUM.get().upper(),)))
        um_select = cursor.fetchone()
        UM.set(um_select[1])
    #print(um_select[1])
    #cursor.close()
    #conn.close() 
    #UM.set("ABC")
    
def FocusSet(itemnum):
    itemnum.focus_set()

def AddNew():
    Database()
    cursor.execute("INSERT INTO `product` (bin_location, item_num, lot_num, product_qty, um, timestamp) VALUES(?, ?, ?, ?, ?,?)", (str(USERNAME.get()), str(ITEM_NUM.get()), str(LOT_NUM.get()), int(PRODUCT_QTY.get()), str(UM.get()), datetime.now()))
    conn.commit()
    ITEM_NUM.set("")
    LOT_NUM.set("")
    PRODUCT_QTY.set("")
    UM.set("loading...")
    cursor.close()
    conn.close()

def ViewForm():
    global tree
    TopViewForm = Frame(viewform, width=220, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    BottomViewForm = Frame(viewform, width=110)
    BottomViewForm.pack(side=BOTTOM, fill=Y)
    MidViewForm = Frame(viewform, width=110)
    MidViewForm.pack(side=RIGHT)
    lbl_text = Label(TopViewForm, text= str(USERNAME.get()), font=('arial', 9), width=110,  bg=Color2, fg=Light_Text)
    lbl_text.pack(fill=X)
    #lbl_txtsearch = Label(BottomViewForm, text="Search", font=('arial', 7))
    #lbl_txtsearch.pack(side=TOP, anchor=W)
    #search = Entry(BottomViewForm, textvariable=SEARCH, font=('arial', 7), width=5)
    #search.pack(side=TOP,  padx=5, fill=X)
    #btn_search = Button(BottomViewForm, text="Search", command=Search)
    #btn_search.pack(side=TOP, padx=5, pady=5, fill=X)
    #btn_reset = Button(BottomViewForm, text="Reset", command=Reset)
    #btn_reset.pack(side=LEFT, padx=5, pady=5, fill=X)
    btn_delete = Button(BottomViewForm, text="Delete", command=Delete,  bg=Color2, fg=Light_Text)
    btn_delete.pack(side=RIGHT, padx=5, pady=5, fill=X)
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm, columns=("ProductID", "Bin Location", "Item Number","Lot","Quantity","UM"), selectmode="extended", height=50, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('ProductID', text="ProductID",anchor=W)
    tree.heading('Bin Location', text="Bin",anchor=W)
    tree.heading('Item Number', text="ITM#",anchor=W)
    tree.heading('Lot', text="Lot",anchor=W)
    tree.heading('Quantity', text="Qty",anchor=W)
    tree.heading('UM', text="UM",anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=0)
    tree.column('#2', stretch=NO, minwidth=0, width=0)
    tree.column('#3', stretch=YES, minwidth=0, width=75)
    tree.column('#4', stretch=YES, minwidth=0, width=70)
    tree.column('#5', stretch=YES, minwidth=0, width=40)
    tree.column('#6', stretch=YES, minwidth=0, width=30)
    tree.pack()
    DisplayData()

def DisplayData():
    Database()
    cursor.execute("SELECT * FROM `product` WHERE `bin_location` LIKE ? ORDER BY timestamp DESC", ('%'+str(USERNAME.get())+'%',))
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def Search():
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        Database()
        cursor.execute("SELECT * FROM `product` WHERE `item_num` LIKE ?", ('%'+str(SEARCH.get())+'%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

#def Reset():
#    tree.delete(*tree.get_children())
#    DisplayData()
#    SEARCH.set("")

def Delete():
    if not tree.selection():
       print("ERROR")
    else:
        result = tkMessageBox.askquestion(CycleCountDate, 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            cursor.execute("DELETE FROM `product` WHERE `product_id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()
    

def ShowView():
    global viewform
    viewform = Toplevel()
    viewform.title("View Product")
    width = 230
    height = 260
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    viewform.geometry("%dx%d+%d+%d" % (width, height, 0, 0))
    viewform.resizable(0, 0)
    ViewForm()

def Logout():
    result = tkMessageBox.askquestion(CycleCountDate, 'Are you sure you want to logout?', icon="warning")
    if result == 'yes': 
        admin_id = ""
        USERNAME.set("")
        root.deiconify()
        Home.destroy()
  
def Login(event=None):
    global admin_id
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
            data = cursor.fetchone()
            admin_id = data[0]
            #USERNAME.set("")
            PASSWORD.set("")
            lbl_result.config(text="")
            ShowHome()
        else:
            lbl_result.config(text="Invalid username or password", fg="red")
            USERNAME.set("")
            PASSWORD.set("")
    cursor.close()
    conn.close() 

def ShowHome():
    root.withdraw()
    Home()
    loginform.destroy()

def mouseclick():
    pyautogui.FAILSAFE = False

    print('FAILSAFE')
    numMin = None
    if ((len(sys.argv)<2) or sys.argv[1].isalpha() or int(sys.argv[1])<1):
        numMin = 1
    else:
        numMin = int(sys.argv[1])
    while(True):
        global afk
        x=0
        print(afk)
        while(x<numMin):
            time.sleep(60)
            x+=1

        for i in range(0,5):
            pyautogui.moveTo(pyautogui.position()[0],pyautogui.position()[1]+i)
        #pyautogui.moveTo(1,1)
        #for i in range(0,3):
        #    pyautogui.press("shift")            
        if afk == False:
            print('thread killed')
            break
        print("Movement made at {}".format(datetime.now().time()))


def foreground():
    
    #========================================MENUBAR WIDGETS==================================
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Account", command=ShowLoginForm)
    filemenu.add_command(label="Exit", command=Exit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)
    print('MENUBAR WIDGETS')
    
    #========================================FRAME============================================
    Title = Frame(root, bd=2, relief=SOLID)
    Title.pack(pady=10)
    print('FRAME')
    
    
    #========================================LABEL WIDGET=====================================
    lbl_display = Label(Title, text=CycleCountDate, font=('arial', 15))
    lbl_display.pack()
    print('LABEL WIDGET')


afk = True
b = threading.Thread(name='background', target=mouseclick)
f = threading.Thread(name='foreground', target=foreground)


b.start()
f.start()


#========================================INITIALIZATION===================================
if __name__ == '__main__':
    root.mainloop()
print('INITIALIZATION')

