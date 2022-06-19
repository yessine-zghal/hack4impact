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
######################### sourde ###################################
#update the text 
def set_text(txt,text):
    if txt !=None:
        val=txt.get("1.0",END)
        val=val[0:-1]
        val=val+str(text)
        txt.delete("1.0",END)
        return txt.insert(END,val)
    return
#playing the sound to text
def play(txt,box_list_language):
    destination=box_list_language.get()
    engine = pyttsx3.init()
    if (destination=='fr'):
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_FR - FR_HORTENSE_11.0')
    if (destination == 'en'):
        engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
    if (destination == 'ar'):
        myobj = gTTS(text=txt.get("1.0", END), lang='ar', slow=False)
        myobj.save("convert.wav")
        os.system("convert.wav")
    engine.say(text=txt.get("1.0", END))
    engine.runAndWait()
def comboAction(box_list_language):
    global destination
    destination = box_list_language.get()
def declarationimage():
    global background,sound_img
    image = Image.open('view/Img/background.png')
    sound_image = Image.open('view/Img/sound.png')
    background = ImageTk.PhotoImage(image)
    sound_img = ImageTk.PhotoImage(sound_image)
    return background,sound_img
source='ar'
#traduction
def Traduire(txt):
    global source
    translated =GoogleTranslator(source=source,target=destination).translate(txt.get("1.0",END))
    print(translated)
    source=destination
    txt.delete('1.0', END)
    txt.insert(END, translated)
#detection frame in image hand
def constrainmin(val, min_val):
    if val-param < min_val: return min_val
    return val-param
def constrainmax(val, max_val):
    if val+param > max_val: return max_val
    return val+param

global cTime
global pTime
cTime=0
pTime=0
i=0
listadd=["a"]
#loading federated model 
model = tf.keras.models.load_model("alphabet.model")
#intialize the frame and show there
def show_frames(frame,texts):
    global pTime
    global i
    global listadd
    img = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
    results = hands.process(img)
    if results.multi_hand_landmarks:
        cTime = time.time()
        for handLms in results.multi_hand_landmarks:
            listx = []
            listy = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x *w), int(lm.y*h)
                #if id ==0:
                listx.append(cx)
                listy.append(cy)
            minx=min(listx)
            miny=min(listy)
            maxx=max(listx)
            maxy=max(listy)
            minx=constrainmin(minx,0)
            miny=constrainmin(miny,0)
            maxx=constrainmax(maxx,w)
            maxy=constrainmax(maxy,h)
            cropped_img= img[miny:maxy,minx:maxx]
            cv2.rectangle(img,(minx-param,miny-param),(maxx+param,maxy+param),(255,0,255), 2)
            image_size = 28
            new_array = cv2.resize(cropped_img, (image_size, image_size))
            test = new_array.reshape(-1, image_size, image_size, 1)
            print(cTime-pTime)
            if (cTime-pTime<2):
                if(i< len(word_dict)):
                    listadd.append(word_dict[i])
                #else:
                    #predict = model.predict([test])
                    #if (pred(predict) != 100):
                        #print(cathegories[pred(predict)])
                        #listadd.append(cathegories[pred(predict)])
            else :
                if(max(listadd,key=listadd.count)!="a"):
                    print(max(listadd,key=listadd.count))
                value=texts.get("1.0",END)
                value =word_list[max(listadd,key=listadd.count)]
                texts.insert(END, str(value))
                listadd=[]
                pTime = cTime
                i=i+1

    else:
        pTime=time.time()
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    frame.imgtk = imgtk
    frame.configure(image=imgtk)
    frame.after(1, show_frames,frame,texts)
#-----------------------------------------------------------------#
#wereting the data 
def datawrite():
    liste=[]
    sentence="شكرا على المساعدة"
word_dict=["sheen","kaaf","ra","aleff","ain","laam","yaa","aleff","laam","meem",
               "seen","aleff","ghain","ain","dal","ha","toot"]
word_list = { 'ain':'ع','al':'ال', 'aleff':'ا', 'bb':'ب','dal':'د','dha':'ذ','dhad':'ض','fa':'ف','gaaf':'ق','ghain':'غ',
             'ha':'ه', 'haa':'ح','jeem':'ج','kaaf':'ك','khaa':'خ','la':'لا','laam':'ل','meem':'م','nun':'ن','ra':'ر'
             ,'saad':'ص','seen':'س','sheen':'ش','ta':'ط','taa':'ت','thaa':'ث','thal':'ظ','toot':'ة','waw':'و',
              'ya':'ئ','yaa':'ي','zay':'ز'}

#get the predection from the model
def pred(predict):
    for i in predict:
        k = 0
        for j in i:
            if (int(j) == 1) and k < len(cathegories)+1:
                return k
            elif (k < len(cathegories) + 1):
                k += 1
            else:
                
                return 100;
