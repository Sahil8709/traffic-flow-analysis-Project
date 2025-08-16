import cv2

cap = cv2.VideoCapture("traffic_video.mp4")

if not cap.isOpened():
    print("❌ Failed to open traffic_video.mp4")
else:
    print("✅ Video opened successfully")

    success, frame = cap.read()
    if success:
        cv2.namedWindow("Test Frame", cv2.WINDOW_NORMAL)
        cv2.imshow("Test Frame", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("❌ Failed to read a frame from the video")

cap.release()