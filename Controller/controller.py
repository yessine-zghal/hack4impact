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