import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

finger_tips = [8, 12, 16, 20]
thumb_tip = 4

stop_img = cv2.imread("images/stop.png")
stop_img = cv2.resize(stop_img, (200, 180))

upward_img = cv2.imread("images/upward.png")
upward_img = cv2.resize(upward_img, (200, 180))

downward_img = cv2.imread("images/downward.png")
downward_img = cv2.resize(downward_img, (200, 180))

left_img = cv2.imread("images/left.png")
left_img = cv2.resize(left_img, (200, 180))

right_img = cv2.imread("images/right.png")
right_img = cv2.resize(right_img, (200, 180))

like_img = cv2.imread("images/like.png")
like_img = cv2.resize(like_img, (200, 180))

dislike_img = cv2.imread("images/dislike.png")
dislike_img = cv2.resize(dislike_img, (200, 180))

while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    h, w, c = img.shape
    results = hands.process(img)

    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(hand_landmark.landmark):
                lm_list.append(lm)
            finger_fold_status = []
            for tip in finger_tips:
                x, y = int(lm_list[tip].x * w), int(lm_list[tip].y * h)
                # print(id, ":", x, y)
                #cv2.circle(img, (x, y), 15, (255, 0, 0), cv2.FILLED)

                if lm_list[tip].x < lm_list[tip - 2].x:
                    #cv2.circle(img, (x, y), 15, (0, 255, 0), cv2.FILLED)
                    finger_fold_status.append(True)
                else:
                    finger_fold_status.append(False)

            print(finger_fold_status)

            x, y = int(lm_list[8].x * w), int(lm_list[8].y * h)
            print(x, y)

            # stop
            if lm_list[4].y < lm_list[2].y and lm_list[8].y < lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                    lm_list[16].y < lm_list[14].y and lm_list[20].y < lm_list[18].y and lm_list[17].x < lm_list[0].x < \
                    lm_list[5].x:
                cv2.putText(img, "STOP", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                print("STOP")
                h, w, c = stop_img.shape
                img[35:h + 35, 30:w + 30] = stop_img

            # Upward
            if lm_list[3].x > lm_list[4].x and lm_list[8].y < lm_list[6].y and lm_list[12].y > lm_list[10].y and \
                    lm_list[16].y > lm_list[14].y and lm_list[20].y > lm_list[18].y:
                cv2.putText(img, "UPWARD", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                print("UPWARD")
                h, w, c = upward_img.shape
                img[35:h + 35, 30:w + 30] = upward_img

            # downward
            if lm_list[3].x > lm_list[4].x and lm_list[3].y < lm_list[4].y and lm_list[8].y > lm_list[6].y and lm_list[12].y < lm_list[10].y and \
                    lm_list[16].y < lm_list[14].y and lm_list[20].y < lm_list[18].y:
                cv2.putText(img, "DOWNWARD", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                print("DOWNWARD")
                h, w, c = downward_img.shape
                img[35:h + 35, 30:w + 30] = downward_img


            # Left
            if lm_list[4].y < lm_list[2].y and lm_list[8].x < lm_list[6].x and lm_list[12].x > lm_list[10].x and \
                    lm_list[16].x > lm_list[14].x and lm_list[20].x > lm_list[18].x and lm_list[5].x < lm_list[0].x:
                cv2.putText(img, "LEFT", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                print("LEFT")
                h, w, c = left_img.shape
                img[35:h + 35, 30:w + 30] = left_img

            # Right
            if lm_list[4].y < lm_list[2].y and lm_list[8].x > lm_list[6].x and lm_list[12].x < lm_list[10].x and \
                    lm_list[16].x < lm_list[14].x and lm_list[20].x < lm_list[18].x:
                cv2.putText(img, "RIGHT", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                print("RIGHT")
                h, w, c = right_img.shape
                img[35:h + 35, 30:w + 30] = right_img


            if all(finger_fold_status):
                # like
                if lm_list[thumb_tip].y < lm_list[thumb_tip - 1].y < lm_list[thumb_tip - 2].y and lm_list[0].x < lm_list[3].y:
                    print("LIKE")
                    cv2.putText(img, "LIKE", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                    h, w, c = like_img.shape
                    img[35:h + 35, 30:w + 30] = like_img
                # Dislike
                if lm_list[thumb_tip].y > lm_list[thumb_tip - 1].y > lm_list[thumb_tip - 2].y and lm_list[0].x < lm_list[3].y:
                    cv2.putText(img, "DISLIKE", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    print("DISLIKE")
                    h, w, c = dislike_img.shape
                    img[35:h + 35, 30:w + 30] = dislike_img


            mp_draw.draw_landmarks(img, hand_landmark,
                                   mp_hands.HAND_CONNECTIONS,
                                   mp_draw.DrawingSpec((0, 0, 255), 6, 3),
                                   mp_draw.DrawingSpec((0, 255, 0), 4, 2)
                                   )

    cv2.imshow("Hand Sign Detection", img)
    cv2.waitKey(1)
