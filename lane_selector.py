# i have run this code separately to get the lane coordinates, just for evaluation purposes i have included it here.


import cv2
import json

# Store clicked points
points = []

# Mouse callback function
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Point {len(points)}: ({x}, {y})")
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
        cv2.putText(frame, f"{len(points)}", (x + 5, y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        cv2.imshow("Click to define lane", frame)

# Load video
video_path = "traffic_video.mp4"  # Replace with your actual video filename
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("❌ Failed to open video file.")
    exit()

# Read the first frame
ret, frame = cap.read()
cap.release()

if not ret:
    print("❌ Failed to read frame from video.")
    exit()

# Show frame and set mouse callback
cv2.imshow("Click to define lane", frame)
cv2.setMouseCallback("Click to define lane", click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save points to JSON
with open("lane_coordinates.json", "w") as f:
    json.dump(points, f)

print("✅ Coordinates saved to lane_coordinates.json")