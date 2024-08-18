from flask import Flask, render_template, Response
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    
    detector = HandDetector(maxHands=1)
    timer = 0
    stateResult = False
    startGame = False
    score = [0, 0]  # [AI, Player]
    initialTime = 0  # Define initialTime here
    
    while True:
        success, img = cap.read()
        if not success:
            break
        
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        imgScaled = cv2.resize(imgRGB, (640, 480))
        
        hands, _ = detector.findHands(imgScaled)
        
        if startGame and not stateResult:
            timer = time.time() - initialTime
            
            if timer > 3:
                stateResult = True
                timer = 0
                
                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    elif fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    elif fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3
                    
                    randomNumber = random.randint(1, 3)
                    imgAI = cv2.imread(f'Resources/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgRGB = cvzone.overlayPNG(imgRGB, imgAI, (160, 253))
                    
                    if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        score[1] += 1
                    elif (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        score[0] += 1
        
        imgRGB = cv2.cvtColor(imgRGB, cv2.COLOR_RGB2BGR)
        
        ret, buffer = cv2.imencode('.jpg', imgRGB)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
