import numpy as np
import cv2
from ultralytics import YOLO
from sort import Sort
import csv
import os

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Load traffic video
cap = cv2.VideoCapture("traffic_video.mp4")
if not cap.isOpened():
    print("Failed to open traffic_video.mp4")
    exit()

# Get frame size and FPS
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Set up video writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("output.avi", fourcc, 30.0, (frame_width, frame_height))

# Lane polygons
# Lane polygons
lanes = {
    1: [(182, 375), (491, 405), (446, 591), (73, 512)],
    2: [(550, 319), (679, 315), (703, 423), (549, 415)],
    3: [(947, 435), (1132, 539), (837, 562), (1095, 669)]
}

# Initialize SORT tracker
tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

# Prepare lane count CSV
csv_file = open("lane_counts.csv", mode="w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Frame", "Lane 1", "Lane 2", "Lane 3"])

# Prepare vehicle log CSV
vehicle_log = open("vehicle_log.csv", mode="w", newline="")
vehicle_writer = csv.writer(vehicle_log)
vehicle_writer.writerow(["Frame", "Vehicle ID", "Lane", "Timestamp (s)"])

# Track counted vehicle IDs per lane
lane_ids = {1: set(), 2: set(), 3: set()}
frame_count = 0

# Define vehicle class IDs (COCO dataset)
vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("✅ Finished processing video.")
        break

    frame_count += 1
    annotated_frame = frame.copy()

    # Run YOLOv8 detection
    results = model(frame)
    detections = []

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            if class_id not in vehicle_classes:
                continue

            x1, y1, x2, y2 = map(float, box.xyxy[0])
            conf = float(box.conf[0])
            detections.append([x1, y1, x2, y2])

    print(f"Frame {frame_count} | YOLO detections: {len(detections)}")

    detections_np = np.array(detections)
    tracked_objects = tracker.update(detections_np)

    print(f"Frame {frame_count} | SORT tracked: {len(tracked_objects)}")

    # Draw lanes
    for lane_id, points in lanes.items():
        cv2.polylines(annotated_frame, [np.array(points)], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.putText(annotated_frame, f"Lane {lane_id}", points[0], cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Count vehicles per lane
    lane_counts = {1: 0, 2: 0, 3: 0}
    for obj in tracked_objects:
        x1, y1, x2, y2, obj_id = map(int, obj)
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        cv2.circle(annotated_frame, (center_x, center_y), 4, (0, 0, 255), -1)
        print(f"  ID {obj_id} center: ({center_x},{center_y})")

        for lane_id, points in lanes.items():
            polygon = np.array(points, np.int32)
            inside = cv2.pointPolygonTest(polygon, (center_x, center_y), False)
            print(f"    Lane {lane_id}: inside={inside}")

            if inside >= 0:
                if obj_id not in lane_ids[lane_id]:
                    lane_counts[lane_id] += 1
                    lane_ids[lane_id].add(obj_id)

                    # Log to vehicle_log.csv
                    timestamp = frame_count / fps
                    vehicle_writer.writerow([frame_count, obj_id, lane_id, round(timestamp, 2)])
                break

        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
        cv2.putText(annotated_frame, f"ID {obj_id}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    # Show lane counts
    y_offset = 30
    for lane_id, count in lane_counts.items():
        cv2.putText(annotated_frame, f"Lane {lane_id}: {count}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        y_offset += 30

    # Show cumulative totals
    for lane_id in lane_ids:
        cv2.putText(annotated_frame, f"Total Lane {lane_id}: {len(lane_ids[lane_id])}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        y_offset += 30

    # Save frame to video
    out.write(annotated_frame)

    # Write cumulative counts to lane_counts.csv
    csv_writer.writerow([
        frame_count,
        len(lane_ids[1]),
        len(lane_ids[2]),
        len(lane_ids[3])
    ])

    # Show frame
    cv2.imshow("Traffic Detection", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
csv_file.close()
vehicle_log.close()
cv2.destroyAllWindows()





# compressing the output video using FFmpeg duue to its large size git is not accepting file more than 100MB

import subprocess

# Compress output.avi using FFmpeg
compressed_output = "output_compressed.mp4"
ffmpeg_cmd = [
    "ffmpeg",
    "-i", "output.avi",         # Input file
    "-vf", "scale=1280:720",    # Resize to 720p (optional)
    "-b:v", "1M",               # Set video bitrate to 1 Mbps
    "-b:a", "128k",             # Set audio bitrate
    "-y", compressed_output     # Overwrite if exists
]

print("🎬 Compressing output video with FFmpeg...")
subprocess.run(ffmpeg_cmd)
print(f"✅ Compression complete: {compressed_output}")