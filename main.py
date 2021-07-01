import mediapipe as mp
import cv2
import numpy as np
import math
from datetime import datetime
import time
from tkinter import *
import matplotlib.pyplot as plt
from PIL import ImageTk, Image

image = None





def plot_array(reps, times):
    new_reps = []
    new_time = []
    time_periods = [0]

    for i in range(1, len(reps)):
        if (reps[i] != reps[i - 1]):
            new_reps.append(reps[i])
            new_time.append(times[i])

    for i in range(0, len(new_time) - 1):
        # print(new_time[i],end = " ")
        # print(new_time[i+1], end=" ")
        # print(" ")
        # print(abs((new_time[i+1]-new_time[i]).total_seconds()))
        time_periods.append(abs((new_time[i + 1] - new_time[i]).total_seconds()))
    return new_reps,time_periods


def runcurl():



    mpdrawing  = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose  #importing stuff for pose estimation and solutions

    cap = cv2.VideoCapture(0)
    landmarks = []

    reps = []
    times = []

    count = 0
    stage = None
    curr_count = 0
    next_count = 0

    time_at_down = None
    time_at_up = None



    def calc_angle(a,b,c):
        x_a = b[0] - a[0]
        y_a = b[1] - a[1]

        x_b = c[0] - b[0]
        y_b = c[1] - b[1]

        val = ((x_a*x_b)+(y_a*y_b))/((math.sqrt(x_a**2 + y_a**2))*(math.sqrt(x_b**2 + y_b**2)))

        rad = np.arccos(val)
        angle = rad*180/np.pi
        if angle > 180:
            return angle - 180
        return 180-angle





        #print(time_periods)





        #plt.plot(new_reps, time_periods)
        #plt.show()





    #setting us the mediapipe
    with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as Pose:
        while cap.isOpened():

            curr_count = count


            times.append(datetime.now())
            reps.append(count)




            ret, frame = cap.read()

            #detection and rendering
            global image
            image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            image.flags.writeable = False #memory saving ig?

            results = Pose.process(image) # We make our detection here. We will use this to render the detection points

            image.flags.writeable = True
            image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

            try:
                landmarks = results.pose_landmarks.landmark # we are grabbing all landmarks from here
                pt_array = np.array([])
                shoulder_array = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y,
                                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z])

                elbow_array = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y,
                                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].z])

                wrist_array = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                                        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y,
                                        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].z])

                angle = calc_angle(shoulder_array, elbow_array, wrist_array)

                cv2.putText(image, str(angle), tuple(np.multiply(elbow_array[:2],[640,480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (255,255,255), 2, cv2.LINE_AA)



                if angle >150:
                    stage='DOWN'
                    time_at_down = datetime.now()


                elif angle < 60 and stage == 'DOWN':
                    stage = 'UP'
                    count += 1
                    time_at_up = datetime.now()

                cv2.putText(image, "REPS "+str(count), (20,20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (255,255,255), 2, cv2.LINE_AA)


            except:
                pass



            #we start redering here
            mpdrawing.draw_landmarks(image,results.pose_landmarks, mp_pose.POSE_CONNECTIONS,mpdrawing.DrawingSpec(color=(245,117,66)),
                                     mpdrawing.DrawingSpec(color=(245,66,230)))
            #We are taking the landmarks from results, plotting them and then connecting them together
            #Results.pose_landmarks will give us the X,y,z coordinates of all the pointsqq
            cv2.imshow('Feed', image)


                # _, frame = cap.read()
                # cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)



            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

        #print(len(landmarks))
        #print(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x)
        #print(type(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value]))
        #print(len(times))
        #print(len(reps))

        return plot_array(reps,times)

