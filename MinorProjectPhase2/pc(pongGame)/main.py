# import cv2
# import cvzone
# from cvzone.HandTrackingModule import HandDetector
# import numpy as np

# cap = cv2.VideoCapture(0)
# cap.set(3, 1280) #640X480
# cap.set(4, 720)  #1280X720 HXW

# # Importing all images
# imgBackground = cv2.imread("Resources/Background.png")
# imgGameOver = cv2.imread("Resources/gameOver.png")
# imgBall = cv2.imread("Resources/Ball.png", cv2.IMREAD_UNCHANGED) #to remove user
# imgBat1 = cv2.imread("Resources/bat1.png", cv2.IMREAD_UNCHANGED)
# imgBat2 = cv2.imread("Resources/bat2.png", cv2.IMREAD_UNCHANGED)

# # Hand Detector
# detector = HandDetector(detectionCon=0.8, maxHands=2)

# # Variables
# ballPos = [100, 100]
# speedX = 5
# speedY = 5
# gameOver = False
# score = [0, 0]

# while True:
#     _, img = cap.read()
#     img = cv2.flip(img, 1) # 0 for vertical and 1 for horizontal but right left hand problem :(
#     imgRaw = img.copy()

#     # Find the hand and its landmarks
#     hands, img = detector.findHands(img, flipType=False)  # with draw right left hand problem solved :)
#     #we can remove line from hands by removing img from lhs and giving 3rd para as draw=false

#     # Overlaying the background image
#     img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

#     # Check for hands
#     if hands:
#         for hand in hands:
#             x, y, w, h = hand['bbox']
#             h1, w1, _ = imgBat1.shape #26X129
#             y1 = y - h1 // 2 #hight which will change , h1 // 2 for center pos not top
#             y1 = np.clip(y1, 20, 415) #upper and lower value of bat

#             if hand['type'] == "Left":
#                 img = cvzone.overlayPNG(img, imgBat1, (59, y1)) #placing bat
#                 if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:   #hittig bat
#                     speedX = -speedX
#                     ballPos[0] += 30 #illusion bouncing
#                     score[0] += 1

#             if hand['type'] == "Right":
#                 img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
#                 if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
#                     speedX = -speedX
#                     ballPos[0] -= 30
#                     score[1] += 1

#     # Game Over
#     if ballPos[0] < 40 or ballPos[0] > 1200:
#         gameOver = True

#     if gameOver:
#         img = imgGameOver
#         cv2.putText(img, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX,
#                     2.5, (200, 0, 200), 5)

#     # If game not over move the ball
#     else:

#         # Move the Ball or bounce back top and bottom
#         if ballPos[1] >= 500 or ballPos[1] <= 10:
#             speedY = -speedY

#         ballPos[0] += speedX
#         ballPos[1] += speedY

#         # Draw the ball
#         img = cvzone.overlayPNG(img, imgBall, ballPos) #3rd for pos (100,100)

#         cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
#         cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
#     #my img
#     img[580:700, 20:233] = cv2.resize(imgRaw, (213, 120))

#     cv2.imshow("Image", img)
#     key = cv2.waitKey(1)
#     #reset gamez
#     if key == ord('r'):
#         ballPos = [100, 100]
#         speedX = 15
#         speedY = 15
#         gameOver = False
#         score = [0, 0]
#         imgGameOver = cv2.imread("Resources/gameOver.png")

from flask import Flask, render_template, Response
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

app = Flask(__name__)

# Initialize OpenCV video capture
cap = cv2.VideoCapture(1)
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height

# Import images and initialize game variables
imgBackground = cv2.imread("Resources/Background.png")
imgGameOver = cv2.imread("Resources/gameOver.png")
imgBall = cv2.imread("Resources/Ball.png", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("Resources/bat1.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("Resources/bat2.png", cv2.IMREAD_UNCHANGED)
detector = HandDetector(detectionCon=0.8, maxHands=2)
ballPos = [100, 100]
speedX = 12
speedY = 12
gameOver = False
score = [0, 0]

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    global cap, imgBackground, imgGameOver, imgBall, imgBat1, imgBat2, detector, ballPos, speedX, speedY, gameOver, score

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)

        hands, img = detector.findHands(img, flipType=False)
        img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

        if hands:
            for hand in hands:
                x, y, w, h = hand['bbox']
                h1, w1, _ = imgBat1.shape
                y1 = y - h1 // 2
                y1 = np.clip(y1, 20, 415)

                if hand['type'] == "Left":
                    img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                    if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:
                        speedX = -speedX
                        ballPos[0] += 30
                        score[0] += 1

                if hand['type'] == "Right":
                    img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                    if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                        speedX = -speedX
                        ballPos[0] -= 30
                        score[1] += 1

        if ballPos[0] < 40 or ballPos[0] > 1200:
            gameOver = True

        if gameOver:
            img = imgGameOver
            cv2.putText(img, str(score[1] + score[0]).zfill(2), (585, 360), cv2.FONT_HERSHEY_COMPLEX,
                        2.5, (200, 0, 200), 5)
        else:
            if ballPos[1] >= 500 or ballPos[1] <= 10:
                speedY = -speedY

            ballPos[0] += speedX
            ballPos[1] += speedY

            img = cvzone.overlayPNG(img, imgBall, ballPos)

            cv2.putText(img, str(score[0]), (300, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)
            cv2.putText(img, str(score[1]), (900, 650), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 255, 255), 5)

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)

