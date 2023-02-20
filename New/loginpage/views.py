from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
import mediapipe as mp
import cv2 
from signbloom import views
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import math
from main import *

# Create your views here.
def home(request):
    return HttpResponse("Hello! I am working")

def Welcome(request):
    
    return render(request, 'C:/Users/anjil/Documents/Project Group/New/loginpage/templates/Firstpage.html')

def signin(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        Password = request.POST['Password']

        our_user = authenticate(username = Username, password = Password)

        if our_user is not None:
            login(request, our_user)
            fname = our_user.first_name
            return redirect('firstpage')
        else:
            messages.error(request, "Bad Credential")
            return redirect('signin')


    return render(request, 'C:/Users/anjil/Documents/Project Group/New/loginpage/Template/signin.html')

def signup(request):

    if request.method == "POST":
        Username = request.POST['Username']
        fname = request.POST['FirstName']
        lname = request.POST['LastName']
        Email = request.POST['Email']
        Password = request.POST['Password']
        confrim = request.POST['Confirm']

        if User.objects.filter(username=Username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('signup')
        
        if User.objects.filter(email=Email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('signin')

        myuser = User.objects.create_user(Username,Email,Password)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your account has been created!!")

        return redirect('signin')

    return render(request, 'C:/Users/anjil/Documents/Project Group/New/loginpage/Template/signup.html')

def firstpage(request):
    return render(request,'C:/Users/anjil/Documents/Project Group/New/loginpage/Template/firstpage.html')

def main(request):
    return render(request, 'C:/Users/anjil/Documents/Project Group/New/loginpage/Template/Main.html')

def detect(request):
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands


    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(min_detection_confidence = 0.8, min_tracking_confidence =  0.5) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            imageHeight,imageWidth,c = frame.shape

            #detection
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = cv2.flip(image,1)
            image.flags.writeable = False
            #DETECTIONSS
            results = hands.process(image)
            classNames = ''
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            print(results)
            
            if results.multi_hand_landmarks != None:
                landmarks = []
                for num, hand in enumerate(results.multi_hand_landmarks):
                    mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                                mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=1, circle_radius=4),#This one is for the circle
                                                mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)#This one is for the line
                                            )
            cv2.imshow('Hand Tracking', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

    return render(request,'firstpage.html')

def Recognition(request):
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)
    classifier = Classifier("Model/keras_model.h5","Model/labels.txt")
    counter = 0
    labels = ["A","B","Hello","I","I Love You","Yes"]
    offset = 20
    imgsize = 300
    while True:
        sucess, frame = cap.read()
        imgOutput = frame.copy()
        hands, frame = detector.findHands(frame)

        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']

            imgWhite = np.ones((imgsize,imgsize,3), np.uint8)*255

            imgCrop = frame[y - offset:y + h + offset, x - offset:x + w + offset]
            if imgCrop.shape[0] == 0 or imgCrop.shape[1] == 0:
                continue  

            ascpectRatio = h/w

            if ascpectRatio > 1:
                k = imgsize/h
                wCal = math.ceil(k*w)
                imgResize = cv2.resize(imgCrop,(wCal, imgsize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgsize-wCal)/2)
                imgWhite[:,wGap:wGap+wCal] = imgResize
                prediction, index = classifier.getPrediction(imgWhite,draw=False)
                print(prediction,index)
            else:
                k = imgsize/w
                hCal = math.ceil(k*h)
                imgResize = cv2.resize(imgCrop,(imgsize,hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgsize-hCal)/2)
                imgWhite[hGap:hGap+hCal, :] = imgResize
                prediction, index = classifier.getPrediction(imgWhite,draw=False)
                
            cv2.rectangle(imgOutput,(x-offset,y-offset-50),(x-offset+150,y-offset-50+50),(255,0,255),cv2.FILLED)
            cv2.putText(imgOutput, labels[index],(x,y-20),cv2.FONT_HERSHEY_COMPLEX,2,(255,255,255),2)
            cv2.rectangle(imgOutput,(x-offset,y-offset),(x+w+offset,y+h+offset),(255,0,255),4)

        cv2.imshow("ImageCrop",imgOutput)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break       

    cap.release()
    cv2.destroyAllWindows()

    return render(request,'C:/Users/anjil/Documents/Project Group/New/loginpage/Template/firstpage.html')

def sign_language(request):
    directory = 'loginpage/static/loginpage/hand'
    file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    alphabet = list(string.ascii_lowercase)
    sign_language_paths = dict(zip(alphabet, file_paths))
    
    transcribed_text = request.GET.get("text", "")
    transcribed_text = transcribed_text.lower()
    transcribed_words = transcribed_text.split()
    transcribed_words_and_image_paths = text_to_image_paths(transcribed_words, sign_language_paths)

    return render(request, 'C:/Users/anjil/Documents/Project Group/New/loginpage/Template/english.html', {"transcribed_words_and_image_paths": transcribed_words_and_image_paths})

def dictonary(request):
    return render(request, 'C:/Users/anjil/Documents/Project Group/New/loginpage/Template/dictonary.html')

def a(request):
    return render(request, 'C:/Users/anjil/Documents/Project Group/New/loginpage/Template/a1.html')

def about(request):
    return render(request, 'C:/Users/anjil/Documents/Project Group/New/loginpage/Template/about.html')


