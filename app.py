from flask import Flask,render_template,Response,request
import cv2
import face_recognition_models
from flask.wrappers import Request
import face_recognition
import numpy as np
import os
from datetime import datetime


app=Flask(__name__)
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
#global name


for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findEncodings(images):
    encodingList = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodingList.append(encode)
    return encodingList

# def markAttendance(name):

#     with open('Attendance.csv','r+') as f:
#         mydatalist = f.readlines()
#         namelist = []
#         now = datetime.now()
#         dstring = now.strftime('%d/%m/%Y')
#         for line in mydatalist:
#             entry = line.split(',')
#             namelist.append(entry[0])
#         if name not in namelist :
#             now = datetime.now()
#             tstring = now.strftime('%H:%M:%S')
#             dstring = now.strftime('%d/%m/%Y')
#             daystring = now.strftime('%A')
#             if tstring <= '10:15:00':
#                 Statuslist = "IN-TIME"
#             else:
#                 Statuslist = "LATE"


#             f.writelines(f'\n{name},{tstring},{dstring},{daystring},{Statuslist}')



camera=cv2.VideoCapture(0)
encodeListKnown = findEncodings(images)

def generate_frames():
    while True:
            
        ## read the camera frame
        success,frame=camera.read()

        if not success:
            break
        else:
            small_frame = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
            rgb_small_frame = small_frame[:,:,::-1]
            facesCurFrame = face_recognition.face_locations(rgb_small_frame)
            encodesCurFrame = face_recognition.face_encodings(rgb_small_frame,facesCurFrame)

            for encodeFace,faceloc in zip(encodesCurFrame,facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
                print(faceDis)
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    global name
                    name = classNames[matchIndex].upper()
                    print(name)
                    y1,x2,y2,x1 = faceloc
                    y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                    cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                    cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,200),2)
                    #markAttendance(name)

                else:
                    name = "UNKNOWN"
                    print(name)
                    y1, x2, y2, x1 = faceloc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(frame, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 200), 2)

            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()
            yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    print(generate_frames())

    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/result', methods = ['POST'])
def result():
    if request.method == 'POST':
        if "login" in request.form:
            with open('Attendance.csv', 'a') as f:
                if (name != 'UNKNOWN'):
                    date_time_string = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                    day= datetime.now().strftime('%A')
                    f.writelines(f'\n{name},{date_time_string},{day},Log In')
                    return render_template('login.html',name=name)
                else:
                    return render_template('unknown.html')

        elif "logout" in  request.form:
             with open('Attendance.csv', 'a') as f:
                if (name != 'UNKNOWN'):
                    date_time_string = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
                    day= datetime.now().strftime('%A')
                    f.writelines(f'\n{name},{date_time_string},{day},Log out')
                    return render_template('logout.html',name=name)
                else:
                    return render_template('unknown.html')
    #return render_template('login.html',name = name)

    

   

if __name__=="__main__":
    app.run(debug=True)
