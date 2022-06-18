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