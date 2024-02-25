import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
# import screen_brightness_control as brightness


def main():
    if cv2.VideoCapture(1, cv2.CAP_DSHOW).isOpened():
        cam_num = 1
    else:
        cam_num = 0
    quit_button = "q"

    cap = cv2.VideoCapture(cam_num, cv2.CAP_DSHOW)
    detector = FaceMeshDetector(maxFaces=1)

    if not cap.isOpened():
        quit(f"Camera `{cam_num}` can't open!")

    while True:
        success, frame = cap.read()
        if not success:
            quit(f"Camera not usable!")

        # Finding faces
        frame, faces = detector.findFaceMesh(frame, draw=False)

        if faces:
            face = faces[0]
            pointLeft = face[145]
            pointRight = face[374]

            w, _ = detector.findDistance(pointLeft, pointRight)
            W = 6.3

            # Finding Focal Length
            # d = 62
            # f = (w * d) / W

            # IMPORTANT: F (Finding Distance)
            f = 600
            d = W * f / w
            print(d)

            # Depth is close
            if d <= 35:
                cvzone.putTextRect(frame, "Be careful", (20, 70), 5, 3, (0, 0, 255))
                # brightness.set_brightness(50)
            else:
                cvzone.putTextRect(frame, "Good", (20, 70), 5, 3, (0, 255, 0))
                # brightness.set_brightness(100)

            # Adding text in the video
            cvzone.putTextRect(frame,
                               f"Depth: {int(d)} cm",
                               (face[10][0] - 200, face[10][1] - 50),
                               scale=2
                               )

        cv2.imshow("Eye Guard", frame)
        if cv2.waitKey(1) == ord(quit_button):
            break

    cap.release()
    cv2.destroyAllWindows()


main()

# TODO: Resolution problem
