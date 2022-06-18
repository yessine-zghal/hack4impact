import cv2
from tkinter.ttk import Combobox
from tkinter import scrolledtext
from gtts import gTTS
from PIL import Image,ImageTk
import pyttsx3
import mediapipe as mp
import time
import tensorflow as tf
import re
from deep_translator import GoogleTranslator
###################### global Parameter ############################
cathegories = ["ain","al","aleff","bb","dal","dha","dhad","fa","gaaf","ghain","ha","haa","jeem","kaaf",
              "khaa","la","laam","meem","nun","ra","saad",
               "seen","sheen","ta","taa","thaa","thal","toot","waw",
               "ya","yaa","zay"]
cap= cv2.VideoCapture(0)
# opening camera form your desktop 
param=40
mpHands = mp.solutions.hands
#cathegories = ["ain","al","aleff","bb","dal"]
hands = mpHands.Hands(static_image_mode=False,
                          max_num_hands=2,
                          min_detection_confidence=0.5,
                          min_tracking_confidence=0.5)
#detection hands from camera
mpDraw = mp.solutions.drawing_utils
#------------------------------------------------------------------#



######################### commun ###################################
#design button to click on fir your tikenter interface 
def createButton(window,text,font,color,command,x,y,w,h,image,texte,box):
    if(command ==play):
        print("there")
        buton= Button(window, text=text, font=font, background=color, command= lambda: play(texte,box),image=image)
    elif(command== ajout):
        buton = Button(window, text=text, font=font, background=color,command= lambda: ajout(texte,box), image=image)
        print('here')
    elif(command==delete):
        buton = Button(window, text=text, font=font, background=color, command=lambda: delete(texte),image=image)
    else:
        buton = Button(window, text=text, font=font, background=color, command=lambda: set_text(texte, command),image=image)
    buton= buton.place(x=x,y=y,width=w,height=h)
    return buton
#-----------------------------------------------------------------#
######################### root #####################################
#declaration root image for your code 
def declarationimageroot():
    rootback = Image.open('view/Img/rootback.png')
    nas = Image.open('view/Img/nas.png')
    ichara = Image.open('view/Img/ichara.png')
    rootback = ImageTk.PhotoImage(rootback)
    nas = ImageTk.PhotoImage(nas)
    ichara = ImageTk.PhotoImage(ichara)
    return rootback,ichara,nas
#-----------------------------------------------------------------#


######################### nas ######################################
#change from ichara to nas
def testpath(let,box,i,j):
        result = listeImg(let[i][j])
        if result != None:
            res = Image.open(result)
            imgdet = ImageTk.PhotoImage(res)
            box.configure(image=imgdet)
            box.image = imgdet
            print(result)
            if(j < len(let[i])-1):
                j=j+1
                k=2
            elif(i<len(let)-1):
              i=i+1
              j=0
              k=6
            else:
                return
            box.after(500*k,testpath,let,box,i,j)
        return
#deleting the text printed
def delete(texte):
    txte = texte.get("1.0", END)
    txte = txte[:-2]
    texte.delete('1.0', END)
    texte.insert(END,txte)
#adding text 
def ajout(texte, box):
    print("here")
    liste = []
    txte = texte.get("1.0", END)
    liste = txte.split()
    testpath(liste,box,0,0)
#declaration the image text
def declarationimagenas():
    nasback = Image.open('view/Img/nasback.png')
    nas_btn = Image.open('view/Img/nas_btn.png')
    nasback = ImageTk.PhotoImage(nasback)
    nas_btn = ImageTk.PhotoImage(nas_btn)
    img2 = ImageTk.PhotoImage(Image.open('Model/data/2a.png'))
    return nasback,nas_btn,img2
#labled the image
def listeImg (val):
    data_uses={'ا':"2a",'ب':"ba",'ت':"ta",'ث':"tha",'ج':"jeem",'ح':"7a",'خ':"kha",'ر':"ra",'ز':"za",'س':"sa",
                'ش':"cha",'ص':"sad",'ض':"dha",'ع':"3aa",'غ':"gha",'ف':"fa",'ق':"9a",'ك':"kef",'ط':"taa",'ظ':"dhad",'ه'
               :"ha", 'ل':"la",'ي':"ya",'ن':"nun",'م':"mim",'د':"da",'ذ':"dhe",'و':"waw"}
    if(val in data_uses):
        return os.path.join("Model/data",data_uses[val]+".png")
    return None
#-----------------------------------------------------------------#