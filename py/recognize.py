import cv2
import sqlite3
from .database import getProfileDataById
import time
import smtplib
import mimetypes
import way2sms
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '

import sys
import os
def send_msg():
    q = way2sms.sms(9892420886, 'motionsensor')
    q.send('9892420886', 'Intruder Alert')
    q.logout()
    print("sms sent")
def send_mail():
    sender = 'motionsensor4all@gmail.com'
    gmail_password = 'motionsensor4all@gmail'
    recipients = ['2015suraj.pawar@ves.ac.in']

    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'Alert !!!!'
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'Intruder has been deteted.\n'

    # List of attachments
    attachments = ['intruders/intruder.jpg']

    # Add the attachments to the message
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment',
                           filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ",
                  sys.exc_info()[0])
            raise

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise



def faceRecognize():
    faceCascPath = "haarcascade_frontalface_default.xml"
    eyeCascadePath = "haarcascade_eye.xml"
    faceCascade = cv2.CascadeClassifier(faceCascPath)
    eyeCascade = cv2.CascadeClassifier(eyeCascadePath)
    cam = cv2.VideoCapture(0)  # capture image here 0 is default webcam
    recog = cv2.face.LBPHFaceRecognizer_create()
    recog.read('recognized/training.yml')

    id = 0
    i=0
    while True:
        a, img = cam.read()  # will return true or false and image frame
        img = cv2.flip(img, 1)
        # convert image to gray scale image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray, 1.1, 5, flags=cv2.CASCADE_SCALE_IMAGE)
        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            eyes = eyeCascade.detectMultiScale(
            	face, 1.1, 5, flags=cv2.CASCADE_SCALE_IMAGE)
            if len(eyes) == 2:
                cv2.imwrite("intruders/intruder.jpg", face)
                faceId, confidence = recog.predict(face)
                # i = i+1
                # send_mail()
                if confidence < 60:
                    profile = getProfileDataById(str(faceId))
                    name = profile[1]
                    occupation = profile[2]
                    gender = profile[3]
                else:
                    name = "Unknown"
                    occupation = "Unknown"
                    gender = "Unknown"

                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 165, 0), 5)
                id, confidence = recog.predict(gray[y:y+h, x:x+w])

                if confidence < 60:
                    profile = getProfileDataById(str(id))
                    name = profile[1]
                    occupation = profile[2]
                    gender = profile[3]
                else:
                    name = "Unknown"
                    occupation = "Unknown"
                    gender = "Unknown"
                i=i+1
                print("wait")
                if i == 5:
                    print("...")
                    if confidence > 80:
                        send_mail()
                        send_msg()
                        break
    				
                cv2.putText(img, "Name- " + name, (x, y + h), cv2.FONT_HERSHEY_PLAIN, 1, (255, 69, 0), 2)
                cv2.putText(img, "Occupation- " + occupation, (x, y + h + 10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 69, 0), 2)
                cv2.putText(img, "Gender- " + gender, (x, y + h + 20),cv2.FONT_HERSHEY_PLAIN, 1, (255, 69, 0), 2)
                print("id = " + str(faceId) +" , confidence = " + str(confidence))

        cv2.imshow("Face Recognition Running", img)
        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
