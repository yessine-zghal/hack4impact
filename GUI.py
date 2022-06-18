from Controller.controleur import *
from Controller.controleur  import Image,ImageTk
from tkinter import *

##################### definition ########################
source = ""
destination = ""
t = ""
font = ("Myriad Arabic",16)

def Traduct(event):
    return Traduire(txt)
########################### principal code ##############################################
#intialize sourde function and design the interface 
def sourde():
    root.destroy()
    global window,txt,frame
    window = Tk()
    window.title("application")
    window.geometry('1125x750')
    window.resizable(False,False)
    background,sound_img=declarationimage()
    img = Label(window,image=background,bg="#9AE1F5",anchor=CENTER)
    img.place(x=0,y=0)
    box_list_language = Combobox(window,values=('fr','ar','en','عربية'),font= font,justify=CENTER,height=10,width=13)
    box_list_language.current(1)
    box_list_language.place(x=50,y=193)
    def ComboAction(event):
        return comboAction(box_list_language)
    box_list_language.bind("<<ComboboxSelected>>", ComboAction)
    txt = scrolledtext.ScrolledText(window, width=43, height=10, background="#3580b1")
    txt.place(x=30.5, y=331)
    createButton(window, None, None, "#3580b1",play, 341, 579, 42, 42, sound_img,txt,box_list_language)
    createButton(window, '?', font, '#c2c2c2', '?',53,522,30,30,None,txt,None)
    createButton(window, '!', font, '#c2c2c2', '!',120,522,30,30,None,txt,None)
    createButton(window, '.', font, '#c2c2c2', '.',187,522,30,30,None,txt,None)
    createButton(window, ',', font, '#c2c2c2', ',', 254, 522, 30, 30,None,txt,None)
    createButton(window, 'supp', font, '#c2c2c2', delete, 320, 522, 50, 30, None, txt, None)
    frame = Label(window, bg="#3580b1")
    frame.place(x=434, y=174)
    show_frames(frame,txt)
    txt.bind("<Return>", Traduct)
    window.mainloop()
